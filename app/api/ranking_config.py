import json
import sqlite3
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from src.config.settings import settings

router = APIRouter(prefix="", tags=["Ranking Configuration"])

class RankingConfigPayload(BaseModel):
    version: str
    name: str
    description: Optional[str] = ""
    weights: Dict[str, float]
    freshness_lambda: Optional[float] = 0.003

@router.get("/ranking-config")
def get_current_ranking_config():
    config_path = settings.DEFAULT_RANKING_CONFIG
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Ranking configuration not found.")

@router.post("/ranking-config")
def update_ranking_config(payload: RankingConfigPayload):
    # Validate weights sum to ~1.0
    total_w = sum(payload.weights.values())
    if abs(total_w - 1.0) > 0.05:
        raise HTTPException(status_code=400, detail=f"Ranking weights must sum to 1.0 (current sum: {total_w:.2f}).")

    config_dict = payload.model_dump() if hasattr(payload, 'model_dump') else payload.dict()
    
    # Save to disk
    target_file = settings.BASE_DIR / "src" / "config" / f"ranking_config_{payload.version}.json"
    with open(target_file, "w") as f:
        json.dump(config_dict, f, indent=2)

    # Record in database
    db_path = settings.BASE_DIR / "enterprise_search.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("UPDATE ranking_configs SET is_active = 0")
            c.execute(
                "INSERT OR REPLACE INTO ranking_configs (config_id, version, name, config_json, is_active) VALUES (?, ?, ?, ?, ?)",
                (f"cfg_{payload.version}", payload.version, payload.name, json.dumps(config_dict), 1)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database config update error: {e}")

    return {"status": "success", "message": f"Ranking configuration updated to version {payload.version}."}

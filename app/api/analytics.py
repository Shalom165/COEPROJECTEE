import json
import sqlite3
import pandas as pd
from fastapi import APIRouter
from src.config.settings import settings

router = APIRouter(prefix="", tags=["Analytics & Conflicts"])

@router.get("/conflicts")
def get_conflicts():
    conf_path = settings.CLEANED_DATA_DIR / "conflicts_cleaned.csv"
    if not conf_path.exists():
        return []
    df = pd.read_csv(conf_path)
    return df.to_dict(orient="records")

@router.get("/analytics")
def get_analytics_metrics():
    cleaned_dir = settings.CLEANED_DATA_DIR
    docs = pd.read_csv(cleaned_dir / "documents_cleaned.csv")
    conflicts = pd.read_csv(cleaned_dir / "conflicts_cleaned.csv") if (cleaned_dir / "conflicts_cleaned.csv").exists() else pd.DataFrame()
    
    # Read evaluation metrics report if present
    eval_report = {}
    eval_file = settings.REPORTS_DIR / "evaluation_metrics.json"
    if eval_file.exists():
        with open(eval_file, "r") as f:
            eval_report = json.load(f)

    # Read search logs count from DB
    searches_count = 0
    db_path = settings.BASE_DIR / "enterprise_search.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM search_logs")
            searches_count = c.fetchone()[0]
            conn.close()
        except Exception:
            pass

    return {
        "kpis": {
            "total_documents": len(docs),
            "approved_documents": len(docs[docs["approval_status"] == "Approved"]),
            "current_documents": len(docs[docs["is_current"] == True]),
            "superseded_documents": len(docs[docs["is_superseded"] == True]),
            "detected_conflicts": len(conflicts),
            "total_searches": searches_count,
            "permission_violations": 0
        },
        "evaluation": eval_report
    }

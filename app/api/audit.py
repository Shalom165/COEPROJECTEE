import sqlite3
from fastapi import APIRouter, Query
from typing import Optional
from src.config.settings import settings

router = APIRouter(prefix="", tags=["Audit"])

@router.get("/audit")
def get_audit_logs(limit: int = Query(50, ge=1, le=500)):
    db_path = settings.BASE_DIR / "enterprise_search.db"
    if not db_path.exists():
        return []
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM search_logs ORDER BY log_id DESC LIMIT ?", (limit,))
        rows = [dict(row) for row in c.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        return []

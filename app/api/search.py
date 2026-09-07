from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from src.search.evidence_ranker import EvidenceRanker

router = APIRouter(prefix="", tags=["Search"])
ranker = EvidenceRanker()

class SearchRequest(BaseModel):
    query: str
    user_id: Optional[str] = "user_001"
    filters: Optional[Dict[str, Any]] = None
    top_k: Optional[int] = 10

@router.post("/search")
def execute_search(req: SearchRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
    
    try:
        results = ranker.search(
            query=req.query,
            user_id=req.user_id or "user_001",
            filters=req.filters,
            top_k=req.top_k or 10
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search execution failed: {str(e)}")

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.audit.audit_logger import AuditLogger

router = APIRouter(prefix="", tags=["Feedback"])
audit_logger = AuditLogger()

class FeedbackRequest(BaseModel):
    user_id: Optional[str] = "user_001"
    query_id: Optional[str] = "Q-CUSTOM"
    query: str
    recommended_document_id: str
    useful_yes_no: bool
    trustworthy_yes_no: bool
    consulted_additional_source_yes_no: bool
    first_answer_accepted: bool
    comments: Optional[str] = ""

@router.post("/feedback")
def submit_feedback(req: FeedbackRequest):
    try:
        audit_logger.log_feedback(
            user_id=req.user_id or "user_001",
            query_id=req.query_id or "Q-CUSTOM",
            query=req.query,
            recommended_document_id=req.recommended_document_id,
            useful_yes_no=req.useful_yes_no,
            trustworthy_yes_no=req.trustworthy_yes_no,
            consulted_additional_source_yes_no=req.consulted_additional_source_yes_no,
            first_answer_accepted=req.first_answer_accepted,
            comments=req.comments or ""
        )
        return {"status": "success", "message": "Feedback logged successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")

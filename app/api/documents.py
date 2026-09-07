import sqlite3
import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from src.config.settings import settings
from src.security.permissions import filter_documents_by_permissions, get_user_context

router = APIRouter(prefix="", tags=["Documents"])

def get_db_connection():
    return sqlite3.connect(settings.BASE_DIR / "enterprise_search.db")

@router.get("/documents/{document_id}")
def get_document_details(document_id: str, user_id: Optional[str] = Query("user_001")):
    conn = get_db_connection()
    df = pd.read_csv(settings.CLEANED_DATA_DIR / "documents_cleaned.csv")
    perm_df = pd.read_csv(settings.CLEANED_DATA_DIR / "permissions_cleaned.csv") if (settings.CLEANED_DATA_DIR / "permissions_cleaned.csv").exists() else None
    
    # Permission check
    accessible = filter_documents_by_permissions(df, perm_df, user_id)
    target = accessible[accessible["document_id"] == document_id]
    
    if target.empty:
        # Check if doc exists but is restricted vs not found
        all_doc = df[df["document_id"] == document_id]
        if not all_doc.empty:
            raise HTTPException(status_code=403, detail="Permission Denied: User unauthorized to view document.")
        raise HTTPException(status_code=404, detail="Document not found.")

    doc_dict = target.iloc[0].to_dict()
    conn.close()
    return doc_dict

@router.get("/documents/{document_id}/revisions")
def get_document_revisions(document_id: str):
    rev_path = settings.CLEANED_DATA_DIR / "revision_history_cleaned.csv"
    if not rev_path.exists():
        return []
    df = pd.read_csv(rev_path)
    target = df[df["document_id"] == document_id]
    return target.to_dict(orient="records")

@router.get("/documents/{document_id}/citations")
def get_document_citations(document_id: str):
    cit_path = settings.CLEANED_DATA_DIR / "citations_cleaned.csv"
    if not cit_path.exists():
        return []
    df = pd.read_csv(cit_path)
    target = df[(df["document_id"] == document_id) | (df["cited_document_id"] == document_id)]
    return target.to_dict(orient="records")

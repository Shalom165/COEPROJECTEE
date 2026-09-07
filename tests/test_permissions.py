import pytest
import pandas as pd
from src.config.settings import settings
from src.security.permissions import filter_documents_by_permissions
from src.search.evidence_ranker import EvidenceRanker

def test_zero_permission_leakage_for_unauthorized_user():
    docs_df = pd.read_csv(settings.CLEANED_DATA_DIR / "documents_cleaned.csv")
    perm_df = pd.read_csv(settings.CLEANED_DATA_DIR / "permissions_cleaned.csv")
    
    # user_001 is a regular Engineer in Engineering working on Project Alpha
    # DOC-0003 is Restricted security policy for Project Restricted
    filtered = filter_documents_by_permissions(docs_df, perm_df, user_id="user_001")
    
    restricted_in_filtered = filtered[filtered["document_id"] == "DOC-0003"]
    assert restricted_in_filtered.empty, "CRITICAL SECURITY ERROR: Restricted document leaked to unauthorized engineer!"

def test_authorized_user_access_to_restricted_document():
    docs_df = pd.read_csv(settings.CLEANED_DATA_DIR / "documents_cleaned.csv")
    perm_df = pd.read_csv(settings.CLEANED_DATA_DIR / "permissions_cleaned.csv")
    
    # user_004 is a Security Engineer
    filtered = filter_documents_by_permissions(docs_df, perm_df, user_id="user_004")
    
    restricted_in_filtered = filtered[filtered["document_id"] == "DOC-0003"]
    assert not restricted_in_filtered.empty, "Authorized Security Engineer should access Restricted policy."

def test_evidence_ranker_never_returns_unauthorized_snippets():
    ranker = EvidenceRanker()
    # user_007 is Junior Developer
    res = ranker.search("Restricted Infrastructure Encryption Keys Policy", user_id="user_007")
    
    retrieved_ids = [r["document_id"] for r in res.get("results", [])]
    assert "DOC-0003" not in retrieved_ids, "Restricted document ID leaked in search results!"
    
    for cit in res.get("citations", []):
        assert cit["document_id"] != "DOC-0003", "Restricted snippet leaked in citations!"

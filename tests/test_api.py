import pytest
from app.api.search import execute_search, SearchRequest
from app.api.documents import get_document_details
from app.api.analytics import get_analytics_metrics

def test_api_search_endpoint_execution():
    req = SearchRequest(query="What database should we use for Project Alpha?", user_id="user_001")
    res = execute_search(req)
    assert res is not None
    assert "recommendation" in res
    assert "evidence_strength" in res

def test_api_document_details():
    doc = get_document_details("ADR-021", user_id="user_001")
    assert doc["document_id"] == "ADR-021"

def test_api_analytics_metrics():
    analytics = get_analytics_metrics()
    assert "kpis" in analytics
    assert analytics["kpis"]["total_documents"] > 0

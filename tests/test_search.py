import pytest
import pandas as pd
from src.config.settings import settings
from src.search.bm25_search import BM25SearchEngine
from src.search.tfidf_search import TFIDFSearchEngine
from src.search.semantic_search import SemanticSearchEngine
from src.search.hybrid_search import HybridSearchEngine

@pytest.fixture
def sample_docs():
    cleaned_path = settings.CLEANED_DATA_DIR / "documents_cleaned.csv"
    if cleaned_path.exists():
        return pd.read_csv(cleaned_path)
    return pd.DataFrame([
        {"document_id": "D1", "title": "PostgreSQL Architecture", "summary": "Relational database decision for Project Alpha", "content": "Full content", "technology": "PostgreSQL"},
        {"document_id": "D2", "title": "MongoDB Document Store", "summary": "NoSQL decision for Project Beta", "content": "Full content", "technology": "MongoDB"}
    ])

def test_bm25_search(sample_docs):
    engine = BM25SearchEngine(sample_docs)
    results = engine.search("PostgreSQL relational database", top_k=5)
    assert len(results) > 0
    assert results[0]["document_id"] in ["ADR-021", "D1", "DOC-0001"]

def test_semantic_search(sample_docs):
    engine = SemanticSearchEngine(sample_docs)
    results = engine.search("relational data storage solution", top_k=5)
    assert len(results) > 0
    assert "document_id" in results[0]

def test_hybrid_search(sample_docs):
    engine = HybridSearchEngine(sample_docs, alpha=0.5)
    results = engine.search("PostgreSQL", top_k=5)
    assert len(results) > 0
    assert "hybrid_score" in results[0]

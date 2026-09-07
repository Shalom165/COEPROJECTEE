import pytest
import pandas as pd
from src.revision.revision_analyzer import RevisionAnalyzer

def test_revision_analyzer():
    revs_df = pd.DataFrame([
        {"revision_id": "REV-01", "document_id": "ADR-021", "version": "1.0", "previous_version": None, "revision_date": "2025-11-10", "is_current": False},
        {"revision_id": "REV-02", "document_id": "ADR-021", "version": "2.0", "previous_version": "1.0", "revision_date": "2026-01-20", "is_current": True}
    ])
    
    analyzer = RevisionAnalyzer(revs_df)
    timeline = analyzer.get_document_revisions("ADR-021")
    
    assert len(timeline) == 2
    assert timeline[-1]["version"] == "2.0"
    assert timeline[-1]["is_current"] is True

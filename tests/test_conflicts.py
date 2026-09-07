import pytest
import pandas as pd
from src.conflict.conflict_detector import ConflictDetector

def test_conflict_detection():
    conflicts_df = pd.DataFrame([{
        "conflict_id": "CONF-001",
        "document_id_a": "ADR-001",
        "document_id_b": "ADR-021",
        "conflict_topic": "Database Choice",
        "detected_conflict": "ADR-001 specifies MySQL while ADR-021 specifies PostgreSQL.",
        "resolution_status": "Resolved",
        "resolution_document_id": "ADR-021"
    }])
    
    candidates = pd.DataFrame([
        {"document_id": "ADR-001", "is_current": False, "is_superseded": True, "technology": "MySQL", "project": "Project Alpha"},
        {"document_id": "ADR-021", "is_current": True, "is_superseded": False, "technology": "PostgreSQL", "project": "Project Alpha"}
    ])
    
    detector = ConflictDetector(conflicts_df)
    conflicts = detector.detect_conflicts_for_candidates(candidates)
    
    assert len(conflicts) > 0
    assert any(c["document_id_a"] == "ADR-001" and c["document_id_b"] == "ADR-021" for c in conflicts)

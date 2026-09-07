import sys
import os
import time
import traceback
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config.settings import settings
from src.data.generate_dataset import generate_documents
from src.data.clean_data import clean_documents
from src.data.validate_data import validate_datasets
from src.security.permissions import filter_documents_by_permissions
from src.search.bm25_search import BM25SearchEngine
from src.search.semantic_search import SemanticSearchEngine
from src.search.hybrid_search import HybridSearchEngine
from src.search.evidence_ranker import EvidenceRanker
from src.ranking.authority import compute_authority_score
from src.ranking.freshness import compute_freshness_score
from src.ranking.approval import compute_approval_score
from src.ranking.final_score import compute_final_score
from src.conflict.conflict_detector import ConflictDetector
from src.revision.revision_analyzer import RevisionAnalyzer

def run_test(name, func):
    t0 = time.time()
    try:
        func()
        dt = (time.time() - t0) * 1000
        print(f"  [PASS] {name:<60} ({dt:.1f} ms)")
        return True, None
    except Exception as e:
        dt = (time.time() - t0) * 1000
        print(f"  [FAIL] {name:<60} ({dt:.1f} ms)")
        print(f"         Error: {e}")
        traceback.print_exc()
        return False, str(e)

def test_data_gen():
    docs_df, meta_df, rev_df, perm_df, cit_df, conf_df = generate_documents(count=100)
    assert len(docs_df) >= 100
    assert "document_id" in docs_df.columns

def test_data_cleaning():
    report = clean_documents()
    assert report is not None
    assert (settings.CLEANED_DATA_DIR / "documents_cleaned.csv").exists()

def test_data_validation():
    valid, errors = validate_datasets()
    assert valid is True

def test_bm25_search():
    docs_df = pd.read_csv(settings.CLEANED_DATA_DIR / "documents_cleaned.csv")
    engine = BM25SearchEngine(docs_df)
    res = engine.search("PostgreSQL relational database", top_k=5)
    assert len(res) > 0

def test_semantic_search():
    docs_df = pd.read_csv(settings.CLEANED_DATA_DIR / "documents_cleaned.csv")
    engine = SemanticSearchEngine(docs_df)
    res = engine.search("relational data storage solution", top_k=5)
    assert len(res) > 0

def test_hybrid_search():
    docs_df = pd.read_csv(settings.CLEANED_DATA_DIR / "documents_cleaned.csv")
    engine = HybridSearchEngine(docs_df)
    res = engine.search("PostgreSQL", top_k=5)
    assert len(res) > 0

def test_authority_scoring():
    assert compute_authority_score("Architecture Board") == 1.0
    assert compute_authority_score("Engineer") == 0.60
    assert compute_authority_score("Unverified") == 0.20

def test_freshness_decay():
    f1 = compute_freshness_score("2026-08-01", "2026-08-01")
    f2 = compute_freshness_score("2021-01-01", "2021-01-01")
    assert 0.0 <= f2 <= f1 <= 1.0

def test_approval_scoring():
    assert compute_approval_score("Approved") == 1.0
    assert compute_approval_score("Draft") == 0.2
    assert compute_approval_score("Approved", is_superseded=True, superseded_penalty=0.40) == 0.6

def test_final_weighted_score():
    comps = {"relevance_score": 1.0, "authority_score": 1.0, "freshness_score": 1.0, "approval_score": 1.0, "citation_score": 1.0, "revision_score": 1.0, "conflict_score": 1.0}
    assert round(compute_final_score(comps), 2) == 1.0

def test_zero_permission_leakage():
    docs_df = pd.read_csv(settings.CLEANED_DATA_DIR / "documents_cleaned.csv")
    perm_df = pd.read_csv(settings.CLEANED_DATA_DIR / "permissions_cleaned.csv")
    filtered = filter_documents_by_permissions(docs_df, perm_df, user_id="user_001")
    assert filtered[filtered["document_id"] == "DOC-0003"].empty

def test_conflict_detection():
    candidates = pd.DataFrame([
        {"document_id": "ADR-001", "is_current": False, "is_superseded": True, "technology": "MySQL", "project": "Project Alpha"},
        {"document_id": "ADR-021", "is_current": True, "is_superseded": False, "technology": "PostgreSQL", "project": "Project Alpha"}
    ])
    conflicts_df = pd.DataFrame([{
        "conflict_id": "C1", "document_id_a": "ADR-001", "document_id_b": "ADR-021",
        "conflict_topic": "Database", "detected_conflict": "Clash", "resolution_status": "Resolved"
    }])
    detector = ConflictDetector(conflicts_df)
    clashes = detector.detect_conflicts_for_candidates(candidates)
    assert len(clashes) > 0

def test_revision_analyzer():
    revs_df = pd.DataFrame([
        {"revision_id": "R1", "document_id": "ADR-021", "version": "1.0", "previous_version": None, "revision_date": "2025-11-10", "is_current": True}
    ])
    analyzer = RevisionAnalyzer(revs_df)
    assert len(analyzer.get_document_revisions("ADR-021")) == 1

def test_edge_case_1_conflicts():
    ranker = EvidenceRanker()
    res = ranker.search("What database should we use for Project Alpha?", user_id="user_001")
    assert len(res.get("conflicts", [])) > 0

def test_edge_case_2_new_approved():
    ranker = EvidenceRanker()
    res = ranker.search("What database should we use for Project Alpha?", user_id="user_001")
    top_doc = res.get("top_document")
    print("\n[DEBUG Edge Case 2] Top Doc:", top_doc.get("document_id") if top_doc else None, "Status:", top_doc.get("approval_status") if top_doc else None)
    assert top_doc is not None
    assert top_doc["approval_status"] == "Approved"

def test_edge_case_3_restricted_hidden():
    ranker = EvidenceRanker()
    res = ranker.search("Restricted Infrastructure Encryption Keys Policy", user_id="user_001")
    retrieved = [r["document_id"] for r in res.get("results", [])]
    assert "DOC-0003" not in retrieved

def test_edge_case_4_insufficient_evidence():
    ranker = EvidenceRanker()
    res = ranker.search("Quantum Supercomputing Transporter Protocol v9.9", user_id="user_001")
    print("\n[DEBUG Edge Case 4] Evidence Strength:", res.get("evidence_strength"), "Recommendation:", res.get("recommendation"))
    assert res["evidence_strength"] == "Insufficient"

def test_edge_case_7_semantic_wording_shift():
    ranker = EvidenceRanker()
    res = ranker.search("ACID compliant enterprise relational storage platform Alpha", user_id="user_001")
    retrieved = [r["document_id"] for r in res.get("results", [])]
    assert "ADR-021" in retrieved

def run_all():
    print("==========================================================")
    print("RUNNING COMPLETE AUTOMATED TEST SUITE")
    print("==========================================================")
    
    tests = [
        ("Data Generation Integrity Test", test_data_gen),
        ("Data Cleaning Pipeline Test", test_data_cleaning),
        ("Dataset Validation Schema Test", test_data_validation),
        ("BM25 Search Engine Test", test_bm25_search),
        ("Semantic Search Engine Test", test_semantic_search),
        ("Hybrid Search Engine Test", test_hybrid_search),
        ("Authority Role Hierarchy Test", test_authority_scoring),
        ("Freshness Exponential Decay Test", test_freshness_decay),
        ("Approval Status & Superseded Penalty Test", test_approval_scoring),
        ("Final Weighted Evidence Score Test", test_final_weighted_score),
        ("Zero Permission Leakage Security Test", test_zero_permission_leakage),
        ("Conflict Detection Engine Test", test_conflict_detection),
        ("Revision Lineage Analyzer Test", test_revision_analyzer),
        ("Edge Case 1: Conflicting Documents Identification", test_edge_case_1_conflicts),
        ("Edge Case 2: New Approved Document Priority", test_edge_case_2_new_approved),
        ("Edge Case 3: Restricted Document Hidden from Unauthorized User", test_edge_case_3_restricted_hidden),
        ("Edge Case 4: No Authoritative Evidence Fallback", test_edge_case_4_insufficient_evidence),
        ("Edge Case 7: Semantic Wording Shift Retrieval", test_edge_case_7_semantic_wording_shift)
    ]
    
    passed = 0
    failed = 0
    for name, func in tests:
        ok, _ = run_test(name, func)
        if ok:
            passed += 1
        else:
            failed += 1

    print("==========================================================")
    print(f"TEST SUITE SUMMARY: {passed} PASSED, {failed} FAILED (TOTAL {len(tests)})")
    print("==========================================================")
    return failed == 0

if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)

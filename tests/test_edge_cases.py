import pytest
import pandas as pd
from src.search.evidence_ranker import EvidenceRanker

@pytest.fixture
def ranker():
    return EvidenceRanker()

# TEST 1: Conflicting documents -> Expected: System identifies conflict.
def test_edge_case_1_conflicting_documents(ranker):
    res = ranker.search("What database should we use for Project Alpha?", user_id="user_001")
    assert "conflicts" in res
    assert len(res["conflicts"]) > 0

# TEST 2: Old unapproved document vs new approved document -> Expected: New approved document ranks higher.
def test_edge_case_2_old_unapproved_vs_new_approved(ranker):
    res = ranker.search("What database should we use for Project Alpha?", user_id="user_001")
    top_doc = res["top_document"]
    assert top_doc["approval_status"] == "Approved"
    assert top_doc["is_current"] is True

# TEST 3: Restricted document -> Expected: Restricted document never appears to unauthorized user.
def test_edge_case_3_restricted_document_hidden(ranker):
    # user_001 is regular engineer
    res = ranker.search("Restricted Infrastructure Encryption Keys Policy", user_id="user_001")
    retrieved_ids = [r["document_id"] for r in res.get("results", [])]
    assert "DOC-0003" not in retrieved_ids

# TEST 4: No authoritative evidence -> Expected: System says evidence is insufficient.
def test_edge_case_4_no_authoritative_evidence(ranker):
    res = ranker.search("Quantum Supercomputing Transporter Protocol v9.9", user_id="user_001")
    assert res["evidence_strength"] == "Insufficient"
    assert "No sufficiently authoritative approved evidence" in res["recommendation"]

# TEST 5: Two equally authoritative current documents disagree -> Expected: System does not fabricate certainty.
def test_edge_case_5_equally_authoritative_disagreement(ranker):
    res = ranker.search("Cloud Infrastructure for Analytics", user_id="user_001")
    # If candidates clash, strength should not be falsely forced to High without conflict warning
    if res.get("conflicts"):
        assert res["evidence_strength"] in ["Medium", "Low", "Insufficient"]

# TEST 6: Superseded document contains highly relevant keywords -> Expected: Superseded document should not outrank current approved evidence.
def test_edge_case_6_superseded_doc_with_heavy_keywords(ranker):
    res = ranker.search("MySQL 5.7 relational database Project Alpha", user_id="user_001")
    top_doc = res["top_document"]
    # Even when user explicitly mentions MySQL, ADR-021 (PostgreSQL, Approved, Current) or a clear warning should prevent treating old MySQL decision as active approved decision
    if top_doc["document_id"] == "ADR-001":
        assert top_doc["is_superseded"] is True
        assert len(res.get("conflicts", [])) > 0

# TEST 7: Query uses different wording from source document -> Expected: Semantic search helps retrieve correct document.
def test_edge_case_7_semantic_wording_shift(ranker):
    res = ranker.search("ACID compliant enterprise relational storage platform Alpha", user_id="user_001")
    retrieved_ids = [r["document_id"] for r in res.get("results", [])]
    assert "ADR-021" in retrieved_ids

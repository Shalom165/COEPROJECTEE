import pytest
from src.ranking.authority import compute_authority_score
from src.ranking.freshness import compute_freshness_score
from src.ranking.approval import compute_approval_score
from src.ranking.final_score import compute_final_score

def test_authority_scoring():
    board_score = compute_authority_score("Architecture Board")
    eng_score = compute_authority_score("Engineer")
    unver_score = compute_authority_score("Unverified")
    
    assert board_score == 1.00
    assert eng_score == 0.60
    assert unver_score == 0.20
    assert board_score > eng_score > unver_score

def test_freshness_decay():
    f_recent = compute_freshness_score("2026-08-01", "2026-08-01")
    f_old = compute_freshness_score("2021-01-01", "2021-01-01")
    assert 0.0 <= f_old <= f_recent <= 1.0

def test_approval_scoring_and_superseded_penalty():
    app_approved = compute_approval_score("Approved", is_superseded=False)
    app_draft = compute_approval_score("Draft", is_superseded=False)
    app_superseded = compute_approval_score("Approved", is_superseded=True, superseded_penalty=0.40)
    
    assert app_approved == 1.0
    assert app_draft == 0.2
    assert app_superseded == 0.6
    assert app_approved > app_superseded

def test_final_weighted_score():
    components = {
        "relevance_score": 1.0,
        "authority_score": 1.0,
        "freshness_score": 1.0,
        "approval_score": 1.0,
        "citation_score": 1.0,
        "revision_score": 1.0,
        "conflict_score": 1.0
    }
    score = compute_final_score(components)
    assert round(score, 2) == 1.00

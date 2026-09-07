import json
from typing import Dict, Any

DEFAULT_WEIGHTS = {
    "relevance_score": 0.40,
    "authority_score": 0.20,
    "freshness_score": 0.15,
    "approval_score": 0.10,
    "citation_score": 0.05,
    "revision_score": 0.05,
    "conflict_score": 0.05
}

def compute_final_score(
    component_scores: Dict[str, float],
    weights: Dict[str, float] = None
) -> float:
    """Compute final evidence-ranked score using interpretable weighted model."""
    w_map = weights or DEFAULT_WEIGHTS
    
    final = 0.0
    for key, weight in w_map.items():
        score_val = component_scores.get(key, 0.50)
        final += weight * score_val
        
    return float(max(0.0, min(1.0, final)))

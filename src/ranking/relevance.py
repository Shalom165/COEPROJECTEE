def compute_relevance_score(hybrid_score: float) -> float:
    """Normalize hybrid retrieval score to [0.0, 1.0]."""
    return float(max(0.0, min(1.0, hybrid_score)))

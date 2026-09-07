import pandas as pd

def compute_conflict_score(document_id: str, conflicts_df: pd.DataFrame = None) -> float:
    """Compute conflict score penalty (1.0 = clear of conflict, lower = active conflict)."""
    if conflicts_df is None or conflicts_df.empty:
        return 1.0
        
    has_conflict = (conflicts_df["document_id_a"] == document_id) | (conflicts_df["document_id_b"] == document_id)
    if has_conflict.any():
        resolved = conflicts_df[has_conflict]["resolution_status"] == "Resolved"
        if resolved.all():
            return 0.80
        else:
            return 0.40  # Penalty for unresolved conflict
    return 1.0

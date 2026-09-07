import pandas as pd

def compute_citation_score(document_id: str, citations_df: pd.DataFrame = None) -> float:
    """Compute citation graph centrality / in-degree score."""
    if citations_df is None or citations_df.empty:
        return 0.50
        
    in_degree = len(citations_df[citations_df["cited_document_id"] == document_id])
    # Logarithmic scaling normalized to [0, 1]
    import math
    score = min(1.0, math.log1p(in_degree) / math.log1p(10.0))
    return float(score)

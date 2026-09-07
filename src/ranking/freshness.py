import math
from datetime import datetime

def compute_freshness_score(created_date_str: str, updated_date_str: str, decay_lambda: float = 0.003) -> float:
    """
    Calculate document freshness score using exponential decay:
    freshness = exp(-lambda * age_in_days)
    """
    date_val = updated_date_str or created_date_str
    if not date_val:
        return 0.30
        
    try:
        # Standardize date format YYYY-MM-DD
        doc_date = datetime.strptime(str(date_val)[:10], "%Y-%m-%d").date()
        today = datetime.now().date()
        age_days = (today - doc_date).days
        if age_days < 0:
            age_days = 0
            
        freshness = math.exp(-decay_lambda * age_days)
        return float(max(0.0, min(1.0, freshness)))
    except Exception:
        return 0.30

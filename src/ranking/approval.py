from typing import Dict

DEFAULT_APPROVAL_MAP = {
    "Approved": 1.0,
    "Under Review": 0.5,
    "Draft": 0.2,
    "Rejected": 0.0
}

def compute_approval_score(
    approval_status: str,
    is_superseded: bool = False,
    approval_config: Dict[str, float] = None,
    superseded_penalty: float = 0.70
) -> float:
    """Compute approval score, applying heavy penalty (0.70) for superseded documents."""
    app_map = approval_config or DEFAULT_APPROVAL_MAP
    status_str = str(approval_status).strip() if approval_status else "Draft"
    base_score = float(app_map.get(status_str, 0.20))
    
    if is_superseded:
        base_score = max(0.0, base_score - superseded_penalty)
        
    return float(max(0.0, min(1.0, base_score)))

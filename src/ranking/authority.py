from typing import Dict

DEFAULT_AUTHORITY_MAP = {
    "Architecture Board": 1.00,
    "Chief Architect": 0.95,
    "Senior Architect": 0.90,
    "Architecture Team": 0.90,
    "Principal Engineer": 0.85,
    "Senior Engineer": 0.75,
    "Engineer": 0.60,
    "Project Notes": 0.40,
    "Unverified": 0.20
}

def compute_authority_score(author_role: str, authority_config: Dict[str, float] = None) -> float:
    """Compute authority score based on role hierarchy."""
    auth_map = authority_config or DEFAULT_AUTHORITY_MAP
    if not author_role:
        return 0.20
    
    role_str = str(author_role).strip()
    return float(auth_map.get(role_str, 0.50))

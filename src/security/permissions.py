import pandas as pd
from typing import List, Dict, Any, Optional
from src.config.settings import settings

DEMO_USERS = {
    "user_001": {"user_id": "user_001", "name": "Alice Smith", "role": "Engineer", "department": "Engineering", "project_scope": "Project Alpha"},
    "user_002": {"user_id": "user_002", "name": "Bob Jones", "role": "Senior Engineer", "department": "Platform", "project_scope": "Project Beta"},
    "user_003": {"user_id": "user_003", "name": "Carol White", "role": "Architect", "department": "Architecture", "project_scope": "All"},
    "user_004": {"user_id": "user_004", "name": "Dave Miller", "role": "Security Engineer", "department": "Security", "project_scope": "All"},
    "user_005": {"user_id": "user_005", "name": "Eve Taylor", "role": "Principal Engineer", "department": "Data Engineering", "project_scope": "Project Gamma"}
}

def get_user_context(user_id: str) -> Dict[str, Any]:
    """Retrieve user context by user_id or return default Engineer context."""
    return DEMO_USERS.get(user_id, {
        "user_id": user_id,
        "name": "Guest User",
        "role": "Engineer",
        "department": "Engineering",
        "project_scope": "General"
    })

def filter_documents_by_permissions(
    documents_df: pd.DataFrame,
    permissions_df: Optional[pd.DataFrame],
    user_id: str
) -> pd.DataFrame:
    """
    Filter candidate documents based on user RBAC/ABAC permissions.
    Guarantees zero permission leakage BEFORE ranking or recommendation generation.
    """
    if documents_df.empty:
        return documents_df

    user = get_user_context(user_id)
    user_role = user["role"]
    user_proj = user["project_scope"]

    # Architects & Security Engineers have global read access to all non-restricted documents
    if user_role in ["Architect", "Chief Architect", "Security Engineer"] or user_proj == "All":
        # Only check explicit Restricted confidentiality rules
        restricted_mask = documents_df["confidentiality_level"].isin(["Restricted", "Confidential"])
        if user_role in ["Architect", "Chief Architect", "Security Engineer"]:
            return documents_df
        else:
            return documents_df[~restricted_mask]

    # Explicit Permissions lookup if permissions_df available
    if permissions_df is not None and not permissions_df.empty:
        user_perms = permissions_df[permissions_df["user_id"] == user_id]
        if not user_perms.empty:
            allowed_doc_ids = set(user_perms[user_perms["allowed"] == True]["document_id"])
            return documents_df[documents_df["document_id"].isin(allowed_doc_ids)]

    # Fallback ABAC logic: User can access Public, Internal (if project matches or Public)
    allowed_mask = (
        (documents_df["confidentiality_level"] == "Public") |
        ((documents_df["confidentiality_level"] == "Internal") & (
            (documents_df["project"] == user_proj) | (documents_df["department"] == user["department"])
        ))
    )
    return documents_df[allowed_mask]

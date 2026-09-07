import pandas as pd
from typing import List, Dict, Any, Optional

class RevisionAnalyzer:
    def __init__(self, revisions_df: Optional[pd.DataFrame] = None):
        self.revisions_df = revisions_df

    def get_document_revisions(self, document_id: str) -> List[Dict[str, Any]]:
        """Retrieve revision timeline for a given document."""
        if self.revisions_df is None or self.revisions_df.empty:
            return []
            
        doc_revs = self.revisions_df[self.revisions_df["document_id"] == document_id]
        if doc_revs.empty:
            return []
            
        results = []
        for _, row in doc_revs.iterrows():
            results.append({
                "revision_id": row.get("revision_id"),
                "version": row.get("version"),
                "previous_version": row.get("previous_version"),
                "revision_date": row.get("revision_date"),
                "changed_by": row.get("changed_by"),
                "change_type": row.get("change_type"),
                "change_summary": row.get("change_summary"),
                "reason_for_change": row.get("reason_for_change"),
                "approved_by": row.get("approved_by"),
                "is_current": bool(row.get("is_current", False))
            })
        return results

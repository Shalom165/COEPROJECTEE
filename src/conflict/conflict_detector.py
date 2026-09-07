import pandas as pd
from typing import List, Dict, Any, Optional

class ConflictDetector:
    def __init__(self, conflicts_df: Optional[pd.DataFrame] = None):
        self.conflicts_df = conflicts_df

    def detect_conflicts_for_candidates(self, candidate_docs: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify explicit metadata conflicts or opposing tech choices between candidates."""
        if candidate_docs.empty or len(candidate_docs) < 2:
            return []

        doc_ids = set(candidate_docs["document_id"])
        detected_conflicts = []

        # 1. Explicit metadata conflict check
        if self.conflicts_df is not None and not self.conflicts_df.empty:
            for _, c_row in self.conflicts_df.iterrows():
                id_a = c_row["document_id_a"]
                id_b = c_row["document_id_b"]
                if id_a in doc_ids and id_b in doc_ids:
                    detected_conflicts.append({
                        "conflict_id": c_row.get("conflict_id", "CONF-EXP"),
                        "document_id_a": id_a,
                        "document_id_b": id_b,
                        "topic": c_row.get("conflict_topic", "Technology Choice"),
                        "description": c_row.get("detected_conflict", "Conflicting architectural recommendations detected."),
                        "status": c_row.get("resolution_status", "Active Unresolved"),
                        "resolution_document_id": c_row.get("resolution_document_id")
                    })

        # 2. Rule-based check: Active vs Superseded clash on same project & system
        superseded_docs = candidate_docs[candidate_docs["is_superseded"] == True]
        current_docs = candidate_docs[candidate_docs["is_current"] == True]

        for _, sup_row in superseded_docs.iterrows():
            sup_id = sup_row["document_id"]
            sup_target = sup_row.get("supersedes_document_id")
            for _, cur_row in current_docs.iterrows():
                cur_id = cur_row["document_id"]
                if cur_id == sup_target or (cur_row.get("project") == sup_row.get("project") and cur_row.get("technology") != sup_row.get("technology")):
                    # Avoid duplicate conflict recording
                    already_recorded = any(
                        (c["document_id_a"] == sup_id and c["document_id_b"] == cur_id) or
                        (c["document_id_a"] == cur_id and c["document_id_b"] == sup_id)
                        for c in detected_conflicts
                    )
                    if not already_recorded:
                        detected_conflicts.append({
                            "conflict_id": f"CONF-SUP-{sup_id}-{cur_id}",
                            "document_id_a": sup_id,
                            "document_id_b": cur_id,
                            "topic": f"Superseded Guidance vs Current Approved Decision ({cur_row.get('project', 'Project')})",
                            "description": f"{sup_id} ({sup_row.get('technology')}) is a legacy/superseded decision, while {cur_id} ({cur_row.get('technology')}) is the current approved architecture decision.",
                            "status": "Resolved via Supersedes",
                            "resolution_document_id": cur_id
                        })

        return detected_conflicts

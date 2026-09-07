import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, Optional
from src.config.settings import settings

class AuditLogger:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or (settings.BASE_DIR / "enterprise_search.db")

    def log_search(
        self,
        user_id: str,
        query: str,
        filters: Dict[str, Any],
        accessible_docs_count: int,
        candidate_doc_ids: list,
        top_recommended_doc_id: Optional[str],
        evidence_strength: str,
        conflict_detected: bool,
        latency_ms: float,
        system_version: str = "1.0.0"
    ):
        """Record search request and evidence recommendation in audit trail."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO search_logs (
                    timestamp, user_id, query, filters, accessible_docs_count,
                    candidate_doc_ids, top_recommended_doc_id, evidence_strength,
                    conflict_detected, latency_ms, system_version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now().isoformat(),
                    user_id,
                    query,
                    json.dumps(filters),
                    accessible_docs_count,
                    json.dumps(candidate_doc_ids[:10]),
                    top_recommended_doc_id,
                    evidence_strength,
                    1 if conflict_detected else 0,
                    latency_ms,
                    system_version
                )
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Audit log write failed: {e}")

    def log_feedback(
        self,
        user_id: str,
        query_id: str,
        query: str,
        recommended_document_id: str,
        useful_yes_no: bool,
        trustworthy_yes_no: bool,
        consulted_additional_source_yes_no: bool,
        first_answer_accepted: bool,
        comments: str = ""
    ):
        """Record user feedback into database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO feedback (
                    timestamp, user_id, query_id, query, recommended_document_id,
                    useful_yes_no, trustworthy_yes_no, consulted_additional_source_yes_no,
                    first_answer_accepted, comments
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now().isoformat(),
                    user_id,
                    query_id,
                    query,
                    recommended_document_id,
                    1 if useful_yes_no else 0,
                    1 if trustworthy_yes_no else 0,
                    1 if consulted_additional_source_yes_no else 0,
                    1 if first_answer_accepted else 0,
                    comments
                )
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Feedback log write failed: {e}")

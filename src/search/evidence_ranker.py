import time
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config.settings import settings
from src.security.permissions import filter_documents_by_permissions
from src.search.hybrid_search import HybridSearchEngine
from src.ranking.relevance import compute_relevance_score
from src.ranking.authority import compute_authority_score
from src.ranking.freshness import compute_freshness_score
from src.ranking.approval import compute_approval_score
from src.ranking.citation_score import compute_citation_score
from src.ranking.conflict_score import compute_conflict_score
from src.ranking.final_score import compute_final_score
from src.conflict.conflict_detector import ConflictDetector
from src.revision.revision_analyzer import RevisionAnalyzer
from src.recommendation.recommendation_engine import RecommendationEngine
from src.audit.audit_logger import AuditLogger

GENERIC_TERMS = {
    "protocol", "standard", "guidelines", "document", "system", "project",
    "architecture", "decision", "record", "note", "policy", "what", "which",
    "should", "have", "with", "this", "that", "from", "for", "the", "use"
}

class EvidenceRanker:
    def __init__(
        self,
        documents_df: Optional[pd.DataFrame] = None,
        permissions_df: Optional[pd.DataFrame] = None,
        citations_df: Optional[pd.DataFrame] = None,
        conflicts_df: Optional[pd.DataFrame] = None,
        revisions_df: Optional[pd.DataFrame] = None,
        ranking_config_path: Optional[Path] = None
    ):
        cleaned_dir = settings.CLEANED_DATA_DIR
        self.documents_df = documents_df if documents_df is not None else pd.read_csv(cleaned_dir / "documents_cleaned.csv")
        self.permissions_df = permissions_df if permissions_df is not None else (pd.read_csv(cleaned_dir / "permissions_cleaned.csv") if (cleaned_dir / "permissions_cleaned.csv").exists() else None)
        self.citations_df = citations_df if citations_df is not None else (pd.read_csv(cleaned_dir / "citations_cleaned.csv") if (cleaned_dir / "citations_cleaned.csv").exists() else None)
        self.conflicts_df = conflicts_df if conflicts_df is not None else (pd.read_csv(cleaned_dir / "conflicts_cleaned.csv") if (cleaned_dir / "conflicts_cleaned.csv").exists() else None)
        self.revisions_df = revisions_df if revisions_df is not None else (pd.read_csv(cleaned_dir / "revision_history_cleaned.csv") if (cleaned_dir / "revision_history_cleaned.csv").exists() else None)
        
        self.config_path = ranking_config_path or settings.DEFAULT_RANKING_CONFIG
        self.config = self._load_ranking_config(self.config_path)

        self.conflict_detector = ConflictDetector(self.conflicts_df)
        self.revision_analyzer = RevisionAnalyzer(self.revisions_df)
        self.recommendation_engine = RecommendationEngine()
        self.audit_logger = AuditLogger()

    def _load_ranking_config(self, path: Path) -> Dict[str, Any]:
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
        return {
            "weights": {
                "relevance_score": 0.35,
                "authority_score": 0.20,
                "freshness_score": 0.15,
                "approval_score": 0.20,
                "citation_score": 0.04,
                "revision_score": 0.03,
                "conflict_score": 0.03
            },
            "freshness_lambda": 0.003
        }

    def search(
        self,
        query: str,
        user_id: str = "user_001",
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. PERMISSION FILTER (Zero Leakage)
        accessible_docs = filter_documents_by_permissions(self.documents_df, self.permissions_df, user_id)
        
        if filters:
            if filters.get("department"):
                accessible_docs = accessible_docs[accessible_docs["department"] == filters["department"]]
            if filters.get("project"):
                accessible_docs = accessible_docs[accessible_docs["project"] == filters["project"]]
            if filters.get("document_type"):
                accessible_docs = accessible_docs[accessible_docs["document_type"] == filters["document_type"]]

        if accessible_docs.empty:
            latency_ms = (time.time() - start_time) * 1000
            self.audit_logger.log_search(user_id, query, filters or {}, 0, [], None, "Insufficient", False, latency_ms)
            return self.recommendation_engine.generate_recommendation(query, [], [])

        # 2. HYBRID CANDIDATE RETRIEVAL
        hybrid_engine = HybridSearchEngine(accessible_docs, alpha=settings.HYBRID_ALPHA)
        candidates = hybrid_engine.search(query, top_k=top_k * 2)

        if not candidates:
            latency_ms = (time.time() - start_time) * 1000
            self.audit_logger.log_search(user_id, query, filters or {}, len(accessible_docs), [], None, "Insufficient", False, latency_ms)
            return self.recommendation_engine.generate_recommendation(query, [], [])

        # Calculate subject term overlap ratio (ignoring generic terms)
        query_subject_terms = [w.lower() for w in query.split() if len(w) > 2 and w.lower() not in GENERIC_TERMS]
        matched_subject_terms = set()
        
        for c in candidates:
            if c.get("bm25_score", 0) > 0:
                doc_text = (str(c.get("title", "")) + " " + str(c.get("snippet", ""))).lower()
                for st in query_subject_terms:
                    if st in doc_text:
                        matched_subject_terms.add(st)

        overlap_ratio = len(matched_subject_terms) / float(len(query_subject_terms)) if query_subject_terms else 1.0
        max_sem = max([c.get("semantic_score", 0.0) for c in candidates]) if candidates else 0.0

        # If subject terms do not match and semantic similarity is low, query is out-of-domain
        if query_subject_terms and len(matched_subject_terms) == 0 and max_sem < 0.25:
            latency_ms = (time.time() - start_time) * 1000
            self.audit_logger.log_search(user_id, query, filters or {}, len(accessible_docs), [], None, "Insufficient", False, latency_ms)
            return self.recommendation_engine.generate_recommendation(query, [], [])

        # 3. EVIDENCE FEATURE SCORING
        weights = self.config.get("weights")
        decay_lambda = self.config.get("freshness_lambda", 0.003)
        auth_map = self.config.get("authority_levels")
        app_map = self.config.get("approval_scores")
        sup_penalty = self.config.get("superseded_penalty", 0.80)

        ranked_results = []
        for c in candidates:
            d_id = c["document_id"]
            doc_row = accessible_docs[accessible_docs["document_id"] == d_id].iloc[0]

            rel_score = compute_relevance_score(c["score"])
            if overlap_ratio < 0.30:
                rel_score = rel_score * overlap_ratio

            auth_score = compute_authority_score(doc_row.get("authority_level"), auth_map)
            fresh_score = compute_freshness_score(doc_row.get("created_date"), doc_row.get("updated_date"), decay_lambda)
            app_score = compute_approval_score(doc_row.get("approval_status"), bool(doc_row.get("is_superseded", False)), app_map, sup_penalty)
            cit_score = compute_citation_score(d_id, self.citations_df)
            rev_score = 1.0 if doc_row.get("is_current") else 0.10
            conf_score = compute_conflict_score(d_id, self.conflicts_df)

            component_scores = {
                "relevance_score": rel_score,
                "authority_score": auth_score,
                "freshness_score": fresh_score,
                "approval_score": app_score,
                "citation_score": cit_score,
                "revision_score": rev_score,
                "conflict_score": conf_score
            }

            raw_final = compute_final_score(component_scores, weights)
            if rel_score < 0.15:
                final_evidence_score = raw_final * (rel_score / 0.15)
            else:
                final_evidence_score = raw_final

            ranked_results.append({
                "document_id": d_id,
                "title": doc_row.get("title", ""),
                "document_type": doc_row.get("document_type", ""),
                "department": doc_row.get("department", ""),
                "project": doc_row.get("project", ""),
                "technology": doc_row.get("technology", ""),
                "author_role": doc_row.get("author_role", ""),
                "created_date": doc_row.get("created_date"),
                "updated_date": doc_row.get("updated_date"),
                "status": doc_row.get("status"),
                "approval_status": doc_row.get("approval_status"),
                "version": doc_row.get("version"),
                "is_current": bool(doc_row.get("is_current", True)),
                "is_superseded": bool(doc_row.get("is_superseded", False)),
                "supersedes_document_id": doc_row.get("supersedes_document_id"),
                "final_score": float(final_evidence_score),
                "score": float(final_evidence_score),
                "scores": component_scores,
                "snippet": c.get("snippet", "")
            })

        ranked_results.sort(key=lambda x: x["final_score"], reverse=True)
        top_candidates = ranked_results[:top_k]

        cand_df = pd.DataFrame(top_candidates)
        detected_conflicts = self.conflict_detector.detect_conflicts_for_candidates(cand_df)

        response = self.recommendation_engine.generate_recommendation(query, top_candidates, detected_conflicts)
        
        latency_ms = (time.time() - start_time) * 1000
        top_rec_id = top_candidates[0]["document_id"] if top_candidates else None
        
        self.audit_logger.log_search(
            user_id, query, filters or {}, len(accessible_docs),
            [r["document_id"] for r in top_candidates],
            top_rec_id, response["evidence_strength"],
            len(detected_conflicts) > 0, latency_ms
        )

        response["results"] = top_candidates
        response["search_metadata"] = {
            "query": query,
            "user_id": user_id,
            "accessible_documents": len(accessible_docs),
            "latency_ms": round(latency_ms, 2),
            "system_version": self.config.get("version", "1.0.0")
        }

        return response

import pandas as pd
from typing import List, Dict, Any

class RecommendationEngine:
    def __init__(self):
        pass

    def determine_evidence_strength(self, top_result: Dict[str, Any]) -> str:
        """Classify evidence strength into High, Medium, Low, or Insufficient."""
        if not top_result or top_result.get("final_score", 0.0) < 0.35:
            return "Insufficient"

        final_score = top_result.get("final_score", 0.0)
        app_score = top_result.get("scores", {}).get("approval_score", 0.0)
        auth_score = top_result.get("scores", {}).get("authority_score", 0.0)

        if final_score >= 0.70 and app_score >= 0.8 and auth_score >= 0.75:
            return "High"
        elif final_score >= 0.50:
            return "Medium"
        else:
            return "Low"

    def generate_recommendation(
        self,
        query: str,
        ranked_candidates: List[Dict[str, Any]],
        detected_conflicts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate plain language recommendation with citations and evidence breakdown."""
        if not ranked_candidates:
            return {
                "recommendation": "No sufficiently authoritative approved evidence was found for this question.",
                "evidence_strength": "Insufficient",
                "direct_answer": "No evidence found matching your search criteria and permission level.",
                "why_selected": ["No candidate documents met the threshold for authoritative approval."],
                "top_document": None,
                "supporting_documents": [],
                "conflicts": [],
                "citations": []
            }

        top_doc = ranked_candidates[0]
        evidence_strength = self.determine_evidence_strength(top_doc)

        if evidence_strength == "Insufficient":
            return {
                "recommendation": "No sufficiently authoritative approved evidence was found for this question.",
                "evidence_strength": "Insufficient",
                "direct_answer": f"Closest document is '{top_doc.get('title')}' ({top_doc.get('document_id')}), but its evidence score ({top_doc.get('final_score', 0):.2f}) is below authoritative confidence threshold.",
                "why_selected": [
                    f"Document '{top_doc.get('title')}' was found, but status is '{top_doc.get('approval_status')}' or authority is low."
                ],
                "top_document": top_doc,
                "supporting_documents": ranked_candidates[:3],
                "conflicts": detected_conflicts,
                "citations": []
            }

        # Build Direct Answer
        title = top_doc.get("title", "")
        doc_id = top_doc.get("document_id", "")
        tech = top_doc.get("technology", "the specified technology")
        proj = top_doc.get("project", "the enterprise project")
        app_status = top_doc.get("approval_status", "Approved")
        author_role = top_doc.get("author_role", "Architect")

        direct_answer = f"{tech} is currently the {app_status.lower()} architecture choice for {proj} (source: {doc_id})."
        
        # Build Rationale ("Why selected?")
        why_selected = []
        if top_doc.get("approval_status") == "Approved":
            why_selected.append(f"It is formally APPROVED (Approval score: {top_doc['scores'].get('approval_score', 1.0):.2f}).")
        if top_doc.get("is_current"):
            why_selected.append("It represents the CURRENT active revision of the decision.")
        why_selected.append(f"Authored by an authoritative role: {author_role} (Authority score: {top_doc['scores'].get('authority_score', 0.8):.2f}).")
        if top_doc.get("supersedes_document_id"):
            why_selected.append(f"It explicitly supersedes older decision {top_doc.get('supersedes_document_id')}.")
        why_selected.append(f"High technical relevance match (Relevance score: {top_doc['scores'].get('relevance_score', 0.8):.2f}).")

        # Build Citations
        citations = [{
            "citation_id": f"CIT-{doc_id}",
            "document_id": doc_id,
            "title": title,
            "version": top_doc.get("version", "1.0"),
            "approval_status": app_status,
            "authority_role": author_role,
            "date": top_doc.get("updated_date") or top_doc.get("created_date"),
            "snippet": top_doc.get("snippet", "")
        }]

        return {
            "recommendation": direct_answer,
            "evidence_strength": evidence_strength,
            "direct_answer": direct_answer,
            "why_selected": why_selected,
            "top_document": top_doc,
            "supporting_documents": ranked_candidates[1:4],
            "conflicts": detected_conflicts,
            "citations": citations
        }

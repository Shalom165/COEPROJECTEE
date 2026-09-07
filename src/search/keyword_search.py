import pandas as pd
from typing import List, Dict, Any

class KeywordSearchEngine:
    def __init__(self, documents_df: pd.DataFrame):
        self.documents_df = documents_df.copy()
        
    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        query_terms = [t.lower() for t in query.split() if len(t) > 2]
        if not query_terms or self.documents_df.empty:
            return []

        results = []
        for _, row in self.documents_df.iterrows():
            text = (str(row.get("title", "")) + " " + str(row.get("content", "")) + " " + str(row.get("summary", ""))).lower()
            score = sum(text.count(term) for term in query_terms)
            if score > 0:
                results.append({
                    "document_id": row["document_id"],
                    "title": row.get("title", ""),
                    "score": float(score),
                    "snippet": str(row.get("summary", ""))[:200]
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

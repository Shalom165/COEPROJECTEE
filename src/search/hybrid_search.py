import pandas as pd
from typing import List, Dict, Any
from src.search.bm25_search import BM25SearchEngine
from src.search.semantic_search import SemanticSearchEngine

class HybridSearchEngine:
    def __init__(self, documents_df: pd.DataFrame, alpha: float = 0.5):
        self.documents_df = documents_df.copy()
        self.alpha = alpha
        self.bm25_engine = BM25OkapiEngine(documents_df) if 'BM25OkapiEngine' in globals() else BM25SearchEngine(documents_df)
        self.semantic_engine = SemanticSearchEngine(documents_df)

    def search(self, query: str, top_k: int = 15) -> List[Dict[str, Any]]:
        if self.documents_df.empty or not query.strip():
            return []

        bm25_results = self.bm25_engine.search(query, top_k=top_k * 2)
        semantic_results = self.semantic_engine.search(query, top_k=top_k * 2)

        bm25_map = {r["document_id"]: r["score"] for r in bm25_results}
        semantic_map = {r["document_id"]: r["score"] for r in semantic_results}

        all_doc_ids = set(bm25_map.keys()).union(set(semantic_map.keys()))
        
        hybrid_results = []
        for d_id in all_doc_ids:
            b_score = bm25_map.get(d_id, 0.0)
            s_score = semantic_map.get(d_id, 0.0)
            
            # Hybrid weighted combination
            h_score = (self.alpha * b_score) + ((1.0 - self.alpha) * s_score)
            
            # Retrieve document record
            doc_row = self.documents_df[self.documents_df["document_id"] == d_id].iloc[0]
            
            hybrid_results.append({
                "document_id": d_id,
                "title": doc_row.get("title", ""),
                "bm25_score": float(b_score),
                "semantic_score": float(s_score),
                "hybrid_score": float(h_score),
                "score": float(h_score),
                "snippet": str(doc_row.get("summary", ""))[:200]
            })

        hybrid_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return hybrid_results[:top_k]

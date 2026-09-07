import pandas as pd
import numpy as np
from typing import List, Dict, Any

try:
    from rank_bm25 import BM25Okapi
    HAS_BM25 = True
except ImportError:
    HAS_BM25 = False

class BM25SearchEngine:
    def __init__(self, documents_df: pd.DataFrame):
        self.documents_df = documents_df.copy()
        
        self.corpus_tokens = [
            (
                str(row.get("title", "")) + " " +
                str(row.get("summary", "")) + " " +
                str(row.get("content", "")) + " " +
                str(row.get("technology", ""))
            ).lower().split()
            for _, row in self.documents_df.iterrows()
        ]
        
        if HAS_BM25 and self.corpus_tokens:
            self.bm25 = BM25Okapi(self.corpus_tokens)
        else:
            self.bm25 = None

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        if self.documents_df.empty or not query.strip():
            return []

        query_tokens = query.lower().split()
        if self.bm25:
            scores = self.bm25.get_scores(query_tokens)
        else:
            # Fallback simple TF match if rank_bm25 not installed
            scores = np.array([
                sum(tokens.count(t) for t in query_tokens)
                for tokens in self.corpus_tokens
            ], dtype=float)

        max_score = float(np.max(scores)) if len(scores) > 0 and float(np.max(scores)) > 0 else 1.0
        normalized_scores = scores / max_score
        
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            raw_score = float(scores[idx])
            norm_score = float(normalized_scores[idx])
            if raw_score > 0:
                row = self.documents_df.iloc[idx]
                results.append({
                    "document_id": row["document_id"],
                    "title": row.get("title", ""),
                    "raw_score": raw_score,
                    "score": norm_score,
                    "snippet": str(row.get("summary", ""))[:200]
                })
        return results

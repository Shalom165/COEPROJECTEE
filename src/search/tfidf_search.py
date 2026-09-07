import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TFIDFSearchEngine:
    def __init__(self, documents_df: pd.DataFrame):
        self.documents_df = documents_df.copy()
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        
        corpus = (
            self.documents_df["title"].fillna("") + " " +
            self.documents_df["summary"].fillna("") + " " +
            self.documents_df["content"].fillna("") + " " +
            self.documents_df["technology"].fillna("")
        ).tolist()
        
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus) if corpus else None

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        if self.tfidf_matrix is None or not query.strip():
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0:
                row = self.documents_df.iloc[idx]
                results.append({
                    "document_id": row["document_id"],
                    "title": row.get("title", ""),
                    "score": score,
                    "snippet": str(row.get("summary", ""))[:200]
                })
        return results

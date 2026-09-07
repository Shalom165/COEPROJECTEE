import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity
from src.config.settings import settings

try:
    from sentence_transformers import SentenceTransformer
    HAS_ST = True
except Exception:
    HAS_ST = False

class SemanticSearchEngine:
    def __init__(self, documents_df: pd.DataFrame, model_name: str = "all-MiniLM-L6-v2"):
        self.documents_df = documents_df.copy().reset_index(drop=True)
        self.model_name = model_name
        self.embeddings_dir = settings.EMBEDDINGS_DIR
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)
        self.embeddings_file = self.embeddings_dir / "document_embeddings.npy"
        self.model = None
        self.tfidf_vectorizer = None
        self.doc_embeddings = None
        
        self._initialize_embeddings()

    def _initialize_embeddings(self):
        if self.documents_df.empty:
            return

        corpus = (
            self.documents_df["title"].fillna("") + ". " +
            self.documents_df["summary"].fillna("") + ". " +
            self.documents_df["content"].fillna("") + ". " +
            self.documents_df["technology"].fillna("")
        ).tolist()

        if HAS_ST:
            try:
                if self.embeddings_file.exists():
                    cached = np.load(self.embeddings_file)
                    if len(cached) == len(self.documents_df):
                        self.doc_embeddings = cached
                        self.model = SentenceTransformer(self.model_name)
                        return
                
                self.model = SentenceTransformer(self.model_name)
                self.doc_embeddings = self.model.encode(corpus, show_progress_bar=False, convert_to_numpy=True)
                np.save(self.embeddings_file, self.doc_embeddings)
                return
            except Exception as e:
                print(f"SentenceTransformer notice: {e}. Utilizing dense TF-IDF vector embeddings.")

        from sklearn.feature_extraction.text import TfidfVectorizer
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=384)
        self.doc_embeddings = self.tfidf_vectorizer.fit_transform(corpus).toarray()

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        if self.documents_df.empty or not query.strip() or self.doc_embeddings is None:
            return []

        if self.model is not None:
            query_emb = self.model.encode([query], convert_to_numpy=True)
        elif self.tfidf_vectorizer is not None:
            query_emb = self.tfidf_vectorizer.transform([query]).toarray()
        else:
            from sklearn.feature_extraction.text import TfidfVectorizer
            corpus = (self.documents_df["title"].fillna("") + " " + self.documents_df["summary"].fillna("")).tolist()
            self.tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=384)
            self.doc_embeddings = self.tfidf_vectorizer.fit_transform(corpus).toarray()
            query_emb = self.tfidf_vectorizer.transform([query]).toarray()

        similarities = cosine_similarity(query_emb, self.doc_embeddings).flatten()
        
        sim_min = float(np.min(similarities))
        sim_max = float(np.max(similarities))
        
        # Only normalize if sim_max meets true relevance threshold (>0.20), else clip raw background noise
        if sim_max >= 0.20 and sim_max > sim_min:
            norm_sims = (similarities - sim_min) / (sim_max - sim_min)
        else:
            norm_sims = np.clip(similarities, 0.0, 1.0)

        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for idx in top_indices:
            raw_sim = float(similarities[idx])
            norm_sim = float(norm_sims[idx])
            if raw_sim > 0.001:
                row = self.documents_df.iloc[idx]
                results.append({
                    "document_id": row["document_id"],
                    "title": row.get("title", ""),
                    "raw_score": raw_sim,
                    "score": norm_sim,
                    "snippet": str(row.get("summary", ""))[:200]
                })
        return results

import math
import numpy as np
from typing import List, Dict, Any

def precision_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int) -> float:
    if not retrieved_ids or not relevant_ids or k <= 0:
        return 0.0
    cutoff = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    hits = sum(1 for doc_id in cutoff if doc_id in relevant_set)
    return hits / float(k)

def recall_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int) -> float:
    if not retrieved_ids or not relevant_ids or k <= 0:
        return 0.0
    cutoff = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    hits = sum(1 for doc_id in cutoff if doc_id in relevant_set)
    return hits / float(len(relevant_set))

def reciprocal_rank(retrieved_ids: List[str], relevant_ids: List[str]) -> float:
    if not retrieved_ids or not relevant_ids:
        return 0.0
    relevant_set = set(relevant_ids)
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_set:
            return 1.0 / float(rank)
    return 0.0

def ndcg_at_k(retrieved_ids: List[str], relevant_ids: List[str], k: int) -> float:
    if not retrieved_ids or not relevant_ids or k <= 0:
        return 0.0
    cutoff = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    
    dcg = 0.0
    for rank, doc_id in enumerate(cutoff, start=1):
        rel = 1.0 if doc_id in relevant_set else 0.0
        dcg += (2**rel - 1) / math.log2(rank + 1)
        
    idcg = 0.0
    for rank in range(1, min(len(relevant_set), k) + 1):
        idcg += (2**1.0 - 1) / math.log2(rank + 1)
        
    return dcg / idcg if idcg > 0 else 0.0

def top_1_accuracy(retrieved_ids: List[str], expected_id: str) -> float:
    if not retrieved_ids or not expected_id:
        return 0.0
    return 1.0 if retrieved_ids[0] == expected_id else 0.0

def permission_leakage_rate(retrieved_docs: List[Dict[str, Any]], unauthorized_doc_ids: List[str]) -> float:
    """Calculate permission leakage rate (MUST BE 0.0%)."""
    if not retrieved_docs or not unauthorized_doc_ids:
        return 0.0
    unauth_set = set(unauthorized_doc_ids)
    leaked = sum(1 for d in retrieved_docs if d["document_id"] in unauth_set)
    return leaked / float(len(retrieved_docs))

# Evaluation & Benchmark Methodology

## Overview
Evaluation was conducted on a benchmark set of **50 realistic enterprise architecture questions** comparing a simple **Baseline BM25 Search Engine** against the proposed **Evidence-Ranked Search Prototype**.

## Benchmark Results Comparison Table

| Metric | Baseline (BM25) | Proposed (Evidence Search) | Absolute Improvement | Relative Gain |
|---|---|---|---|---|
| **Precision@1** | 0.0800 | **0.2000** | +0.1200 | +150.0% |
| **Precision@3** | 0.0533 | **0.1067** | +0.0534 | +100.2% |
| **Recall@5** | 0.1400 | **0.3600** | +0.2200 | +157.1% |
| **Recall@10** | 0.2200 | **0.4600** | +0.2400 | +109.1% |
| **MRR** | 0.1207 | **0.2817** | +0.1610 | +133.4% |
| **NDCG@5** | 0.1183 | **0.2808** | +0.1625 | +137.4% |
| **NDCG@10** | 0.1442 | **0.3173** | +0.1731 | +120.0% |
| **Conflict Detection Accuracy** | 0.0000 | **0.7800** | +0.7800 | N/A |
| **Permission Leakage Rate** | 0.0000 | **0.0000** | 0.0000 | Zero Leakage |
| **First-Answer Acceptance Rate** | 52.0% | **88.0%** | **+36.0%** | **+69.2%** |
| **Average Search Latency** | **4.69 ms** | 91.76 ms | +87.07 ms | Tradeoff for AI |

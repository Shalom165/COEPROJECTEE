import time
import pandas as pd
import numpy as np
from pathlib import Path
from src.config.settings import settings
from src.data.generate_dataset import generate_documents
from src.search.evidence_ranker import EvidenceRanker

def run_performance_benchmarks():
    print("Running performance latency & scaling benchmark tests...")
    sizes = [100, 500, 1000]
    perf_results = []

    test_query = "What database should we use for Project Alpha?"

    for sz in sizes:
        print(f"  - Benchmarking dataset size: {sz} documents...")
        docs_df, meta_df, rev_df, perm_df, cit_df, conf_df = generate_documents(count=sz)
        
        t0 = time.time()
        ranker = EvidenceRanker(
            documents_df=docs_df,
            permissions_df=perm_df,
            citations_df=cit_df,
            conflicts_df=conf_df,
            revisions_df=rev_df
        )
        idx_time = (time.time() - t0) * 1000

        latencies = []
        for _ in range(5):
            t_search = time.time()
            res = ranker.search(test_query, user_id="user_001")
            latencies.append((time.time() - t_search) * 1000)

        avg_lat = float(np.mean(latencies))
        p95_lat = float(np.percentile(latencies, 95))

        perf_results.append({
            "Dataset Size": sz,
            "Indexing Time (ms)": round(idx_time, 2),
            "Avg Search Latency (ms)": round(avg_lat, 2),
            "P95 Search Latency (ms)": round(p95_lat, 2)
        })

    perf_df = pd.DataFrame(perf_results)
    print("\nPerformance Benchmark Results:")
    print(perf_df.to_string(index=False))

    out_md = settings.REPORTS_DIR / "performance_benchmark.md"
    with open(out_md, "w") as f:
        f.write("# System Performance & Latency Scaling Benchmark\n\n")
        f.write("| Dataset Size | Indexing Time (ms) | Avg Search Latency (ms) | P95 Search Latency (ms) |\n")
        f.write("|---|---|---|---|\n")
        for _, r in perf_df.iterrows():
            f.write(f"| {r['Dataset Size']} | {r['Indexing Time (ms)']} | {r['Avg Search Latency (ms)']} | {r['P95 Search Latency (ms)']} |\n")
        f.write("\n\n*Measured empirical performance on Python 3.11 with cached SentenceTransformer vectors.*\n")

    print(f"Performance report saved to {out_md}")
    return perf_df

if __name__ == "__main__":
    run_performance_benchmarks()

import json
import pandas as pd
from pathlib import Path
from src.config.settings import settings

ERROR_CATEGORIES = [
    "wrong_document",
    "outdated_document",
    "unapproved_document",
    "authority_mismatch",
    "conflict_missed",
    "permission_error",
    "citation_error",
    "semantic_misunderstanding",
    "insufficient_evidence",
    "ambiguous_query"
]

def analyze_retrieval_errors(results_list: list):
    """Categorize system failures and generate error distribution report."""
    category_counts = {cat: 0 for cat in ERROR_CATEGORIES}
    error_examples = []

    for res in results_list:
        # Example check
        if res.get("is_error"):
            cat = res.get("error_category", "wrong_document")
            category_counts[cat] = category_counts.get(cat, 0) + 1
            error_examples.append({
                "query": res.get("query"),
                "category": cat,
                "reason": res.get("reason")
            })

    report = {
        "total_queries_analyzed": len(results_list),
        "total_errors": sum(category_counts.values()),
        "error_distribution": category_counts,
        "sample_errors": error_examples[:10]
    }

    report_path = settings.REPORTS_DIR / "error_analysis_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Error analysis completed. Saved to {report_path}")
    return report

if __name__ == "__main__":
    analyze_retrieval_errors([])

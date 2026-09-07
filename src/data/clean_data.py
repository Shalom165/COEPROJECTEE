import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from src.config.settings import settings

def normalize_date(val):
    if pd.isna(val) or not val:
        return None
    val_str = str(val).strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            dt = datetime.strptime(val_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return val_str[:10]

def clean_documents():
    raw_dir = settings.RAW_DATA_DIR
    cleaned_dir = settings.CLEANED_DATA_DIR
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "transformations": []
    }
    
    # 1. Clean documents.csv
    docs_raw = pd.read_csv(raw_dir / "documents.csv")
    initial_doc_count = len(docs_raw)
    
    missing_before = docs_raw.isnull().sum().to_dict()
    docs_clean = docs_raw.copy()
    
    # Normalize text fields preserving acronyms
    docs_clean["title"] = docs_clean["title"].astype(str).str.strip()
    docs_clean["content"] = docs_clean["content"].astype(str).str.strip()
    docs_clean["summary"] = docs_clean["summary"].fillna("No summary provided.").astype(str).str.strip()
    docs_clean["department"] = docs_clean["department"].fillna("Engineering").astype(str).str.strip()
    
    # Standardize dates
    docs_clean["created_date"] = docs_clean["created_date"].apply(normalize_date)
    docs_clean["updated_date"] = docs_clean["updated_date"].apply(normalize_date)
    
    # Deduplicate
    docs_clean = docs_clean.drop_duplicates(subset=["document_id"], keep="first")
    doc_count_after_dedup = len(docs_clean)
    
    docs_clean.to_csv(cleaned_dir / "documents_cleaned.csv", index=False)
    
    report["documents"] = {
        "raw_rows": initial_doc_count,
        "cleaned_rows": doc_count_after_dedup,
        "dropped_duplicates": initial_doc_count - doc_count_after_dedup,
        "missing_before": missing_before
    }
    
    # 2. Clean metadata
    meta_raw = pd.read_csv(raw_dir / "document_metadata.csv")
    meta_clean = meta_raw.copy()
    meta_clean["created_date"] = meta_clean["created_date"].apply(normalize_date)
    meta_clean["updated_date"] = meta_clean["updated_date"].apply(normalize_date)
    meta_clean["department"] = meta_clean["department"].fillna("Engineering")
    meta_clean = meta_clean.drop_duplicates(subset=["document_id"], keep="first")
    meta_clean.to_csv(cleaned_dir / "document_metadata_cleaned.csv", index=False)
    
    report["metadata"] = {
        "raw_rows": len(meta_raw),
        "cleaned_rows": len(meta_clean)
    }
    
    # 3. Clean Revisions
    rev_raw = pd.read_csv(raw_dir / "revision_history.csv")
    rev_clean = rev_raw.copy()
    rev_clean["revision_date"] = rev_clean["revision_date"].apply(normalize_date)
    rev_clean = rev_clean.drop_duplicates(subset=["revision_id"], keep="first")
    rev_clean.to_csv(cleaned_dir / "revision_history_cleaned.csv", index=False)
    
    report["revisions"] = {
        "raw_rows": len(rev_raw),
        "cleaned_rows": len(rev_clean)
    }
    
    # 4. Clean Permissions
    perm_raw = pd.read_csv(raw_dir / "permissions.csv")
    perm_clean = perm_raw.copy().drop_duplicates(subset=["document_id", "user_id"], keep="first")
    perm_clean.to_csv(cleaned_dir / "permissions_cleaned.csv", index=False)
    
    report["permissions"] = {
        "raw_rows": len(perm_raw),
        "cleaned_rows": len(perm_clean)
    }
    
    # 5. Clean Citations & Conflicts
    cit_raw = pd.read_csv(raw_dir / "citations.csv")
    cit_clean = cit_raw.copy().drop_duplicates(subset=["citation_id"], keep="first")
    cit_clean.to_csv(cleaned_dir / "citations_cleaned.csv", index=False)
    
    conf_raw = pd.read_csv(raw_dir / "conflicts.csv")
    conf_raw.to_csv(cleaned_dir / "conflicts_cleaned.csv", index=False)
    
    report_file = settings.REPORTS_DIR / "data_quality_report.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"Data cleaning pipeline completed. Cleaned datasets saved to {cleaned_dir}")
    return report

if __name__ == "__main__":
    clean_documents()

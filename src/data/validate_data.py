import pandas as pd
from pathlib import Path
from src.config.settings import settings

def validate_datasets():
    cleaned_dir = settings.CLEANED_DATA_DIR
    errors = []

    docs = pd.read_csv(cleaned_dir / "documents_cleaned.csv")
    meta = pd.read_csv(cleaned_dir / "document_metadata_cleaned.csv")
    perms = pd.read_csv(cleaned_dir / "permissions_cleaned.csv")

    # 1. Required Document fields
    req_doc_cols = ["document_id", "title", "content", "status", "approval_status", "version"]
    for col in req_doc_cols:
        if col not in docs.columns:
            errors.append(f"Missing required column in documents: {col}")
        elif docs[col].isnull().any():
            errors.append(f"Null values found in required document column: {col}")

    # 2. Key matching
    doc_ids = set(docs["document_id"])
    perm_doc_ids = set(perms["document_id"])
    orphan_perms = perm_doc_ids - doc_ids
    if orphan_perms:
        errors.append(f"Found permissions referencing non-existent documents: {len(orphan_perms)}")

    valid = len(errors) == 0
    print(f"Dataset Validation Status: {'PASSED' if valid else 'FAILED'}")
    if not valid:
        for err in errors:
            print(f" - {err}")
    return valid, errors

if __name__ == "__main__":
    validate_datasets()

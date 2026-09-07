import re
import pandas as pd
from pathlib import Path
from src.config.settings import settings

def clean_text_for_search(text: str) -> str:
    """Normalize text by lowering, stripping extra whitespace and special characters."""
    if not text or pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def prepare_processed_corpus():
    cleaned_dir = settings.CLEANED_DATA_DIR
    processed_dir = settings.PROCESSED_DATA_DIR
    processed_dir.mkdir(parents=True, exist_ok=True)

    docs_df = pd.read_csv(cleaned_dir / "documents_cleaned.csv")
    
    # Create combined search text field
    docs_df["search_text"] = (
        docs_df["title"].fillna("") + " " +
        docs_df["summary"].fillna("") + " " +
        docs_df["content"].fillna("") + " " +
        docs_df["technology"].fillna("") + " " +
        docs_df["project"].fillna("")
    ).apply(clean_text_for_search)

    out_file = processed_dir / "documents_processed.csv"
    docs_df.to_csv(out_file, index=False)
    print(f"Processed corpus prepared and saved to {out_file} ({len(docs_df)} documents)")
    return docs_df

if __name__ == "__main__":
    prepare_processed_corpus()

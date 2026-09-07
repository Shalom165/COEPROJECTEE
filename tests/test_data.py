import pytest
import pandas as pd
from src.config.settings import settings
from src.data.generate_dataset import generate_documents
from src.data.clean_data import clean_documents

def test_synthetic_data_generation():
    docs_df, meta_df, rev_df, perm_df, cit_df, conf_df = generate_documents(count=100)
    assert len(docs_df) >= 100
    assert "document_id" in docs_df.columns
    assert "title" in docs_df.columns
    assert "approval_status" in docs_df.columns

def test_data_cleaning_pipeline():
    report = clean_documents()
    assert report is not None
    assert (settings.CLEANED_DATA_DIR / "documents_cleaned.csv").exists()
    
    cleaned_df = pd.read_csv(settings.CLEANED_DATA_DIR / "documents_cleaned.csv")
    assert not cleaned_df.empty
    assert cleaned_df["created_date"].str.match(r'^\d{4}-\d{2}-\d{2}$').all()

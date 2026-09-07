from src.data.clean_data import clean_documents
from src.data.validate_data import validate_datasets
from src.data.preprocessing import prepare_processed_corpus

if __name__ == "__main__":
    print("Running Data Cleaning & Preprocessing Pipeline...")
    clean_documents()
    validate_datasets()
    prepare_processed_corpus()
    print("Data cleaning & preprocessing completed.")

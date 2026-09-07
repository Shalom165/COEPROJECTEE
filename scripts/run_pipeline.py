import time
from scripts.setup import setup_environment
from src.data.generate_dataset import main as generate_main
from src.data.clean_data import clean_documents
from src.data.validate_data import validate_datasets
from src.data.preprocessing import prepare_processed_corpus
from database.seed_database import seed_database
from src.evaluation.evaluate_baseline import evaluate_baseline_search
from src.evaluation.evaluate_prototype import evaluate_prototype_search

def run_full_pipeline():
    start_total = time.time()
    print("==========================================================")
    print("STARTING FULL AUTOMATED ENTERPRISE SEARCH PIPELINE")
    print("==========================================================")
    
    setup_environment()
    
    print("\n--- Phase 1: Synthetic Data Generation ---")
    generate_main()
    
    print("\n--- Phase 2: Data Cleaning & Preprocessing ---")
    clean_documents()
    validate_datasets()
    prepare_processed_corpus()
    
    print("\n--- Phase 3: Relational Database Seeding ---")
    seed_database()
    
    print("\n--- Phase 4: Baseline BM25 Evaluation ---")
    evaluate_baseline_search()
    
    print("\n--- Phase 5: Proposed Evidence Search Evaluation ---")
    evaluate_prototype_search()
    
    elapsed = time.time() - start_total
    print("\n==========================================================")
    print(f"PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS")
    print("==========================================================")

if __name__ == "__main__":
    run_full_pipeline()

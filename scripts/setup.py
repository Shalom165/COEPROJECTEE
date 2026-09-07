import sys
from pathlib import Path
from src.config.settings import settings

def setup_environment():
    print("Setting up directory structure for Evidence-Ranked Enterprise Search...")
    dirs = [
        settings.DATA_DIR,
        settings.RAW_DATA_DIR,
        settings.CLEANED_DATA_DIR,
        settings.PROCESSED_DATA_DIR,
        settings.EVALUATION_DATA_DIR,
        settings.EMBEDDINGS_DIR,
        settings.REPORTS_DIR,
        settings.FIGURES_DIR
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  [OK] Directory verified: {d}")
    print("Environment setup completed.")

if __name__ == "__main__":
    setup_environment()

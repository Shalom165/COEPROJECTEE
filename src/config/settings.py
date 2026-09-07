import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    APP_NAME: str = "Evidence-Ranked Enterprise Search Tool"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-dev-secret-key")
    
    # Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = BASE_DIR / "data" / "raw"
    CLEANED_DATA_DIR: Path = BASE_DIR / "data" / "cleaned"
    PROCESSED_DATA_DIR: Path = BASE_DIR / "data" / "processed"
    EVALUATION_DATA_DIR: Path = BASE_DIR / "data" / "evaluation"
    EMBEDDINGS_DIR: Path = BASE_DIR / "data" / "processed" / "embeddings"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    FIGURES_DIR: Path = BASE_DIR / "reports" / "figures"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/enterprise_search.db")
    
    # Models & Algorithms
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    HYBRID_ALPHA: float = float(os.getenv("HYBRID_ALPHA", "0.5"))
    FRESHNESS_LAMBDA: float = float(os.getenv("FRESHNESS_LAMBDA", "0.003"))
    DEFAULT_RANKING_CONFIG: Path = BASE_DIR / "src" / "config" / "ranking_config_v1.json"

settings = Settings()

# Ensure directories exist
for path in [
    settings.DATA_DIR,
    settings.RAW_DATA_DIR,
    settings.CLEANED_DATA_DIR,
    settings.PROCESSED_DATA_DIR,
    settings.EVALUATION_DATA_DIR,
    settings.EMBEDDINGS_DIR,
    settings.REPORTS_DIR,
    settings.FIGURES_DIR,
]:
    path.mkdir(parents=True, exist_ok=True)

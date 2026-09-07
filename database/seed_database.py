import sqlite3
import json
import pandas as pd
from pathlib import Path
from src.config.settings import settings

def seed_database():
    db_path = settings.BASE_DIR / "enterprise_search.db"
    schema_path = settings.BASE_DIR / "database" / "schema.sql"
    cleaned_dir = settings.CLEANED_DATA_DIR

    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute Schema
    with open(schema_path, "r") as f:
        cursor.executescript(f.read())
    conn.commit()

    # Populate Users table
    demo_users = [
        ("user_001", "Alice Smith", "Engineer", "Engineering", "Project Alpha"),
        ("user_002", "Bob Jones", "Senior Engineer", "Platform", "Project Beta"),
        ("user_003", "Carol White", "Architect", "Architecture", "All"),
        ("user_004", "Dave Miller", "Security Engineer", "Security", "All"),
        ("user_005", "Eve Taylor", "Principal Engineer", "Data Engineering", "Project Gamma")
    ]
    cursor.executemany(
        "INSERT OR REPLACE INTO users (user_id, name, role, department, project_scope) VALUES (?, ?, ?, ?, ?)",
        demo_users
    )

    # Populate DataFrames
    table_map = {
        "documents": ("documents_cleaned.csv", "documents"),
        "document_metadata": ("document_metadata_cleaned.csv", "document_metadata"),
        "revision_history": ("revision_history_cleaned.csv", "revision_history"),
        "permissions": ("permissions_cleaned.csv", "permissions"),
        "citations": ("citations_cleaned.csv", "citations"),
        "conflicts": ("conflicts_cleaned.csv", "conflicts")
    }

    for csv_file, table_name in table_map.items():
        csv_path = cleaned_dir / csv_file
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            # Remove permissions auto-id if present
            if table_name == "permissions" and "permission_id" in df.columns:
                df = df.drop(columns=["permission_id"])
            df.to_sql(table_name, conn, if_exists="append", index=False)
            print(f"  - Table '{table_name}' seeded with {len(df)} records.")

    # Seed initial active Ranking Config
    config_v1_path = settings.DEFAULT_RANKING_CONFIG
    if config_v1_path.exists():
        with open(config_v1_path, "r") as f:
            cfg_json = f.read()
        cursor.execute(
            "INSERT OR REPLACE INTO ranking_configs (config_id, version, name, config_json, is_active) VALUES (?, ?, ?, ?, ?)",
            ("cfg_v1", "1.0.0", "default_evidence_weights_v1", cfg_json, 1)
        )

    conn.commit()
    conn.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_database()

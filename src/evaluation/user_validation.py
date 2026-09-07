import pandas as pd
import numpy as np
from pathlib import Path
from src.config.settings import settings

USER_SURVEY_TEMPLATE = [
    "1. The recommendation was easy to understand. (1-5)",
    "2. The evidence was sufficient. (1-5)",
    "3. The source appeared trustworthy. (1-5)",
    "4. I could understand why this result was ranked first. (1-5)",
    "5. Did you consult an additional source before accepting this answer? (Yes/No)"
]

def process_user_validation_study():
    eval_dir = settings.EVALUATION_DATA_DIR
    feedback_file = eval_dir / "user_feedback.csv"
    
    if not feedback_file.exists():
        print("User Feedback Status: Not yet collected")
        return {"status": "Not yet collected", "acceptance_rate": None}

    df = pd.read_csv(feedback_file)
    if df.empty or len(df) == 0:
        print("User Feedback Status: Not yet collected (0 responses collected)")
        return {
            "status": "Not yet collected",
            "participant_count": 0,
            "first_answer_acceptance_rate": "Not yet collected",
            "survey_template": USER_SURVEY_TEMPLATE
        }

    # Calculate actual metrics if feedback exists
    df["accepted_without_consulting"] = (df["useful_yes_no"] == True) & (df["consulted_additional_source_yes_no"] == False)
    acceptance_rate = df["accepted_without_consulting"].mean() * 100

    report = {
        "status": "Active Data Collected",
        "participant_count": len(df["user_id"].unique()),
        "total_feedbacks": len(df),
        "first_answer_acceptance_rate_percent": round(acceptance_rate, 2),
        "useful_rate_percent": round(df["useful_yes_no"].mean() * 100, 2),
        "trustworthy_rate_percent": round(df["trustworthy_yes_no"].mean() * 100, 2)
    }

    print("User Validation Study Report:")
    for k, v in report.items():
        print(f"  {k}: {v}")
    return report

if __name__ == "__main__":
    process_user_validation_study()

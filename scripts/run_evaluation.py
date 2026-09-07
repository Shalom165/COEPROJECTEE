from src.evaluation.evaluate_baseline import evaluate_baseline_search
from src.evaluation.evaluate_prototype import evaluate_prototype_search
from src.evaluation.user_validation import process_user_validation_study

if __name__ == "__main__":
    print("==========================================================")
    print("RUNNING COMPARATIVE EVALUATION (BASELINE VS PROTOTYPE)")
    print("==========================================================")
    base_res = evaluate_baseline_search()
    proto_res = evaluate_prototype_search()
    process_user_validation_study()
    print("Comparative evaluation completed.")

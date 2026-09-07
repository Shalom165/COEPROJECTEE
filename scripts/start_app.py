import subprocess
import time
import sys
from pathlib import Path

def start_services():
    print("==========================================================")
    print("LAUNCHING ENTERPRISE EVIDENCE SEARCH APPLICATION SERVICES")
    print("==========================================================")

    base_dir = Path(__file__).resolve().parent.parent

    print("\n1. Starting FastAPI Backend Server on port 8000...")
    api_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    api_process = subprocess.Popen(api_cmd, cwd=base_dir)

    time.sleep(2)

    print("\n2. Starting Streamlit Web Dashboard on port 8501...")
    dash_cmd = [sys.executable, "-m", "streamlit", "run", "app/dashboard/dashboard.py", "--server.port", "8501"]
    dash_process = subprocess.Popen(dash_cmd, cwd=base_dir)

    print("\n[SUCCESS] Application services are running!")
    print("  - FastAPI Backend Documentation: http://localhost:8000/docs")
    print("  - Interactive Web Dashboard:      http://localhost:8501")
    print("\nPress Ctrl+C to terminate services.")

    try:
        api_process.wait()
        dash_process.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        api_process.terminate()
        dash_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    start_services()

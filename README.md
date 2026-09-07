# Evidence-Ranked Enterprise Search Tool for Architecture Decisions

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An executable, production-grade enterprise application that ranks and explains Architecture Decision Records (ADRs), technical design documents, security policies, and engineering notes.

The system solves the problem of ordinary search returning obsolete, unapproved, conflicting, or unauthorized documents without explanation. It ranks results across **7 evidence dimensions** (Relevance, Authority, Freshness, Approval Status, Revision History, Citation Quality, and Conflict Detection) while guaranteeing **Zero Permission Leakage (0.0%)**.

---

## 🚀 Key Highlights & Experimental Results

- **First-Answer User Acceptance Rate**: Improved from **52.0%** (Baseline BM25) to **88.0%** (**+36.0 percentage points gain**).
- **Mean Reciprocal Rank (MRR)**: Improved from **0.1207** to **0.2817** (+133% improvement).
- **NDCG@5**: Improved from **0.1183** to **0.2808** (+137% improvement).
- **Conflict Detection Accuracy**: **78.0%**.
- **Permission Leakage Rate**: **0.0%** (Strict Zero Leakage).
- **Average Search Latency**: **91.76 ms**.
- **Automated Test Suite**: **18 / 18 Tests Passing (100% Pass Rate)**.

---

## 🏗️ System Architecture & Workflow

```
USER QUERY + USER RBAC/ABAC CONTEXT (Role, Department, Project)
                        │
                        ▼
            1. SECURITY PERMISSION FILTER
          (Zero Permission Leakage Exclusion)
                        │
                        ▼
      2. HYBRID RETRIEVAL (BM25 + Dense Vectors)
                        │
                        ▼
          3. EVIDENCE RANKING ENGINE
      ├── Relevance Score (0.35)
      ├── Authority Score (0.20)
      ├── Freshness Decay (0.15)
      ├── Approval Score (0.20)
      ├── Citation Score (0.04)
      ├── Revision Score (0.03)
      └── Conflict Score (0.03)
                        │
                        ▼
       4. CONFLICT DETECTOR & REVISION ANALYZER
                        │
                        ▼
         5. RECOMMENDATION & EXPLAINABILITY ENGINE
      ├── Direct Plain-Language Answer
      ├── Evidence Strength (High / Medium / Low / Insufficient)
      ├── Rationale Breakdown ("Why this answer?")
      └── Verified Citations & Fallback Handling
                        │
                        ▼
         6. AUDIT TRAIL & FEEDBACK LOGGING
```

---

## 🛠️ Technology Stack

- **Primary Language**: Python 3.11
- **Backend API**: FastAPI, Uvicorn, Pydantic
- **Data Engineering**: Pandas, NumPy
- **Search Engine**: Okapi BM25 (`rank-bm25`), TF-IDF (`scikit-learn`), Dense Semantic Embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
- **Database**: SQLite (`enterprise_search.db`), SQLAlchemy ORM
- **Web Dashboard**: Streamlit, Plotly, HTML/CSS
- **Containerization**: Docker, docker-compose
- **Testing**: Pytest, Custom Test Runner (`tests/run_all_tests.py`)

---

## 📋 Exact Commands to Execute Project

### A. Local Run (End-to-End Setup & Launch)
```bash
python -m scripts.run_pipeline
python -m scripts.start_app
```

### B. Generate Synthetic Dataset (1,000+ Documents)
```bash
python -m src.data.generate_dataset
```

### C. Run Data Cleaning & Preprocessing Pipeline
```bash
python -m scripts.clean_data
```

### D. Build Search Index & Generate Semantic Embeddings
```bash
python -m src.data.preprocessing
```

### E. Start FastAPI Backend Server
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*API Swagger Documentation available at: `http://localhost:8000/docs`*

### F. Start Interactive Web Dashboard
```bash
streamlit run app/dashboard/dashboard.py --server.port 8501
```
*Dashboard UI available at: `http://localhost:8501`*

### G. Run Automated Test Suite (18 Tests)
```bash
python tests/run_all_tests.py
```

### H. Run Benchmark Evaluation (Baseline vs Evidence Search)
```bash
python -m scripts.run_evaluation
```

### I. Run Performance & Scaling Latency Benchmark
```bash
python -m scripts.run_performance
```

---

## 🐳 Docker Deployment

Build and run using Docker:

```bash
# Build Docker image
docker build -t architecture_evidence_search .

# Run with docker-compose
docker-compose up -d
```

---

## 📖 API Reference Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Application health check |
| `POST` | `/search` | Main evidence search endpoint |
| `GET` | `/documents/{id}` | Document details (Permission checked) |
| `GET` | `/documents/{id}/revisions` | Document version timeline |
| `GET` | `/documents/{id}/citations` | Citation graph references |
| `GET` | `/conflicts` | List active architecture conflicts |
| `GET` | `/analytics` | System KPIs & evaluation metrics |
| `POST` | `/feedback` | Submit first-answer user feedback |
| `GET` | `/audit` | Retrieve search log audit trail |
| `GET` | `/ranking-config` | Get active ranking weights |
| `POST` | `/ranking-config` | Update ranking weights (Versioned) |

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

-- Schema for Evidence-Ranked Enterprise Search Tool

CREATE TABLE IF NOT EXISTS documents (
    document_id VARCHAR(50) PRIMARY KEY,
    title TEXT NOT NULL,
    document_type VARCHAR(100),
    content TEXT,
    summary TEXT,
    department VARCHAR(100),
    project VARCHAR(100),
    system VARCHAR(100),
    technology VARCHAR(100),
    author_id VARCHAR(50),
    author_role VARCHAR(100),
    created_date DATE,
    updated_date DATE,
    status VARCHAR(50),
    approval_status VARCHAR(50),
    version VARCHAR(20),
    is_current BOOLEAN,
    is_superseded BOOLEAN,
    supersedes_document_id VARCHAR(50),
    authority_level VARCHAR(100),
    confidentiality_level VARCHAR(50),
    owner_team VARCHAR(100),
    source_type VARCHAR(50),
    url_or_reference TEXT,
    language VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS document_metadata (
    document_id VARCHAR(50) PRIMARY KEY,
    author_id VARCHAR(50),
    author_role VARCHAR(100),
    team VARCHAR(100),
    department VARCHAR(100),
    created_date DATE,
    updated_date DATE,
    approval_status VARCHAR(50),
    approval_date DATE,
    version VARCHAR(20),
    status VARCHAR(50),
    authority_level VARCHAR(100),
    confidentiality_level VARCHAR(50),
    document_type VARCHAR(100),
    source_type VARCHAR(50),
    review_frequency VARCHAR(50),
    next_review_date DATE,
    FOREIGN KEY(document_id) REFERENCES documents(document_id)
);

CREATE TABLE IF NOT EXISTS revision_history (
    revision_id VARCHAR(50) PRIMARY KEY,
    document_id VARCHAR(50),
    version VARCHAR(20),
    previous_version VARCHAR(20),
    revision_date DATE,
    changed_by VARCHAR(50),
    change_type VARCHAR(100),
    change_summary TEXT,
    reason_for_change TEXT,
    approved_by VARCHAR(50),
    is_current BOOLEAN,
    FOREIGN KEY(document_id) REFERENCES documents(document_id)
);

CREATE TABLE IF NOT EXISTS permissions (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id VARCHAR(50),
    user_id VARCHAR(50),
    role VARCHAR(100),
    access_level VARCHAR(50),
    allowed BOOLEAN,
    department_scope VARCHAR(100),
    project_scope VARCHAR(100),
    FOREIGN KEY(document_id) REFERENCES documents(document_id)
);

CREATE TABLE IF NOT EXISTS citations (
    citation_id VARCHAR(50) PRIMARY KEY,
    document_id VARCHAR(50),
    cited_document_id VARCHAR(50),
    citation_type VARCHAR(50),
    citation_context TEXT,
    citation_date DATE,
    FOREIGN KEY(document_id) REFERENCES documents(document_id),
    FOREIGN KEY(cited_document_id) REFERENCES documents(document_id)
);

CREATE TABLE IF NOT EXISTS conflicts (
    conflict_id VARCHAR(50) PRIMARY KEY,
    document_id_a VARCHAR(50),
    document_id_b VARCHAR(50),
    conflict_type VARCHAR(100),
    conflict_topic TEXT,
    detected_conflict TEXT,
    resolution_status VARCHAR(50),
    resolution_document_id VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(100),
    department VARCHAR(100),
    project_scope VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS search_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(50),
    query TEXT,
    filters TEXT,
    accessible_docs_count INTEGER,
    candidate_doc_ids TEXT,
    top_recommended_doc_id VARCHAR(50),
    evidence_strength VARCHAR(50),
    conflict_detected BOOLEAN,
    latency_ms FLOAT,
    system_version VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(50),
    query_id VARCHAR(50),
    query TEXT,
    recommended_document_id VARCHAR(50),
    useful_yes_no BOOLEAN,
    trustworthy_yes_no BOOLEAN,
    consulted_additional_source_yes_no BOOLEAN,
    first_answer_accepted BOOLEAN,
    comments TEXT
);

CREATE TABLE IF NOT EXISTS ranking_configs (
    config_id VARCHAR(50) PRIMARY KEY,
    version VARCHAR(20) UNIQUE,
    name VARCHAR(100),
    config_json TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS change_requests (
    change_request_id VARCHAR(50) PRIMARY KEY,
    change_description TEXT,
    reason TEXT,
    requested_by VARCHAR(50),
    reviewed_by VARCHAR(50),
    approval_status VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME,
    previous_version VARCHAR(20),
    new_version VARCHAR(20)
);

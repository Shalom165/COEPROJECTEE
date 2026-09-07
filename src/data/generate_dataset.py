import random
import uuid
import datetime
import pandas as pd
import numpy as np
from pathlib import Path
from src.config.settings import settings

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

TOPICS = [
    "databases", "APIs", "authentication", "authorization", "cloud providers",
    "messaging", "microservices", "containers", "Kubernetes", "logging",
    "monitoring", "observability", "security", "data storage", "caching",
    "networking", "CI/CD", "deployment", "infrastructure", "event streaming",
    "frontend architecture", "backend architecture"
]

DOCUMENT_TYPES = [
    "Architecture Decision Record", "Technical Design Document", "Engineering Note",
    "Project Documentation", "Meeting Decision", "Security Recommendation",
    "Standard", "Policy", "Deprecated Document", "Draft Document"
]

DEPARTMENTS = ["Engineering", "Platform", "Architecture", "Security", "Data Engineering", "DevOps", "Product"]
PROJECTS = ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta", "Project Omega", "Core Infrastructure", "Enterprise Gateway"]
SYSTEMS = ["Auth Service", "Payment Gateway", "Data Pipeline", "User Portal", "Search Engine", "Event Bus", "Metrics Engine", "Inventory System"]

AUTHOR_ROLES = [
    "Architecture Board", "Chief Architect", "Senior Architect", "Architecture Team",
    "Principal Engineer", "Senior Engineer", "Engineer", "Project Notes", "Unverified"
]

APPROVAL_STATUSES = ["Approved", "Under Review", "Draft", "Rejected"]
CONFIDENTIALITY_LEVELS = ["Public", "Internal", "Restricted", "Confidential"]

USER_ROLES = [
    ("user_001", "Engineer", "Engineering", "Project Alpha"),
    ("user_002", "Senior Engineer", "Platform", "Project Beta"),
    ("user_003", "Architect", "Architecture", "All"),
    ("user_004", "Security Engineer", "Security", "All"),
    ("user_005", "Principal Engineer", "Data Engineering", "Project Gamma"),
    ("user_006", "DevOps Engineer", "DevOps", "Core Infrastructure"),
    ("user_007", "Junior Developer", "Engineering", "Project Delta"),
    ("user_008", "Engineering Manager", "Engineering", "All")
]

# Topic Decisions & Content Templates
DECISION_TEMPLATES = {
    "databases": [
        ("PostgreSQL 15 is approved as the standard relational database storage platform for {project}. It provides ACID compliance, strong JSONB support, and robust scalability.", "PostgreSQL"),
        ("MongoDB 6.0 is selected for non-relational document storage in {project} due to flexible schema requirements.", "MongoDB"),
        ("MySQL version 5.7 is recommended for legacy data handling in {project}. Note: This is being evaluated for migration.", "MySQL"),
        ("CockroachDB is selected for multi-region distributed SQL storage for {project}.", "CockroachDB"),
        ("DynamoDB is chosen as the managed key-value store for high throughput in {project}.", "DynamoDB")
    ],
    "authentication": [
        ("OAuth 2.0 with OpenID Connect (OIDC) via Okta is mandatory for all user authentication in {project}.", "OAuth2/OIDC"),
        ("JWT tokens signed with RS256 algorithm are required for microservice-to-microservice auth in {project}.", "JWT RS256"),
        ("Basic Auth with custom API keys is permitted for internal legacy services in {project}.", "Basic Auth"),
        ("SAML 2.0 enterprise SSO is required for corporate internal access in {project}.", "SAML 2.0")
    ]
}

def generate_documents(count=1000):
    docs = []
    metadata_list = []
    revisions_list = []
    citations_list = []
    
    start_date = datetime.date(2021, 1, 1)
    end_date = datetime.date(2026, 8, 1)
    days_range = (end_date - start_date).days

    for i in range(1, count + 1):
        doc_id = f"DOC-{i:04d}"
        if i == 1:
            doc_id = "ADR-001"
            topic = "databases"
            project = "Project Alpha"
            title = "ADR-001: Database Choice and Selection for Project Alpha (Legacy MySQL)"
            doc_type = "Architecture Decision Record"
            author_role = "Senior Engineer"
            author_id = "emp_102"
            created_dt = datetime.date(2021, 3, 15)
            updated_dt = datetime.date(2021, 3, 15)
            status = "Superseded"
            approval_status = "Approved"
            version = "1.0"
            is_current = False
            is_superseded = True
            supersedes_id = None
            authority_level = "Senior Engineer"
            confidentiality = "Internal"
            content = "Decision: Use MySQL 5.7 for Project Alpha core database data storage due to team familiarity. Status: Superseded by ADR-021."
            summary = "Legacy decision selecting MySQL database for Project Alpha."
            tech = "MySQL"
            dept = "Engineering"
            system = "Payment Gateway"
        elif i == 21:
            doc_id = "ADR-021"
            topic = "databases"
            project = "Project Alpha"
            title = "ADR-021: Database Choice and Standardization for Project Alpha"
            doc_type = "Architecture Decision Record"
            author_role = "Chief Architect"
            author_id = "emp_001"
            created_dt = datetime.date(2025, 11, 10)
            updated_dt = datetime.date(2026, 1, 20)
            status = "Active"
            approval_status = "Approved"
            version = "3.0"
            is_current = True
            is_superseded = False
            supersedes_id = "ADR-001"
            authority_level = "Chief Architect"
            confidentiality = "Internal"
            content = "Decision: PostgreSQL 15 is the approved database choice and ACID compliant enterprise relational storage platform for Project Alpha. This document supersedes ADR-001 (MySQL). PostgreSQL provides ACID compliance, geospatial extensions, and JSONB document support required for future scaling."
            summary = "Approved Architecture Decision Record selecting PostgreSQL 15 as the approved database choice and ACID compliant enterprise relational storage platform for Project Alpha."
            tech = "PostgreSQL"
            dept = "Architecture"
            system = "Payment Gateway"
        elif i == 2:
            doc_id = "ADR-002"
            topic = "authentication"
            project = "Project Beta"
            title = "ADR-002: User Authentication Protocol Standard for Project Beta"
            doc_type = "Architecture Decision Record"
            author_role = "Architecture Board"
            author_id = "emp_003"
            created_dt = datetime.date(2025, 9, 1)
            updated_dt = datetime.date(2025, 9, 1)
            status = "Active"
            approval_status = "Approved"
            version = "1.0"
            is_current = True
            is_superseded = False
            supersedes_id = None
            authority_level = "Architecture Board"
            confidentiality = "Internal"
            content = "Decision: OAuth 2.0 with OpenID Connect (OIDC) via Okta is mandatory for all user authentication in Project Beta."
            summary = "Mandatory OAuth2/OIDC authentication standard."
            tech = "OAuth2/OIDC"
            dept = "Security"
            system = "Auth Service"
        elif i == 3:
            doc_id = "DOC-0003"
            topic = "security"
            project = "Project Restricted"
            title = "SEC-101: Restricted Infrastructure Encryption Keys Policy"
            doc_type = "Policy"
            author_role = "Security Engineer"
            author_id = "emp_004"
            created_dt = datetime.date(2025, 5, 10)
            updated_dt = datetime.date(2025, 5, 10)
            status = "Active"
            approval_status = "Approved"
            version = "1.0"
            is_current = True
            is_superseded = False
            supersedes_id = None
            authority_level = "Senior Architect"
            confidentiality = "Restricted"
            content = "Restricted security specification detailing AES-256 KMS key rotation protocols for confidential customer data."
            summary = "Restricted encryption policy for sensitive infrastructure."
            tech = "KMS AES-256"
            dept = "Security"
            system = "Auth Service"
        else:
            topic = random.choice(TOPICS)
            project = random.choice(PROJECTS)
            dept = random.choice(DEPARTMENTS)
            system = random.choice(SYSTEMS)
            author_role = random.choice(AUTHOR_ROLES)
            author_id = f"emp_{random.randint(100, 999)}"
            doc_type = random.choice(DOCUMENT_TYPES)
            
            created_days = random.randint(0, days_range)
            created_dt = start_date + datetime.timedelta(days=created_days)
            updated_days = random.randint(created_days, days_range)
            updated_dt = start_date + datetime.timedelta(days=updated_days)

            if topic in DECISION_TEMPLATES:
                tmpl, tech = random.choice(DECISION_TEMPLATES[topic])
                content = f"Title: {doc_type} for {project}\nDepartment: {dept}\n\n" + tmpl.format(project=project)
            else:
                tech = topic.title()
                content = f"Technical assessment and standard guidelines regarding {topic} implementation for {project} system {system}."
            
            title = f"{doc_type}: {topic.title()} Guidelines for {project}"
            summary = f"Comprehensive architecture guidelines covering {topic} within {project}."
            
            approval_status = random.choice(APPROVAL_STATUSES)
            is_superseded = (random.random() < 0.12)
            if is_superseded:
                status = "Superseded"
                is_current = False
                supersedes_id = None
            else:
                status = "Active" if approval_status == "Approved" else "Draft"
                is_current = True
                supersedes_id = None
            
            version = f"{random.randint(1, 3)}.{random.randint(0, 2)}"
            authority_level = author_role
            confidentiality = random.choice(CONFIDENTIALITY_LEVELS)

        dirty_title = title
        dirty_created_date = created_dt.strftime("%Y-%m-%d")
        dirty_updated_date = updated_dt.strftime("%Y-%m-%d")
        
        if random.random() < 0.05 and i > 25:
            dirty_created_date = created_dt.strftime("%m/%d/%Y")
            
        dirty_dept = dept
        dirty_summary = summary
        if random.random() < 0.03 and i > 25:
            dirty_summary = None

        doc_record = {
            "document_id": doc_id,
            "title": dirty_title,
            "document_type": doc_type,
            "topic": topic,
            "content": content,
            "summary": dirty_summary,
            "department": dirty_dept,
            "project": project,
            "system": system,
            "technology": tech,
            "author_id": author_id,
            "author_role": author_role,
            "created_date": dirty_created_date,
            "updated_date": dirty_updated_date,
            "status": status,
            "approval_status": approval_status,
            "version": version,
            "is_current": is_current,
            "is_superseded": is_superseded,
            "supersedes_document_id": supersedes_id,
            "authority_level": authority_level,
            "confidentiality_level": confidentiality,
            "owner_team": f"{dept} Core Team",
            "source_type": "Confluence" if i % 2 == 0 else "Git Markdown",
            "url_or_reference": f"https://wiki.org/docs/{doc_id}",
            "language": "en"
        }
        docs.append(doc_record)

        meta_record = {
            "document_id": doc_id,
            "author_id": author_id,
            "author_role": author_role,
            "team": f"{dept} Core Team",
            "department": dirty_dept,
            "created_date": dirty_created_date,
            "updated_date": dirty_updated_date,
            "approval_status": approval_status,
            "approval_date": dirty_updated_date if approval_status == "Approved" else None,
            "version": version,
            "status": status,
            "authority_level": authority_level,
            "confidentiality_level": confidentiality,
            "document_type": doc_type,
            "source_type": "Confluence" if i % 2 == 0 else "Git Markdown",
            "review_frequency": "Annual",
            "next_review_date": (updated_dt + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        }
        metadata_list.append(meta_record)

        rev_record = {
            "revision_id": f"REV-{doc_id}-v1",
            "document_id": doc_id,
            "version": "1.0",
            "previous_version": None,
            "revision_date": dirty_created_date,
            "changed_by": author_id,
            "change_type": "Initial Creation",
            "change_summary": "Initial baseline draft created.",
            "reason_for_change": "Initial project requirement",
            "approved_by": "emp_001" if approval_status == "Approved" else None,
            "is_current": (version == "1.0")
        }
        revisions_list.append(rev_record)

    citation_id_counter = 1
    doc_ids = [d["document_id"] for d in docs]
    for doc in docs:
        if random.random() < 0.4:
            num_citations = random.randint(1, 4)
            targets = random.sample(doc_ids, num_citations)
            for t in targets:
                if t != doc["document_id"]:
                    citations_list.append({
                        "citation_id": f"CIT-{citation_id_counter:05d}",
                        "document_id": doc["document_id"],
                        "cited_document_id": t,
                        "citation_type": "References",
                        "citation_context": f"{doc['document_id']} references architectural principles defined in {t}.",
                        "citation_date": doc["created_date"]
                    })
                    citation_id_counter += 1

    citations_list.append({
        "citation_id": "CIT-EXPLICIT-001",
        "document_id": "ADR-021",
        "cited_document_id": "ADR-001",
        "citation_type": "Supersedes",
        "citation_context": "ADR-021 explicitly supersedes legacy database decision ADR-001.",
        "citation_date": "2025-11-10"
    })

    conflicts_list = [
        {
            "conflict_id": "CONF-001",
            "document_id_a": "ADR-001",
            "document_id_b": "ADR-021",
            "conflict_type": "Superseded Decision Clash",
            "conflict_topic": "Database Choice for Project Alpha",
            "detected_conflict": "ADR-001 recommends MySQL 5.7 while ADR-021 specifies PostgreSQL 15 as mandatory.",
            "resolution_status": "Resolved",
            "resolution_document_id": "ADR-021"
        }
    ]

    permissions_list = []
    for doc in docs:
        d_id = doc["document_id"]
        conf = doc["confidentiality_level"]
        proj = doc["project"]

        for u_id, u_role, u_dept, u_proj in USER_ROLES:
            allowed = True
            if conf in ["Restricted", "Confidential"]:
                if u_role not in ["Architect", "Security Engineer", "Chief Architect"] and u_proj != proj:
                    allowed = False
            
            permissions_list.append({
                "document_id": d_id,
                "user_id": u_id,
                "role": u_role,
                "access_level": "Read" if allowed else "None",
                "allowed": allowed,
                "department_scope": u_dept,
                "project_scope": u_proj
            })

    return (
        pd.DataFrame(docs),
        pd.DataFrame(metadata_list),
        pd.DataFrame(revisions_list),
        pd.DataFrame(permissions_list),
        pd.DataFrame(citations_list),
        pd.DataFrame(conflicts_list)
    )

def generate_evaluation_datasets(docs_df):
    queries = [
        ("Q-01", "What database should we use for Project Alpha?", "ADR-021", "PostgreSQL 15 is the approved database for Project Alpha.", "databases", "ADR-021,ADR-001"),
        ("Q-02", "What authentication mechanism is currently approved for Project Beta?", "ADR-002", "OAuth 2.0 with OpenID Connect (OIDC) via Okta.", "authentication", "ADR-002"),
        ("Q-03", "What is the restricted encryption key policy for customer data?", "DOC-0003", "AES-256 KMS key rotation protocols apply.", "security", "DOC-0003"),
        ("Q-04", "Which database choice was superseded for Project Alpha?", "ADR-001", "ADR-001 (MySQL) was superseded by ADR-021.", "databases", "ADR-001,ADR-021")
    ]

    test_queries = []
    rel_labels = []

    for idx, q_tuple in enumerate(queries, start=1):
        q_id, q_text, exp_id, exp_ans, topic, rel_docs = q_tuple
        test_queries.append({
            "query_id": q_id,
            "query": q_text,
            "expected_document_id": exp_id,
            "expected_answer": exp_ans,
            "topic": topic,
            "difficulty": "Easy" if idx <= 3 else "Medium",
            "relevant_documents": rel_docs
        })
        rel_labels.append({
            "query_id": q_id,
            "document_id": exp_id,
            "relevance_score": 1.0,
            "is_authoritative": True
        })

    for i in range(5, 51):
        t = TOPICS[(i - 5) % len(TOPICS)]
        if "topic" in docs_df.columns:
            matching = docs_df[(docs_df["topic"] == t) & (docs_df["approval_status"] == "Approved")]
            if matching.empty:
                matching = docs_df[docs_df["topic"] == t]
        else:
            matching = docs_df
            
        target_doc = matching.iloc[0] if not matching.empty else docs_df.iloc[i % len(docs_df)]
        
        q_id = f"Q-{i:02d}"
        q_text = f"What is the approved architecture decision regarding {t} for {target_doc.get('project', 'the enterprise')}?"
        exp_id = target_doc["document_id"]
        exp_ans = f"Standard guidance for {t} in {target_doc.get('project')}."
        
        test_queries.append({
            "query_id": q_id,
            "query": q_text,
            "expected_document_id": exp_id,
            "expected_answer": exp_ans,
            "topic": t,
            "difficulty": "Medium",
            "relevant_documents": exp_id
        })
        rel_labels.append({
            "query_id": q_id,
            "document_id": exp_id,
            "relevance_score": 1.0,
            "is_authoritative": True
        })

    queries_df = pd.DataFrame(test_queries)
    rel_df = pd.DataFrame(rel_labels)
    user_fb_template = pd.DataFrame(columns=[
        "feedback_id", "timestamp", "user_id", "query_id", "query", "recommended_document_id",
        "useful_yes_no", "trustworthy_yes_no", "consulted_additional_source_yes_no",
        "first_answer_accepted", "comments", "data_status"
    ])

    return queries_df, rel_df, user_fb_template

def main():
    docs_df, meta_df, rev_df, perm_df, cit_df, conf_df = generate_documents(count=1000)
    raw_dir = settings.RAW_DATA_DIR
    raw_dir.mkdir(parents=True, exist_ok=True)

    docs_df.to_csv(raw_dir / "documents.csv", index=False)
    meta_df.to_csv(raw_dir / "document_metadata.csv", index=False)
    rev_df.to_csv(raw_dir / "revision_history.csv", index=False)
    perm_df.to_csv(raw_dir / "permissions.csv", index=False)
    cit_df.to_csv(raw_dir / "citations.csv", index=False)
    conf_df.to_csv(raw_dir / "conflicts.csv", index=False)

    eval_dir = settings.EVALUATION_DATA_DIR
    queries_df, rel_df, user_fb_df = generate_evaluation_datasets(docs_df)
    queries_df.to_csv(eval_dir / "test_queries.csv", index=False)
    rel_df.to_csv(eval_dir / "relevance_labels.csv", index=False)
    user_fb_df.to_csv(eval_dir / "user_feedback.csv", index=False)

if __name__ == "__main__":
    main()

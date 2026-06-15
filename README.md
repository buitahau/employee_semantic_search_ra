# RA-G — Skills Search Module

**RAG minus the Generation step.** Retrieve and rank; do not generate.

This module adds a skills search feature to the OWT Employee App. It lets admins find the right people for a project in seconds instead of manually browsing profiles.

---

## Problem

OWT has ~60 employees. When staffing a new project, admins have no efficient way to find people whose skills match the requirements — they rely on memory or manual profile browsing.

## Solution

A single unified search endpoint that supports two complementary modes:

- **Semantic search** — vector similarity over employee CVs, experience records, and training logs. Admin types a natural-language query like `"React developer with e-commerce experience"` and gets ranked results.
- **Structured filter search** — fast SQL queries over skill/proficiency tables. Filter by skill, proficiency level, position, experience, and training records.

When both modes are used together, structured filters run first to narrow candidates, then semantic search reranks the survivors.

---

## Technology

| Concern | Choice | Reason |
|---|---|---|
| Vector store | pgvector (PostgreSQL extension) | No extra service — project already uses Postgres |
| Embedding model | all-MiniLM-L6-v2 (384 dims) | CPU-only, well-tested for semantic similarity, swappable |
| Embedding runtime | onnxruntime (~50 MB) | Avoids PyTorch (~1.5 GB) for CPU-only inference |
| API | Python / FastAPI | Single service; embedding runs as a sub-module, not a sidecar |

---

## Setup & Running

### Prerequisites

- Python 3.12
- Docker & Docker Compose (for local databases)
- The `all-MiniLM-L6-v2` ONNX model (downloaded via `scripts/download_model.py` into `models/all-MiniLM-L6-v2/`)

### 1. Start databases

```bash
docker compose -f docker-compose.yml up -d
```

This starts two containers:
- `ra_source_db` — PostgreSQL 16 on port **5433** (source employee DB)
- `ra_vector_db` — pgvector on port **5434** (vector store)

### 2. Install Python dependencies

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Download the embedding model

```bash
python scripts/download_all-MiniLM-L6-v2_model.py
```

Downloads the ONNX model and tokenizer into `models/all-MiniLM-L6-v2/`. Run once after install.

### 4. Configure

```bash
cp .env.example .env
# The default values in .env.example match the docker-compose ports and credentials.
# Fill in LLM_API_KEY for the AI cleanup phase.
```

### 5. Run migrations and seed data

Apply the pgvector schema to the vector DB:

```bash
psql -h localhost -p 5434 -U postgres -d vectordb -f migrations/001_create_skills_search_index.sql
```

Load local seed data (200 employees) into the source DB:

```bash
psql -h localhost -p 5433 -U postgres -d postgres -f migrations/local/seed_with_200_full_users.sql
```

Both commands will prompt for the password (`123456`).

### 6. Start the dev server

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

The API is available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Run tests

```bash
pytest
```

---

## Docs

- [`docs/proposal/v3.md`](docs/proposal/v3.md) — Architecture & functional requirements (current)

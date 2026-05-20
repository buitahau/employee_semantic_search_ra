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
- Two PostgreSQL instances: the source OWT employee DB and a pgvector-enabled DB for the vector store
- The `all-MiniLM-L6-v2.onnx` model file (place it at the path set in `EMBEDDING_MODEL_PATH`)

### Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
# Edit .env and fill in your values:
#   SOURCE_DB_*        — owt-employee-app-backend database
#   VECTOR_DB_*        — pgvector database
#   OPENAI_API_KEY     — GPT-4.1 mini (used in the AI cleanup phase)
#   EMBEDDING_MODEL_PATH — path to all-MiniLM-L6-v2.onnx
```

### Run migrations

Apply the pgvector schema to the vector DB before first use:

```bash
psql -h $VECTOR_DB_HOST -U $VECTOR_DB_USER -d $VECTOR_DB_NAME -f migrations/<migration_file>.sql
```

### Start the dev server

```bash
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

# CLAUDE.md — ra_minus_g

Skills search module for the OWT Employee App. ETL pipeline that indexes employee data into pgvector, plus a FastAPI query API. RAG without the generation step — retrieve and rank, do not generate.

## Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.12 |
| API | FastAPI 0.111, uvicorn |
| Source DB | PostgreSQL via psycopg2-binary |
| Vector DB | PostgreSQL + pgvector (384-dim, all-MiniLM-L6-v2) |
| Embeddings | onnxruntime (CPU-only, ~50 MB) |
| AI cleanup | OpenAI GPT-4.1 mini (T3.2 only) |
| Config | pydantic-settings (env-prefixed) |
| Tests | pytest, pytest-asyncio |

## Package Layout

```
api/            FastAPI app — /search and /index endpoints only
  routers/
    search.py   GET /search
    index.py    POST /index
etl/            ETL pipeline phases (one module per phase)
  extract.py    Phase 2 — pull raw data from source DB
  transform.py  Phase 3 — normalize → AI cleanup → chunk → embed
  load.py       Phase 4 — upsert into pgvector
  trigger.py    Phase 5 — reconciliation triggers
query/          SQL query functions against the source DB (psycopg2)
common/
  config.py     Settings loaded from env (SOURCE_DB_*, VECTOR_DB_*, OPENAI_API_KEY)
  constants.py  PREPROCESS_VERSION and other shared constants
  logging.py    Structured JSON logger — get_logger(name)
  types.py      Shared dataclasses (RawEmployeeData, CvRow, etc.)
migrations/     SQL migration files (pgvector schema + last_index_at columns)
tests/          pytest test suite
```

## Conventions

### config
- All external config is loaded via pydantic-settings in `common/config.py`
- No hardcoded credentials, hostnames, or connection strings anywhere in source
- Import as `from common.config import settings`

### constants
- Shared constants live in `common/constants.py`
- `PREPROCESS_VERSION` must be bumped whenever normalization or chunking rules change (affects cache invalidation)

### query/
- Raw SQL via psycopg2 only — no ORM
- Always use parameterized queries (`%s` placeholders); never interpolate user input or dynamic values into SQL strings

### etl/
- Each module is responsible for exactly one pipeline phase
- Pure transform functions (normalize, chunk) must be side-effect-free
- `PREPROCESS_VERSION` from `common/constants` must be stored alongside every indexed chunk

### api/
- Route handlers are thin — delegate all logic to `etl/` modules
- No database access or business logic inside router files
- Use FastAPI dependency injection for DB connections (when implemented)

### tests/
- New functions in `etl/` and `query/` require unit tests
- Tests assert on output/behavior, not just that a function is callable
- Removed tests must be justified by deleted code

### commits
- Follow Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`
- Do not mix cosmetic changes with functional changes in the same commit

## Environment

Copy `.env.example` → `.env` and fill in values. `.env` is git-ignored. Required variables:

```
SOURCE_DB_HOST / PORT / NAME / USER / PASSWORD   — owt-employee-app-backend DB
VECTOR_DB_HOST / PORT / NAME / USER / PASSWORD   — pgvector DB
OPENAI_API_KEY                                   — GPT-4.1 mini for AI cleanup (T3.2)
EMBEDDING_MODEL_PATH                             — path to all-MiniLM-L6-v2.onnx
```

## Running

```bash
# Install
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Dev server
uvicorn main:app --reload

# Tests
pytest
```

## Implementation Plan

Phased ETL rollout documented in `docs/implementation_plan/`:
- `elt/plan.md` — full ETL roadmap (T1–T6)
- `query/plan.md` — query layer roadmap
- `elt/tasks/T*.md` — individual task specs with deliverables and acceptance tests

Current branch tracks task progress via branch naming: `feat/T{N}.{M}-{slug}`.

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| pr-review | `/review [PR number or URL]` | Review a GitHub PR — code smells, conventions, test coverage, scope |

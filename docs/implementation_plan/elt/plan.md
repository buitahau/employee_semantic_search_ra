# ETL Implementation Plan

Source spec: [`docs/proposal/etl.md`](../docs/proposal/etl.md)

---

## Overview

The ETL pipeline indexes employee data into `pgvector` for semantic search. It extracts source entities from `owt-employee-app-backend`, transforms them through normalization → AI cleanup → metadata extraction → chunking → embedding, and loads the results into `skills_search_index`.

---

## Task Breakdown

### Phase 1 — Infrastructure & Schema

#### T1.1 — Database schema

***Description***
- Create `skills_search_index` table with columns: `id`, `employee_id`, `chunk_index`, `field_type TEXT NOT NULL` (`'cv'`, `'training_log'`, `'task'`), `chunk_text`, `normalized_text`, `ai_search_text`, `embedding VECTOR(384)`, `metadata JSONB`, `indexed_at`
- Add `UNIQUE (employee_id, chunk_index)` constraint
- Add GIN index on `metadata`
- Verify pgvector extension is installed and `VECTOR(384)` type is available
- Add `last_index_at TIMESTAMPTZ` column (nullable, default `NULL`) to each source entity table: `user_cvs`, `user_skills`, `experiences`, `experience_skills`, `employment_histories`, `trainings`, `task_assignments`, `task_assignments_assignees`
  - Set to the current timestamp whenever a row is successfully included in an indexing run
  - Allows the reconciliation job (T5.2) to compare `last_index_at` against the row's `updated_at` / `created_at` to detect rows that have changed since they were last indexed

***Deliverables***
- `migrations/001_create_skills_search_index.sql` (idempotent): creates `skills_search_index` with all specified columns and types (including `field_type TEXT NOT NULL`), enforces `UNIQUE (employee_id, chunk_index)`, adds GIN index on `metadata`; `SELECT '[1,2,3]'::vector(3);` confirms pgvector is active
- `migrations/002_add_last_index_at.sql`: adds `last_index_at TIMESTAMPTZ` (nullable, default `NULL`) to all eight source entity tables

#### T1.2 — Project scaffold

***Description***
- Set up project structure with three top-level modules:
  - `etl/` — pipeline logic; contains skeleton files: `extract.py`, `transform.py`, `load.py`, `trigger.py`
  - `query/` — all SQL/ORM queries for source entity extraction (feeds into T2.1)
  - `common/` — shared utilities (logging, config, constants, types)
- Set up environment config covering:
  - Traditional DB connection (host, port, name, user, password for `owt-employee-app-backend`)
  - Vector DB connection (host, port, name, user, password for pgvector)
  - OpenAI API key
  - Embedding service URL

***Deliverables***
- Directory tree: `etl/` (with `extract.py`, `transform.py`, `load.py`, `trigger.py`), `query/`, `common/` — all modules importable with no `ImportError` or circular imports
- `requirements.txt` (or `pyproject.toml`) with pinned versions; `pip install -r requirements.txt` completes without error in a fresh virtualenv
- `.env.example` covering both DB connections, OpenAI, and embedding service; `from common.config import settings` loads without error and exposes distinct connection configs for the traditional DB and the vector DB

---

### Phase 2 — Extract

#### T2.1 — Source entity queries

***Description***

One query function per sub-task below. Each accepts `employee_id: int`, uses parameterised queries, and returns a typed list.

**T2.1a — CV**

| Table | Selected columns |
|---|---|
| `user_cvs` | `cv`, `updated_at` |
| `cv_overview` | `custom_position`, `introduction`, `updated_at` |

**T2.1b — Experience**

| Table | Selected columns |
|---|---|
| `experiences` | `project_name`, `domain`, `description`, `roles_and_responsibilities`, `date_from`, `date_to`, `is_currently_working`, `updated_at` |
| `experience_skills` | *(join only)* |
| `skills` | `name` |

**T2.1c — Employment history**

| Table | Selected columns |
|---|---|
| `employment_histories` | `company`, `date_from`, `date_to`, `is_currently_working`, `updated_at` |

**T2.1d — Training**

| Table | Selected columns |
|---|---|
| `trainings` | `training_title`, `training_description`, `training_date`, `updated_at` |
| `training_topics` | `label` → `topic_label` |
| `training_levels` | `label` → `level_label` |

**T2.1e — Task**

| Table | Selected columns |
|---|---|
| `task_assignments` | `title`, `details`, `updated_at` |
| `task_assignments_assignees` | *(join/filter only)* |
| `task_assignments_categories` | `label` → `category_label` |

**T2.1f — User skills**

| Table | Selected columns |
|---|---|
| `user_skills` | `level`, `updated_at` |
| `skills` | `name` → `skill_name` |

***Deliverables***
- One query function per sub-task (T2.1a–T2.1f), each accepting `employee_id: int`, filtered correctly (`is_selected = true` where required), and using parameterised queries (no string interpolation)
- `RawEmployeeData` dataclass with the following structure:

```python
@dataclass
class RawEmployeeData:
    employee_id: int
    cv: CvRow | None               # at most one CV per employee
    experiences: list[ExperienceRow]
    employment_histories: list[EmploymentHistoryRow]
    trainings: list[TrainingRow]
    tasks: list[TaskRow]
    skills: list[UserSkillRow]

@dataclass
class CvRow:
    cv: str                        # user_cvs.cv
    custom_position: str | None    # cv_overview.custom_position
    introduction: str | None       # cv_overview.introduction
    updated_at: datetime

@dataclass
class ExperienceRow:
    project_name: str
    domain: str
    description: str
    roles_and_responsibilities: str
    date_from: date
    date_to: date | None
    is_currently_working: bool
    skills: list[str]              # skills.name resolved via experience_skills
    updated_at: datetime

@dataclass
class EmploymentHistoryRow:
    company: str
    date_from: date
    date_to: date | None
    is_currently_working: bool
    updated_at: datetime

@dataclass
class TrainingRow:
    training_title: str | None
    training_description: str | None
    training_date: date
    topic_label: str | None        # training_topics.label
    level_label: str | None        # training_levels.label
    updated_at: datetime

@dataclass
class TaskRow:
    title: str
    details: str
    category_label: str | None     # task_assignments_categories.label
    updated_at: datetime

@dataclass
class UserSkillRow:
    skill_name: str                # skills.name
    level: int                     # 0–5
    updated_at: datetime
```

- `get_raw_employee_data(employee_id: int) -> RawEmployeeData` — calls T2.1a–T2.1f and populates the DTO; all list fields default to `[]` and `cv` defaults to `None` for an unknown employee
- `get_stale_employee_ids() -> list[int]` — returns `employee_id` values where at least one source-entity row has `updated_at > last_index_at` or `last_index_at IS NULL`; excludes employees whose data has not changed since last index
- Fixture SQL (or factory helpers) that seeds a known employee for testing

---

### Phase 3 — Transform

#### T3.1 — Step 1: Text normalization

***Description***
- Strip HTML tags (handle rich-text editor output)
- Decode HTML entities (`&rsquo;` → `'`, `&amp;` → `&`, `&#46;` → `.`, etc.)
- Collapse whitespace (spaces, tabs, newlines, zero-width chars → single space)
- Unify punctuation (curly quotes → straight, em/en dashes → `-`)
- Skip sentinels: return `None` for `"null"`, `"undefined"`, `"None"`, empty string
- **Do NOT** apply: lowercasing, stop-word removal, stemming, punctuation stripping, spell correction
- Unit test: apply to the spec's example input and assert exact `normalized_text` output

***Deliverables***
- `normalize_text(text: str | None) -> str | None` pure function: strips HTML, decodes entities, collapses whitespace, unifies punctuation; returns `None` for all sentinel values (`"null"`, `"undefined"`, `"None"`, `""`, `None`); does not lowercase, stem, or strip punctuation
- Unit test file asserting exact `normalized_text` output from the spec's example input and covering all sentinel cases

#### T3.2 — Step 2: AI cleanup (GPT-4.1 mini)

***Description***
- Build prompt instructing the model to remove boilerplate/filler while preserving: skills, tools, frameworks, domains, project names, role names, dates, outcomes, certifications, uncommon terms
- Call OpenAI API with `normalized_text`, receive `ai_search_text`
- Store both fields — never discard `normalized_text`
- Handle API errors gracefully: fall back to `normalized_text` if the call fails
- Unit test: verify filler sentences are removed, named entities and dates are preserved

***Deliverables***
- `ai_cleanup(normalized_text: str) -> str` function: removes filler while preserving named entities, dates, and certifications; returns `normalized_text` unchanged (with a WARNING log) if the OpenAI call raises any exception; never mutates or discards `normalized_text`
- System prompt stored as a versioned constant (not inlined)
- Unit tests using mocked OpenAI responses verifying filler removal and entity/date preservation

#### T3.3 — Step 3: Metadata extraction

***Description***
- Extract fixed fields for every chunk:
  - `employee_id` (int)
  - `skills` (union of linked skills from DB + AI-extracted skills from `ai_search_text`)
  - `date_from` / `date_to` formatted as `YYYY-MM` (null if ongoing)
- Extract source-specific fields based on type:
  - `cv`: `position` (customPosition), `summary` (first sentence of introduction)
  - `experience`: `project` (projectName), `domain`, `years` (computed from dateFrom/dateTo)
  - `training`: `title` (trainingTitle), `topic` (topic.label), `level` (level.label)
  - `task`: `title`, `category` (category.label)
- `years` computation: `ceil((dateTo - dateFrom).days / 365)`, use today if `isCurrentlyWorking`
- Unit test: assert metadata shape against spec's example JSON

***Deliverables***
- `extract_metadata(source_type: str, record: dict, employee_id: int) -> dict` function: output matches the spec's example JSON shape; `date_from`/`date_to` are `YYYY-MM` strings or `null` (never raw `datetime`); `years` uses today when `isCurrentlyWorking = true` and applies `ceil`; `skills` is a deduplicated union of DB-linked and AI-extracted skills
- Unit tests covering all four source types and `years` edge cases

#### T3.4 — Step 4: Chunking

***Description***
- Tokenize `ai_search_text` using the `all-MiniLM-L6-v2` tokenizer
- Detect sentence boundaries
- Accumulate sentences up to 200 tokens; emit chunk at last sentence boundary
- Overlap: retain last ~40–50 tokens from previous chunk as window start
- For blocks without sentence boundaries: recurse paragraph → sentence → token split
- Prepend source-type prefix to each chunk (e.g. `"Experience: "`, `"Training: "`, `"CV: "`, `"Task: "`)
- Attach provenance fields per chunk: `chunk_index`, `token_count`, `char_start`, `char_end`, `preprocess_version`
- Merge metadata from T3.3 into each chunk record
- Unit test: verify overlap behaviour, prefix presence, token counts within bounds

***Deliverables***
- `ChunkRecord` dataclass with all provenance and metadata fields
- `chunk_text(text: str, source_type: str, metadata: dict) -> list[ChunkRecord]` function: every chunk's `token_count` ≤ 200; overlap between consecutive chunks is 40–50 tokens; each `chunk_text` starts with the correct source-type prefix; all provenance fields (`chunk_index`, `token_count`, `char_start`, `char_end`, `preprocess_version`) populated; a single-sentence input produces exactly one chunk with no overlap
- Unit tests covering multi-chunk splits, overlap, prefix, and the no-sentence-boundary fallback

#### T3.5 — Step 5: Embedding

***Description***
- Load `all-MiniLM-L6-v2` ONNX model
- For each `chunk_text`: tokenize → ONNX inference → mean pooling (exclude padding tokens) → L2 normalize → 384-dim vector
- Verification tests:
  - Same string embedded twice → cosine similarity = `1.0`
  - ONNX output vs `sentence-transformers` reference within `1e-5` per dimension
  - Round-trip through pgvector: insert known embedding, query it back, similarity = `1.0`

***Deliverables***
- `embed(text: str) -> list[float]` returning a 384-dim L2-normalised vector (norm `1.0 ± 1e-6`); ONNX model path configurable via env and loaded once at startup
- Three verification tests: same string twice → cosine similarity `1.0`; per-dimension delta vs `sentence-transformers` reference < `1e-5`; pgvector round-trip → cosine similarity `1.0`

#### T3.6 — Transform coordinator

***Description***
- Function `transform(raw: RawEmployeeData) -> list[ChunkRecord]` that chains T3.1 → T3.2 → T3.3 → T3.4 → T3.5 for all source types and returns a flat list of fully populated chunk records ready for insertion

***Deliverables***
- `transform(raw: RawEmployeeData) -> list[ChunkRecord]` function: returns a non-empty flat list for a populated input; each `ChunkRecord` has all required fields (`chunk_text`, `normalized_text`, `ai_search_text`, `embedding`, `metadata`, `chunk_index`, `token_count`, `preprocess_version`); source types with no data produce zero chunks without raising an exception
- Integration test verifying all five steps execute in order (normalise → AI cleanup → metadata → chunk → embed) against a fixture `RawEmployeeData`

---

### Phase 4 — Load

#### T4.1 — Write strategy

***Description***
- Function `load_employee(employee_id, chunks: list[ChunkRecord])` that:
  1. Opens a transaction
  2. `DELETE FROM skills_search_index WHERE employee_id = $1`
  3. Bulk-inserts all chunks (use `COPY` or batch `INSERT` for performance)
  4. Commits — atomically swaps old index for new
- Never leave partial state: the transaction ensures either all-new or all-old

***Deliverables***
- `load_employee(employee_id: int, chunks: list[ChunkRecord]) -> None` function: opens a transaction, deletes existing rows, bulk-inserts all chunks, commits; on success contains exactly `len(chunks)` rows with no stale rows from prior runs; handles ≥ 500 chunks without timing out
- Atomicity test: simulate a mid-insert failure and assert the transaction rolls back and previous rows are left intact

#### T4.2 — Idempotency check

***Description***
- Confirm re-running `load_employee` for the same `employee_id` produces a clean replacement with no stale rows

***Deliverables***
- Idempotency test: calls `load_employee` twice with different chunk sets; asserts row count equals the second call's length (not the sum), no `chunk_index` duplicates exist, and calling with an empty list results in zero rows for that `employee_id`

---

### Phase 5 — Triggers

#### T5.1 — Hook trigger

***Description***
- Register DB hooks (or application-level event listeners) on source entities: `user_cvs`, `cv_overview`, `experiences`, `experience_skills`, `employment_histories`, `trainings`, `task_assignments`, `task_assignments_assignees`
- On CREATE / UPDATE / DELETE: resolve the affected `employee_id` and enqueue a re-index job
- Use a queue (or direct async call) to avoid blocking the DB write path

***Deliverables***
- Hook registrations (PostgreSQL triggers or ORM listeners) for all eight source entities: a CREATE, UPDATE, or DELETE enqueues exactly one re-index job for the affected `employee_id` without blocking the originating DB write; if the queue is unavailable the hook logs an error and does not fail the transaction
- Queue producer that enqueues `{ employee_id, triggered_at }` on each mutation, with an integration test per entity (insert a row, assert job in queue)

#### T5.2 — Scheduled reconciliation job

***Description***
- Periodic scan: find employees whose `max(indexed_at)` in `skills_search_index` is older than their last source-data update, or who have no rows at all
- For each stale employee, enqueue a re-index
- Run on a configurable schedule (e.g. every 30 minutes)

***Deliverables***
- `reconcile()` function: detects employees with no rows in `skills_search_index` or with source data updated after their last `indexed_at`, enqueues a re-index for each; does not enqueue up-to-date employees
- Scheduler wiring with interval read from env (e.g. `RECONCILE_INTERVAL_MINUTES=30`, default 30 minutes)

#### T5.3 — Manual indexing API

***Description***
- `POST /admin/index/all` — enqueue re-index for every employee
- `POST /admin/index/:employee_id` — enqueue re-index for one employee
- Require admin auth; return a job ID or status

***Deliverables***
- `POST /admin/index/all` — returns `200` with a job ID or enqueue count; enqueues all employees; calling twice does not double-process
- `POST /admin/index/:employee_id` — returns `200` with a job ID; returns `404` for an unknown employee; unauthenticated or non-admin requests receive `401`/`403`
- Auth middleware applied to both routes

---

### Phase 6 — Observability & Hardening

#### T6.1 — Logging

***Description***
- Log at each pipeline stage: extract row counts, normalize skip counts (sentinels), AI call latency, chunk counts, embed latency, rows written
- Log errors with `employee_id` and stage name for fast diagnosis

***Deliverables***
- Structured log statements (JSON or key=value) at INFO level for each stage (extract, normalize, AI cleanup, chunk, embed, load): each line includes `employee_id`, `stage`, and the relevant metric (row count, latency ms, etc.)
- ERROR-level log wrapper that always includes `employee_id` and `stage` before propagating any exception

#### T6.2 — `preprocess_version` bumping

***Description***
- Define `PREPROCESS_VERSION = 1` as a constant
- Document: bump this integer when normalization/chunking rules change to mark existing rows as stale, triggering a rebuild via the reconciliation job

***Deliverables***
- `PREPROCESS_VERSION = 1` constant in `common/constants.py` with a comment explaining when and how to bump; every `ChunkRecord` written to the DB carries `metadata.preprocess_version = PREPROCESS_VERSION`
- Reconciliation query extended to treat rows where `metadata->>'preprocess_version' != PREPROCESS_VERSION` as stale; bumping the constant from `1` to `2` causes all existing rows to be flagged in the next reconciliation run

#### T6.3 — Resilience

***Description***
- AI cleanup failures fall back to `normalized_text` (logged as a warning)
- Embedding failures abort the transaction and leave the old index intact (logged as an error)
- Hook trigger failures are retried via the queue; reconciliation acts as the safety net

***Deliverables***
- Error-handling wrapper in `ai_cleanup`: on any OpenAI exception returns `normalized_text` unchanged and emits a WARNING log; no exception propagates
- Error-handling wrapper in `embed`/`load_employee`: on any ONNX/embedding exception rolls back the transaction, leaves existing `skills_search_index` rows intact, and emits an ERROR log
- Queue retry policy documentation: failed hook enqueues are retried at least 3 times with backoff before being dead-lettered

#### T6.4 — Integration test

***Description***
- End-to-end test: seed a known employee record, run the full pipeline, assert:
  - Correct number of rows in `skills_search_index`
  - `metadata` matches expected shape
  - Cosine similarity of query embedding vs stored embedding > 0.95 for a matching query

***Deliverables***
- End-to-end test: seeds a fixture employee, runs `extract_employee` → `transform` → `load_employee`; asserts row count matches expected chunk count, `metadata` JSON shape is correct (all required keys, correct types), and cosine similarity of a matching query vs stored embeddings is ≥ 0.95
- Teardown removes all seeded data; test passes on a clean DB with no dependency on prior state

---

## Dependency Order

```
T1.1 → T1.2
T1.2 → T2.1
T2.1 → T3.1 → T3.2 → T3.3 → T3.4 → T3.5 → T3.6
T3.6 → T4.1 → T4.2
T4.1 → T5.1, T5.2, T5.3
T4.2 → T6.4
T3.1–T3.5 → T6.2
```

Phases 1–4 must be complete before Phase 5. Phase 6 runs in parallel with Phase 5 and wraps up last.

---

## Open Questions

1. **Queue implementation** — use an in-process async queue, a DB-backed job table, or an external queue (Redis/BullMQ)? Affects T5.1 and T5.2.
2. **AI cleanup toggle** — should `ai_search_text` generation be skippable per source type or globally disabled for cost control?
3. **Embedding service** — is `all-MiniLM-L6-v2` hosted as a separate HTTP service or loaded in-process? Affects latency and deployment model.
4. **Hook mechanism** — are hooks PostgreSQL triggers (LISTEN/NOTIFY) or application-level ORM hooks in `owt-employee-app-backend`?

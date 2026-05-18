# Query Implementation Plan

Source spec: [`docs/proposal/query.md`](../../proposal/query.md)

---

## Overview

The query layer accepts a natural language query, normalises and rewrites it via LLM, embeds it with the same `all-MiniLM-L6-v2` model used by ETL, retrieves ranked chunks from `skills_search_index`, aggregates results per employee, hydrates display data from the source DB, and returns a formatted response whose shape depends on the detected intent.

---

## Task Breakdown

### Phase 1 — Infrastructure & Scaffold

#### T1.1 — Module scaffold & types

***Description***
- Add a `search/` top-level module alongside `etl/` with skeleton files: `normalize.py`, `rewrite.py`, `retrieve.py`, `aggregate.py`, `hydrate.py`, `respond.py`, `router.py`
- Define shared input/output types used across all steps:

```python
@dataclass
class QueryRequest:
    query: str

@dataclass
class RewriteResult:
    intent:    str          # "find_employees" | "others"
    query:     str          # keyword-dense rewrite for embedding
    heuristic: str          # instruction for Step 5
    filter:    dict         # structured GIN filter (may be empty)

@dataclass
class ChunkHit:
    employee_id: int
    chunk_text:  str
    metadata:    dict
    score:       float

@dataclass
class EmployeeHit:
    employee_id: int
    score:       float
    skills:      list[str]
    chunks:      list[str]  # chunk_text values as LLM evidence

@dataclass
class EmployeeDisplay:
    employee_id: int
    name:        str
    position:    str | None
    avatar:      str | None
    score:       float
    skills:      list[SkillDisplay]
    match_reason: str | None   # populated only for find_employees

@dataclass
class SkillDisplay:
    skill_name:  str
    level:       int          # 0–5
```

- Register the `search` router in the FastAPI app entry point

***Deliverables***
- `search/` directory with all skeleton files importable with no `ImportError`
- All dataclasses defined and importable from `search/types.py`
- Router registered: `GET /search` returns `501 Not Implemented` (placeholder)

---

### Phase 2 — Input Processing

#### T2.1 — Step 1: Prompt normalisation

***Description***
- Apply the same normalisation rules as ETL Step 1, adapted for a short query string (not long-form text):

| Operation | Detail |
|---|---|
| Lowercase | Reduce token variance for the embedding model |
| Trim & collapse whitespace | Remove leading/trailing and repeated spaces |
| Unify punctuation | Normalise curly quotes, dashes, encoding variants to ASCII equivalents |
| Skip sentinels | Reject empty strings, `"null"`, `"undefined"` — raise `ValueError` immediately |

- Do **not** strip HTML (queries are not rich-text editor output)
- Return the normalised string; raise `ValueError` for sentinel inputs

***Deliverables***
- `normalize_query(query: str) -> str` pure function: lowercases, trims, collapses whitespace, unifies punctuation; raises `ValueError` for all sentinel values (`""`, `"null"`, `"undefined"`, `None`)
- Unit tests covering all sentinel cases and a representative normalisation example

#### T2.2 — Step 2: AI prompt rewrite

***Description***
- Pass the normalised query to GPT-4.1 mini with a structured output prompt
- The model must:
  - Correct typos and grammar (`"developper"` → `"developer"`)
  - Expand abbreviations (`"FE"` → `"frontend"`, `"BE"` → `"backend"`)
  - Remove redundant filler (`"Can you tell me who..."` → `"who..."`)
- Return a `RewriteResult` parsed from the model's JSON output:

```json
{
  "intent":    "find_employees | others",
  "query":     "<rewritten text used to generate the embedding in Step 3>",
  "heuristic": "<plain-language instruction for Step 5>",
  "filter":    { "<metadata key>": "<value>" }
}
```

- On OpenAI API failure: fall back to `intent="find_employees"`, `query=<normalized input>`, `heuristic="rank employees by score descending"`, `filter={}` — log as WARNING, never raise

***Deliverables***
- `rewrite_query(normalized: str) -> RewriteResult` function: calls GPT-4.1 mini, parses the JSON output into `RewriteResult`; on any exception returns the fallback `RewriteResult` and emits a WARNING log
- System prompt stored as a versioned constant (not inlined), covering the spec's two example cases
- Unit tests using mocked OpenAI responses asserting correct field mapping for `find_employees` and `others` intents, and verifying the fallback path

---

### Phase 3 — Retrieval

#### T3.1 — Step 3: Embed query & pgvector search

***Description***
- Embed `RewriteResult.query` using `all-MiniLM-L6-v2` (same model and pipeline as ETL Step 5) to produce a 384-dim L2-normalised vector
- Run cosine similarity search against `skills_search_index`:

```sql
SELECT
  employee_id,
  chunk_text,
  metadata,
  1 - (embedding <=> :query_vector) AS score
FROM skills_search_index
WHERE metadata @> :structured_filters   -- omitted if filter is empty
ORDER BY score DESC
LIMIT 100;
```

- Apply `RewriteResult.filter` as a GIN `@>` condition only when the filter dict is non-empty
- Return a list of `ChunkHit` objects

***Deliverables***
- `retrieve(rewrite: RewriteResult) -> list[ChunkHit]` function: embeds the rewritten query, executes the parameterised SQL, applies the GIN filter when present, returns up to 100 `ChunkHit` objects ordered by score descending
- Query uses parameterised values only — no string interpolation
- Unit test: with an empty filter dict, the `WHERE metadata @> ...` clause is omitted from the executed SQL

---

### Phase 4 — Aggregation

#### T4.1 — Step 4: Employee aggregation & scoring

***Description***
- `retrieve` returns one row per chunk; multiple chunks belong to the same employee
- Aggregate per employee:
  - Group by `employee_id`
  - Take the **max score** across all chunks as the employee's relevance score
  - Union all `skills` arrays from `metadata` across chunks and deduplicate
  - Collect all `chunk_text` values as evidence for Step 5b
- Sort result list by score descending

***Deliverables***
- `aggregate(hits: list[ChunkHit]) -> list[EmployeeHit]` pure function: output is sorted by `score` descending; each `EmployeeHit.score` equals the max chunk score for that employee; `skills` is a deduplicated union across all chunks; `chunks` contains all matching `chunk_text` values; an empty input returns `[]`
- Unit tests covering multi-chunk deduplication, score max selection, and empty input

---

### Phase 5 — Hydration & Response

#### T5.1 — Step 5a: Fetch full records from source DB

***Description***
- For the list of `employee_id` values in the aggregated results, fetch display-ready and structured data that is not stored in `skills_search_index`:

| Source | What to fetch | Why |
|---|---|---|
| `users` | Name, position, avatar, contact | Display fields, not in the index |
| `user_skills` + `skills` | Skill list with proficiency levels (0–5) | Structured proficiency data, not embedded |

- The `ai_search_text` and `metadata` already held in `ChunkHit` (from Step 3 / Step 4) are reused directly as LLM context in Step 5b — no re-fetch needed
- Batch-fetch all employees in a single query (avoid N+1)

***Deliverables***
- `hydrate(hits: list[EmployeeHit]) -> list[EmployeeDisplay]` function: batch-fetches `users` and `user_skills`+`skills` for all employee IDs in a single query each; populates `name`, `position`, `avatar`, `skills` (with `level`); `match_reason` is left `None` (populated in T5.2); unknown `employee_id` values are omitted from the result
- Unit tests asserting no N+1 queries and correct field mapping

#### T5.2 — Step 5b: Compute & format response

***Description***
- Branch on `RewriteResult.intent`:

**`find_employees`** — pass employee records, scores, chunk evidence, and `heuristic` to GPT-4.1 mini:
- The model uses `heuristic` to re-rank or filter the list
- Generates a human-readable `match_reason` per employee using the full record as context
- Returns a ranked list of `EmployeeDisplay` objects

**`others`** — apply `heuristic` directly to the Step 4 list without an LLM call:
- `"count distinct matched employees above score threshold"` → return a single integer (employees with `score >= 0.5`)
- `"list skills of the matched employee"` → return the `SkillDisplay` list for the top-matched employee
- Any heuristic that cannot be matched to a known deterministic pattern falls back to the `find_employees` LLM path and logs a WARNING

- Score threshold for `others` counts is configurable via env (`SEARCH_SCORE_THRESHOLD`, default `0.5`)

***Deliverables***
- `respond(intent: str, heuristic: str, employees: list[EmployeeDisplay], hits: list[EmployeeHit]) -> dict` function:
  - For `find_employees`: calls GPT-4.1 mini, populates `match_reason` per employee, returns `{"type": "employee_list", "results": [...]}`
  - For `others` with count heuristic: returns `{"type": "count", "value": <int>}`
  - For `others` with skill-lookup heuristic: returns `{"type": "skill_list", "employee": {...}, "skills": [...]}`
  - Unrecognised `others` heuristic falls back to `find_employees` path with WARNING log
- LLM system prompt for `find_employees` stored as a versioned constant
- Unit tests for all three response shapes and the fallback path

---

### Phase 6 — API Layer

#### T6.1 — Search endpoint

***Description***
- `POST /search` — accepts a JSON body `{ "query": "<text>" }` and runs Steps 1–5 in sequence
- Returns a JSON response whose shape depends on intent (see T5.2)
- Returns `400` for sentinel / empty query (from Step 1 `ValueError`)
- Returns `500` with a structured error body on unexpected failures; never leak internal stack traces to the client

```
POST /search
Body: { "query": "Who has Java backend experience and good English?" }

200 OK
{
  "type": "employee_list",
  "results": [
    {
      "employee_id": 12,
      "name": "Nguyen Van A",
      "position": "Backend Developer",
      "avatar": "...",
      "score": 0.91,
      "skills": [{ "skill_name": "Java", "level": 4 }, ...],
      "match_reason": "Strong Java backend, English proficiency confirmed in CV"
    },
    ...
  ]
}
```

- Wire all five steps: `normalize_query` → `rewrite_query` → `retrieve` → `aggregate` → `hydrate` → `respond`

***Deliverables***
- `POST /search` endpoint wired through all six steps
- `400` on sentinel input with `{"error": "invalid_query"}` body
- `500` on unexpected failure with `{"error": "internal_error"}` body — no stack trace exposed
- Integration test: seed known rows in `skills_search_index`, call `POST /search`, assert response shape and non-empty results for a matching query

---

### Phase 7 — Observability & Hardening

#### T7.1 — Logging

***Description***
- Emit structured logs at each step with consistent fields:

| Step | Log fields |
|---|---|
| Normalise | `query_length`, sentinel rejected (if applicable) |
| Rewrite | `intent`, `filter_keys`, LLM latency ms, fallback used (bool) |
| Retrieve | `filter_applied` (bool), `hits_returned` |
| Aggregate | `employees_found`, `max_score`, `min_score` |
| Hydrate | `employees_hydrated` |
| Respond | `response_type`, LLM latency ms (if called) |

- Log errors with `request_id` and `step` for fast diagnosis
- Attach a `request_id` (UUID) to every request and include it in all log lines for that request

***Deliverables***
- Structured log statements (JSON or key=value) at INFO level for each of the six steps; each line includes `request_id`, `step`, and the relevant metric
- `request_id` middleware generating a UUID per request and injecting it into the logging context
- ERROR-level log wrapper that always includes `request_id` and `step` before propagating any exception

#### T7.2 — Resilience

***Description***
- `rewrite_query` LLM failure → fall back to default `RewriteResult` (already defined in T2.2)
- `respond` LLM failure for `find_employees` → return the aggregated list without `match_reason` (set to `None`), log as WARNING
- Embedding failure in `retrieve` → return `500` to caller, log as ERROR, do not partially respond
- Score threshold for `others` counts is configurable (T5.2) to avoid hard-coding business logic

***Deliverables***
- `respond` fallback: on any OpenAI exception for `find_employees`, returns the employee list with `match_reason: null` for all entries and emits WARNING
- `retrieve` embedding failure: propagates as HTTP `500`; existing `skills_search_index` data is never mutated
- Unit tests for both fallback paths asserting correct response shape and log emission

#### T7.3 — Integration test

***Description***
- End-to-end test: seed known `skills_search_index` rows for two employees, call `POST /search` with a query that should match one employee more strongly, assert:
  - Response type is `"employee_list"`
  - Top result's `employee_id` matches the expected employee
  - `score` of top result is above `0.7`
  - `match_reason` is a non-empty string
- Teardown removes all seeded rows

***Deliverables***
- End-to-end test passing on a clean DB with two seeded employees; asserts top-ranked employee, score threshold, and non-empty `match_reason`
- Teardown is unconditional (runs even on test failure)

---

## Dependency Order

```
T1.1
T1.1 → T2.1 → T2.2
T2.2 → T3.1
T3.1 → T4.1
T4.1 → T5.1 → T5.2
T5.2 → T6.1
T6.1 → T7.3
T2.1–T5.2 → T7.1, T7.2
```

Phases 1–5 must be complete before Phase 6. Phase 7 runs in parallel with Phase 6 and wraps up last.

---

## Open Questions

1. **Embedding call** — does `search/retrieve.py` call the in-process embedding function directly (same FastAPI app), or call the internal `/embed` HTTP endpoint? Affects latency and coupling between the ETL and query modules.
2. **Score threshold** — `0.5` is proposed as the default for `others` count queries. Should this be tuned per intent, or is a single global threshold sufficient?
3. **LLM response format for `find_employees`** — should GPT-4.1 mini return a structured JSON array (for reliable parsing) or free-text `match_reason` strings only (simpler prompt)?
4. **Pagination** — the spec returns up to 100 chunks from pgvector. Should the API expose `limit` / `offset` parameters, or is a fixed cap acceptable for the current 60-employee dataset?
5. **Auth** — is `POST /search` public (any logged-in user) or restricted to specific roles? Affects T6.1 middleware.

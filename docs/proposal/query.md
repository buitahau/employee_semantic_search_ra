# Query — Detail Specification

The query layer handles incoming search requests.. It accepts a natural language query and/or structured filter parameters, converts the query text into a vector embedding, and retrieves ranked employee matches from the database.

---

## Processing Steps

When a search query arrives, it passes through the following steps before a response is returned.

```
User Query
    │
    ▼
Normalization                               (Step 1)
    │
    ▼
Prompt Rewrite + Intent + Heuristic + Filter  (Step 2)
    │
    ▼
Hybrid Retrieval (Vector + Filters)         (Step 3)
    │
    ▼
Employee Aggregation + Sorting by Score     (Step 4)
    │
    ▼
Full Record Hydration from Source DB        (Step 5a)
    │
    ▼
Deterministic Logic OR LLM Interpretation   (Step 5b)
    │
    ▼
Response
```

---

### Step 1 — Normalize prompt

Clean the raw input the same way ETL normalizes source text — consistent input produces consistent embeddings.

| Operation | Detail |
|---|---|
| Lowercase | Reduce token variance for the embedding model |
| Trim & collapse whitespace | Remove leading/trailing spaces and repeated spaces |
| Unify punctuation | Normalize curly quotes, dashes, and encoding variants to ASCII equivalents |
| Skip sentinels | Reject empty strings, `"null"`, `"undefined"` — return an error immediately |

---

### Step 2 — AI prompt rewrite

Pass the normalized prompt to a small LLM (GPT-4.1 mini) to produce a structured output used by all subsequent steps.

The model:
- Corrects typos and grammar (`"developper"` → `"developer"`)
- Expands abbreviations (`"FE"` → `"frontend"`, `"BE"` → `"backend"`)
- Removes redundant filler (`"Can you tell me who..."` → `"who..."`)

**Output schema:**

```json
{
  "intent":    "find_employees | others",
  "query":     "<rewritten text used to generate the embedding in Step 3>",
  "heuristic": "<plain-language description of how to interpret or compute the final result>",
  "filter":    { "<metadata key>": "<value>" }
}
```

| Field | Description |
|---|---|
| `intent` | `find_employees` — run vector search and return a ranked employee list. `others` — the query can be answered without vector search (counts, lookups, out-of-scope). |
| `query` | Clean, keyword-dense rewrite of the prompt. Fed directly to the embedding model in Step 3. |
| `heuristic` | Instruction for Step 5 on how to interpret the pgvector results — e.g. `"count distinct employees"`, `"return top 5 by score"`, `"list skills of the matched employee"`. |
| `filter` | Structured constraints to apply as a GIN filter in Step 3 — e.g. `{"skills": ["Java"], "field_type": "experience"}`. Empty if no filter applies. |

**Example** (input: `"who has java backend and good english"`):

```json
{
  "intent":    "find_employees",
  "query":     "Java backend developer good English communication",
  "heuristic": "rank employees by score descending; include employees with English proficiency evidence",
  "filter":    { "skills": ["Java"] }
}
```

**Example** (input: `"how many full-stack developers do we have?"`):

```json
{
  "intent":    "others",
  "query":     "full-stack developer",
  "heuristic": "count distinct matched employees above score threshold",
  "filter":    {}
}
```

---

### Step 3 — Embed & search pgvector

Embed the rewritten query text from Step 2 using `all-MiniLM-L6-v2` (same model and pipeline as ETL Step 5) to produce a 384-dim L2-normalized vector.

Run cosine similarity search against `skills_search_index`:

```sql
SELECT
  employee_id,
  chunk_text,
  metadata,
  1 - (embedding <=> :query_vector) AS score
FROM skills_search_index
WHERE metadata @> :structured_filters   -- optional, from Step 2
ORDER BY score DESC
LIMIT 100;
```

Structured filters extracted in Step 2 (e.g. `{"skills": ["Java"]}`) are applied as a GIN `@>` condition to narrow candidates before similarity scoring. There is no `field_type` filter — all chunks for an employee live in the same pool.

---

### Step 4 — Collect & group results

pgvector returns one row per chunk. Multiple chunks belong to the same employee — from different sources (CV, experience, training, task) all in the same pool.

Aggregate per employee:
- Group by `employee_id`.
- Take the **max score** across all chunks as the employee's relevance score.
- Union all `skills` arrays across chunks and deduplicate.
- Collect matching `chunk_text` values as evidence for Step 5b.

**Output** — a list of employees sorted by score descending:

```json
[
  { "employee_id": 12, "score": 0.91, "skills": ["Java", "Spring Boot"], "chunks": ["..."] },
  { "employee_id": 7,  "score": 0.84, "skills": ["Java", "Hibernate"],   "chunks": ["...", "..."] },
  { "employee_id": 34, "score": 0.76, "skills": ["Java", "Node.js"],     "chunks": ["..."] }
]
```

---

### Step 5 — Fetch full data, compute & format response

#### 5a — Fetch full records from the source database

The `ai_search_text` and `metadata` already stored in `skills_search_index` (produced during ETL Steps 2–3) are sufficient context for the LLM in Step 5b — no need to re-fetch raw source text. Only display-ready and structured data that is not in the index needs to be fetched from `owt-employee-app-backend`.

| Source | What to fetch | Why |
|---|---|---|
| `users` | Name, position, avatar, contact | Display fields, not in the index |
| `user_skills` + `skills` | Skill list with proficiency levels (0–5) | Structured proficiency data, not embedded |
| `skills_search_index` | `ai_search_text`, `metadata` per chunk | Already available from Step 4 — reuse directly as LLM context |

#### 5b — Compute & format based on intent

**`find_employees`** — pass the full employee records, their scores, and the `heuristic` from Step 2 to GPT-4.1 mini:

- The model uses the `heuristic` to re-rank, filter, or interpret the results.
- Generates a human-readable `match_reason` per employee using the full record as context.
- Returns a ranked list.

**`others`** — apply the `heuristic` from Step 2 directly to the Step 4 list, no LLM needed:

- `"count distinct matched employees above score threshold"` → return a single integer.
- `"list skills of the matched employee"` → return the skill list from `user_skills` for the top-matched employee.
- Any heuristic simple enough to evaluate programmatically is handled here without an LLM call.

---

## Example Input & Output

The endpoint accepts a free-text natural language query. The response shape depends on the intent of the query.

---

### Find employees by skill / requirement

**Input:**
```
"Who has Java backend experience and good English?"
```

**Output** — ranked list of matching employees:

| # | Employee | Skills | Match reason |
|---|---|---|---|
| 1 | Nguyen Van A | Java, Spring Boot, English (C1) | Strong Java backend, English proficiency confirmed in CV |
| 2 | Tran Thi B | Java, Hibernate, English (B2) | Java backend experience, intermediate English |
| 3 | Le Van C | Java, Node.js, English (B1) | Java experience, basic English |

---

### Aggregate / count query

**Input:**
```
"How many full-stack developers do we have?"
```

**Output** — single number:

```
8
```

---

### Skill lookup for a specific employee

**Input:**
```
"Skills of John"
```

**Output** — skill list for the matched employee:

| Skill | Proficiency | Source |
|---|---|---|
| React | Advanced (4/5) | user_skills |
| Node.js | Intermediate (3/5) | user_skills |
| TypeScript | Intermediate (3/5) | experience (ShopCore) |
| PostgreSQL | Intermediate (3/5) | experience (ShopCore) |
| Docker | Beginner (2/5) | experience (ShopCore) |

---

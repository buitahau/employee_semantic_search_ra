# ETL

The ETL pipeline extracts raw employee data, transforms it into text chunks, generates vector embeddings, and loads them into pgvector. It runs on initial load and incrementally as source data changes.

---

## When

The pipeline is triggered in three cases:

1. **Hook trigger** — database hooks fire whenever a source entity (CV, experience record, training log, employee profile) is created, updated, or deleted. The affected employee is re-indexed immediately.

2. **Scheduled reconciliation** — a periodic job scans for employees whose source data has not been indexed or whose index state is stale. This acts as a safety net to catch any records that were missed during hook processing (e.g. due to a transient failure or a bug in the pipeline itself).

3. **Manual indexing** — an admin can trigger re-indexing on demand, either for the entire employee dataset or for a single employee. Useful for recovery after a pipeline issue or after bulk data migrations.

---

## Dependencies

| Tool | Role |
|---|---|
| **pgvector** | PostgreSQL extension that stores and queries `VECTOR(384)` embeddings in `skills_search_index` |
| **all-MiniLM-L6-v2** | Embedding model (ONNX runtime); converts `chunk_text` into 384-dim vectors at index time and query time |
| **GPT-4.1 mini** | Strips boilerplate and filler from `normalized_text` while preserving all skills, tools, project names, domains, dates, and outcomes — producing a compact `ai_search_text` that improves embedding quality without distorting the original signal |

The `ai_search_text` and `metadata` produced here are reused directly by the query layer — see [query.md](query.md).

---

## Source Entities

Entities extracted from `owt-employee-app-backend` that feed the indexing pipeline, grouped by field_type.

Legend: **text** = embedded as raw content · *meta* = stored as metadata for filtering/display

---

### cv

**`user_cvs` (CvEntity)**

| Field | Type | Role |
|---|---|---|
| `cv` | text | **text** — primary CV content, main chunk source |
| `user` (FK) | relation | *meta* — identifies the employee |

**`cv_overview` (CvOverviewEntity)**

| Field | Type | Role |
|---|---|---|
| `introduction` | text | **text** — free-text self-introduction |
| `customPosition` | varchar 255 | **text** — custom job title declared by the employee |
| `user` (FK → `user_id`) | relation | *meta* — identifies the employee |

---

### experience

**`experiences` (ExperienceEntity)**

| Field | Type | Role |
|---|---|---|
| `projectName` | varchar 256 | **text** — project name |
| `domain` | varchar 256 | **text** — industry / domain (e.g. e-commerce, fintech) |
| `description` | varchar 1024 | **text** — project description |
| `rolesAndResponsibilities` | text | **text** — key semantic content, what the employee actually did |
| `dateFrom` | date | *meta* — tenure start, used for display/filtering |
| `dateTo` | date (nullable) | *meta* — tenure end |
| `isCurrentlyWorking` | boolean | *meta* — indicates active engagement |
| `isSelected` | boolean | *meta* — employee-curated flag; only `isSelected = true` entries are indexed |
| `user` (FK) | relation | *meta* — identifies the employee |

**`experience_skills` (ExperienceSkillEntity)**

| Field | Type | Role |
|---|---|---|
| `experienceId` | number | *meta* — join key to `experiences` |
| `skillId` | number | *meta* — join key to `skills`; resolved to `skill.name` for text |

**`employment_histories` (EmploymentHistoryEntity)**

| Field | Type | Role |
|---|---|---|
| `company` | varchar 256 | **text** — employer name |
| `dateFrom` | date | *meta* — employment start |
| `dateTo` | date (nullable) | *meta* — employment end |
| `isCurrentlyWorking` | boolean | *meta* — indicates active employment |
| `isSelected` | boolean | *meta* — only `isSelected = true` entries are indexed |
| `userId` | number | *meta* — identifies the employee |

---

### training

**`trainings` (TrainingEntity)**

| Field | Type | Role |
|---|---|---|
| `trainingTitle` | varchar 256 (nullable) | **text** — title of the training session |
| `trainingDescription` | varchar 1024 (nullable) | **text** — what was covered |
| `trainingDate` | date | *meta* — when the training took place |
| `duration` | number | *meta* — session length in hours |
| `topic` (FK → `training_topics`) | relation | *meta* — resolved to `topic.label` and appended to text |
| `level` (FK → `training_levels`) | relation | *meta* — resolved to `level.label` and appended to text |
| `user` (FK → `user_id`) | relation | *meta* — identifies the employee |

**`training_topics` (TrainingTopicEntity)** — joined, not indexed directly

| Field | Type | Role |
|---|---|---|
| `label` | varchar 100 (nullable) | **text** — topic name appended to the training chunk |

**`training_levels` (TrainingLevelEntity)** — joined, not indexed directly

| Field | Type | Role |
|---|---|---|
| `label` | varchar 100 (nullable) | **text** — level name appended to the training chunk |

---

### task

**`task_assignments` (TaskAssignmentEntity)**

| Field | Type | Role |
|---|---|---|
| `title` | string | **text** — task title |
| `details` | string | **text** — task description / body |
| `priority` | enum (CRITICAL/HIGH/MEDIUM/LOW) | *meta* — stored as metadata, not embedded |
| `status` | enum (OPEN/IN_PROGRESS/DONE) | *meta* — stored as metadata, not embedded |
| `categoryId` | number | *meta* — resolved to `category.label` and appended to text |

**`task_assignments_assignees` (TaskAssignmentAssigneeEntity)**

| Field | Type | Role |
|---|---|---|
| `taskAssignmentId` | number (PK) | *meta* — join key to `task_assignments` |
| `userId` | number (PK) | *meta* — identifies the employee |

**`task_assignments_categories` (TaskAssignmentCategoryEntity)** — joined, not indexed directly

| Field | Type | Role |
|---|---|---|
| `label` | enum (ADMIN/HR/INFRA/EMPLOYEE_APP/BUDDIES) | **text** — category name appended to the task chunk |

---

### Supporting entities (join targets)


**`skills` (SkillEntity)**

| Field | Type | Role |
|---|---|---|
| `name` | varchar 255 | **text** — skill name resolved from `experience_skills.skillId` |
| `group` (FK) | relation | *meta* — skill group, may be appended for context |

**`user_skills` (UserSkillEntity)**

| Field | Type | Role |
|---|---|---|
| `skill` (FK) | relation | *meta* — resolved to `skill.name` |
| `level` | int 0–5 | *meta* — proficiency level, used for structured filter search |
| `isSelected` | boolean | *meta* — only `isSelected = true` entries are indexed |

---

## Transform

Each employee's extracted raw text goes through the following steps before it is written to `skills_search_index`.

### Source record (used across all examples below)

Employee ID 42, `field_type = experience`. Raw `rolesAndResponsibilities` as stored in the database (from a rich-text editor):

```
<p>I&rsquo;m a <strong>Full-Stack Developer</strong> working on the &ldquo;ShopCore&rdquo;
project&nbsp; &nbsp;(2021&ndash;2023).</p>
<ul>
  <li>Build   product  catalog &amp;  checkout  services  using  React,  Node.js</li>
  <li>Integrated  Stripe  payment  gateway&#46;  Reduced  checkout  latency  by  30%.</li>
  <li>Managed  PostgreSQL  schema  migrations  and  deployed  on  AWS  ECS.</li>
  <li>I am a hardworking team player who enjoys coding and always tries my best.</li>
  <li>Led migration of legacy monolith to microservices&#46; Defined service boundaries,
      wrote ADRs, onboarded 2 junior devs&#46;</li>
  <li>Used TypeScript, Docker, and GitHub Actions CI/CD.</li>
</ul>
```

Source metadata: `dateFrom = 2021-03-01`, `dateTo = 2023-08-31`, `projectName = “ShopCore”`, `domain = “e-commerce”`, linked skills: `React, Node.js, TypeScript, PostgreSQL, AWS`.

---

### Step 1 — Normalize text

Clean the raw text so later steps see consistent, model-friendly input. Applied identically at index time and query time — any mismatch is a silent correctness bug.

| Operation | Detail |
|---|---|
| Strip HTML | CV and experience content may come from a rich-text editor; tags eat the token budget without semantic value |
| Normalize whitespace | Collapse runs of spaces, tabs, newlines, zero-width chars into single spaces |
| Skip sentinels | Never process `”null”`, `”undefined”`, `”None”`, or empty strings — skip the record entirely |
| Unify punctuation | Normalize curly quotes, dashes, and encoding variants to their ASCII equivalents |

**Do NOT apply:** stop-word removal, stemming/lemmatization, manual lowercasing (the tokenizer handles it), punctuation stripping (sentence boundaries help pooling), or spell correction (corrupts rare tokens like `”Vue”` → `”Value”`).

**Result after Step 1** (`normalized_text`):

```
I'm a Full-Stack Developer working on the “ShopCore” project (2021-2023).
Build product catalog & checkout services using React, Node.js.
Integrated Stripe payment gateway. Reduced checkout latency by 30%.
Managed PostgreSQL schema migrations and deployed on AWS ECS.
I am a hardworking team player who enjoys coding and always tries my best.
Led migration of legacy monolith to microservices. Defined service boundaries, wrote ADRs, onboarded 2 junior devs.
Used TypeScript, Docker, and GitHub Actions CI/CD.
```

HTML tags removed, entity references decoded (`&rsquo;` → `'`, `&amp;` → `&`, `&#46;` → `.`), repeated spaces collapsed, non-breaking spaces removed.

---

### Step 2 — Optional AI cleanup

Use a small instruction-tuned LLM to create `ai_search_text`, a compact search-optimized version of the normalized text.

The model must preserve all skills, tools, frameworks, domains, project names, role names, dates, outcomes, certifications, and uncommon terms. It may remove boilerplate, duplicated phrases, formatting artefacts, and generic filler.

Do not use the AI output as the only source of truth. Store both `normalized_text` and `ai_search_text`. Downstream embedding should use `ai_search_text`, enriched with extracted skills and important original terms.

Use AI only to:

- remove boilerplate and repeated filler
- normalize messy CV prose
- keep all named entities, skills, tools, project names, domains, dates, outcomes
- produce a compact “search text”

GPT-4.1 mini / GPT-4o mini style model is enough for cleanup/extraction. No need for a large reasoning model.

**Result after Step 2** (`ai_search_text`, input is `normalized_text` from Step 1):

```
Full-Stack Developer, ShopCore project, e-commerce, 2021-2023.
Built product catalog and checkout with React, Node.js; integrated Stripe, reduced checkout latency 30%.
PostgreSQL migrations, AWS ECS deployment.
Microservices migration: defined service boundaries, ADRs, onboarded 2 junior devs.
TypeScript, Docker, GitHub Actions CI/CD.
```

Filler sentence (“I am a hardworking team player...”) removed. All skills, project name, domain, dates, and measurable outcomes preserved.

---

### Step 3 — Detect metadata

Before chunking, extract structured facts from the rewritten text and the source record. These are stored in the `metadata` JSONB column alongside each chunk — never embedded in `chunk_text`.

**Fixed fields** (every chunk, regardless of source):

| Field | Type | Source |
|---|---|---|
| `employee_id` | int | source record FK |
| `skills` | `string[]` | resolved from `experience_skills`, `user_skills`, or AI extraction |
| `date_from` | `string\|null` | `YYYY-MM` from source dates |
| `date_to` | `string\|null` | `YYYY-MM` from source dates, null if ongoing |

**Source-specific fields** (included when present in the source record):

| Source | Extra metadata fields |
|---|---|
| cv | `”position”` (customPosition), `”summary”` (first sentence of introduction) |
| experience | `”project”` (projectName), `”domain”`, `”years”` (int, computed from dateFrom/dateTo) |
| training | `”title”` (trainingTitle), `”topic”` (topic.label), `”level”` (level.label) |
| task | `”title”` (task title), `”category”` (category.label) |

**Result after Step 3** (extracted from the source record and `ai_search_text` from Step 2):

```json
{
  “employee_id”: 42,
  “skills”: [“React”, “Node.js”, “TypeScript”, “PostgreSQL”, “AWS”, “Docker”, “GitHub Actions”],
  “date_from”: “2021-03”,
  “date_to”: “2023-08”,
  “project”: “ShopCore”,
  “domain”: “e-commerce”,
  “years”: 2
}
```

`skills` is the union of linked `experience_skills` (React, Node.js, TypeScript, PostgreSQL, AWS) and skills extracted by the AI from `ai_search_text` (Docker, GitHub Actions). `years` is computed from `dateFrom`/`dateTo`. No `field_type` — all sources for an employee share the same chunk pool.

---

### Step 4 — Chunk

Split the rewritten text into overlapping token-bounded windows. Target size is **200 tokens** — within `all-MiniLM-L6-v2`'s `max_seq_length` of 256, leaving headroom for the source-type prefix.

| Parameter | Value |
|---|---|
| Chunk target | 200 tokens |
| Overlap | 20–25% of chunk size (~40–50 tokens) |
| Boundary rule | Prefer sentence/paragraph boundaries; fall back to token split only if necessary |
| Prefix | Prepend a short source-type label to each chunk (e.g. `”Experience: “`, `”Training: “`) to give the model context |

**Chunking workflow:**

1. Tokenize the rewritten text using the model tokenizer to get accurate token counts.
2. Detect sentence boundaries; tag each sentence with its token count.
3. Accumulate sentences until adding the next would exceed 200 tokens; emit the chunk at the last sentence boundary.
4. Start the next chunk by retaining the last ~40–50 tokens (overlap window) from the previous chunk.
5. For large single blocks (no sentence boundaries), split recursively at paragraph → sentence → token level until within limits.

**Result after Step 4** (input is `ai_search_text` from Step 2; the full text fits in one model window here, so 2 chunks are emitted only to demonstrate overlap):

Chunk 0:
```json
{
  “chunk_index”: 0,
  “chunk_text”: “Experience: Full-Stack Developer, ShopCore project, e-commerce, 2021-2023. Built product catalog and checkout with React, Node.js; integrated Stripe, reduced checkout latency 30%. PostgreSQL migrations, AWS ECS deployment.”,
  “token_count”: 48,
  “char_start”: 0,
  “char_end”: 221,
  “preprocess_version”: 1
}
```

Chunk 1 (overlap carries the last sentence of Chunk 0 into the next window):
```json
{
  “chunk_index”: 1,
  “chunk_text”: “Experience: PostgreSQL migrations, AWS ECS deployment. Microservices migration: defined service boundaries, ADRs, onboarded 2 junior devs. TypeScript, Docker, GitHub Actions CI/CD.”,
  “token_count”: 40,
  “char_start”: 175,
  “char_end”: 354,
  “preprocess_version”: 1
}
```

The metadata object from Step 3 is merged into every emitted chunk row before it is written to `skills_search_index`.

Each emitted chunk carries provenance fields that are merged into the `metadata` object from Step 3 before being written to `skills_search_index`:

| Field | Description |
|---|---|
| `chunk_index` | Sequential integer across all chunks for `(employee_id, field_type)`, starting at 0 |
| `chunk_text` | The prose window, with source-type prefix prepended |
| `token_count` | Actual token count of this chunk — stored in `metadata` for diagnostics |
| `char_start` / `char_end` | Character offsets into the rewritten text — stored in `metadata` for debugging |
| `preprocess_version` | Integer version of the preprocessing rules used — stored in `metadata`; bump when rules change to trigger a rebuild |

---

### Step 5 — Encode

Embed each `chunk_text` with `all-MiniLM-L6-v2` via the internal embedding service.

Pipeline: tokenize → ONNX inference → mean pooling (real tokens only, not padding) → L2 normalize → 384-dim vector.

The resulting vector is stored in the `embedding VECTOR(384)` column of `skills_search_index`.

**Verification:**
- Embed the same string twice → cosine similarity must equal `1.0` (determinism + normalization check).
- Cross-check ONNX output against `sentence-transformers` reference within ~1e-5 per dimension.
- Round-trip through pgvector: insert one known embedding, query for it, similarity must be `1.0`.

---

## Load

After Transform (Steps 1–5), each chunk — now carrying its `chunk_text`, `embedding`, `metadata`, and provenance fields — is written to `skills_search_index`.

### Table: `skills_search_index`

```sql
CREATE TABLE skills_search_index (
  id              BIGSERIAL PRIMARY KEY,
  employee_id     INT          NOT NULL,
  chunk_index     INT          NOT NULL,
  chunk_text      TEXT         NOT NULL,
  normalized_text TEXT,
  ai_search_text  TEXT,
  embedding       VECTOR(384)  NOT NULL,
  metadata        JSONB        NOT NULL DEFAULT '{}',
  indexed_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),

  UNIQUE (employee_id, chunk_index)
);

CREATE INDEX ON skills_search_index USING GIN (metadata);
```

`field_type` is not a column — all chunks for an employee (from CV, experience, training, task) share the same pool, keyed only by `employee_id`. `preprocess_version`, `token_count`, `char_start`, and `char_end` are stored inside `metadata` as diagnostic fields.

### Write strategy

On each indexing run for an employee, the pipeline:

1. Deletes all existing rows for `employee_id`.
2. Re-extracts and re-chunks all sources (CV, experience, training, task) for that employee.
3. Inserts the freshly computed chunks in a single transaction.

This avoids partial state: either the full new index is present, or the old one is. Never a mix. Because all sources are re-indexed together, there is no risk of stale chunks from one source surviving alongside fresh chunks from another.

### Example — final rows loaded for employee 42

The two chunks produced in Step 4 and encoded in Step 5 become two rows:

**Row 1 (chunk_index = 0):**

| Column | Value |
|---|---|
| `employee_id` | `42` |
| `chunk_index` | `0` |
| `chunk_text` | `"Experience: Full-Stack Developer, ShopCore project, e-commerce, 2021-2023. Built product catalog and checkout with React, Node.js; integrated Stripe, reduced checkout latency 30%. PostgreSQL migrations, AWS ECS deployment."` |
| `embedding` | `[0.0312, -0.0451, 0.0178, ..., 0.0289]` *(384 floats, L2-normalized)* |
| `metadata` | `{"employee_id":42,"skills":["React","Node.js","TypeScript","PostgreSQL","AWS","Docker","GitHub Actions"],"date_from":"2021-03","date_to":"2023-08","project":"ShopCore","domain":"e-commerce","years":2,"preprocess_version":1,"token_count":48,"char_start":0,"char_end":221}` |
| `indexed_at` | `2025-05-14T08:23:11Z` |

**Row 2 (chunk_index = 1):**

| Column | Value |
|---|---|
| `employee_id` | `42` |
| `chunk_index` | `1` |
| `chunk_text` | `"Experience: PostgreSQL migrations, AWS ECS deployment. Microservices migration: defined service boundaries, ADRs, onboarded 2 junior devs. TypeScript, Docker, GitHub Actions CI/CD."` |
| `embedding` | `[0.0198, -0.0374, 0.0521, ..., -0.0112]` *(384 floats, L2-normalized)* |
| `metadata` | `{"employee_id":42,"skills":["React","Node.js","TypeScript","PostgreSQL","AWS","Docker","GitHub Actions"],"date_from":"2021-03","date_to":"2023-08","project":"ShopCore","domain":"e-commerce","years":2,"preprocess_version":1,"token_count":40,"char_start":175,"char_end":354}` |
| `indexed_at` | `2025-05-14T08:23:11Z` |

# V1 PROPOSAL — REVIEW & IMPROVEMENT NOTES

Reviewer: hbuita@owt.swiss
Date: 2026-05-12
Status: Feedback on `docs/proposal/v1` — input for v2

---

## 1. OVERALL VERDICT

V1 is a strong first pass. The tech choices (pgvector, all-MiniLM-L6-v2, onnxruntime, FastAPI, two-tier phased delivery) are well-reasoned and proportionate to a 60–70-employee internal tool. The proposal correctly avoids over-engineering (no extra vector DB service, no IVFFlat index, no pagination, no config table for weights).

The gaps are mostly in **specification rigor**, not in direction. Before implementation, v2 needs to close ambiguities around: scoring math, stack boundary (NestJS vs Python), query-side embedding flow, indexing upsert semantics, and a handful of cross-reference errors. Sections below are ordered by impact.

---

## 2. CRITICAL GAPS (MUST FIX BEFORE BUILDING)

### 2.1 Scoring math is underspecified

The formula `final_score = (keyword_score × 0.6) + (semantic_score × 0.4)` only works if both scores are on the same scale. V1 does not define:

- **How `keyword_score` is computed.** Is it `matched_skills / requested_skills`? Level-weighted (`sum(level) / max_possible`)? Boolean (1 if all match, else 0)?
- **How `semantic_score` is computed.** Raw cosine similarity (range −1..1)? Re-scaled to 0..1? Best chunk per employee, or aggregated?
- **How chunks aggregate per employee.** If an employee has 5 matched chunks, do we take `max`, `mean`, or `top-k mean`? `max` favors one-hit wonders; `mean` dilutes; `top-3 mean` is usually the right compromise.

**Recommendation (v2):**
- Define `keyword_score ∈ [0, 1]` explicitly. Suggest level-weighted match ratio:
  `Σ(min(emp_level, requested_min_level)) / Σ(requested_min_level)` clipped to 1.0.
- Define `semantic_score = (cosine_sim + 1) / 2` so it sits in [0, 1].
- Aggregate chunks per employee with `top-3 mean` (or `max` if simplicity wins — pick one and write it down).
- Add a worked example: one employee, three matched chunks, requested skills, computed final score.

### 2.2 Stack boundary is ambiguous (NestJS vs Python)

Section 3.3 says "the project is migrating from NestJS to Python + FastAPI" and "NestJS calls it via HTTP during the transition." Section 8 then shows the module in TypeScript (`.ts` files, `src/modules/...`). Two unanswered questions:

- **Where is Tier 1 built?** If migration is in flight, building Tier 1 in NestJS only to rewrite it in Python is the throwaway work the proposal claims to avoid.
- **Who owns the indexing pipeline?** `indexing.service.ts` (NestJS) chunks text and calls Python `/embed`, but it also writes to a Postgres table that the Python service queries. That's two services writing to the same vector table — fine, but should be explicit.

**Recommendation (v2):** Pick one of:
- **(A)** Build the entire skills-search module in Python/FastAPI from day 1, even if the rest of the app is still NestJS. NestJS proxies the search endpoint through. This matches the "no throwaway work" principle stated for the embedding service.
- **(B)** Build Tier 1 in NestJS now, accept that semantic_search.service + indexing.service will be rewritten in Python during migration. State this explicitly as accepted throwaway.

State which one, and why.

### 2.3 Query-side embedding flow is missing

V1 describes how source text gets embedded into the index but never explicitly says: **the search query itself must also be embedded at request time** by calling `/embed` with `free_text`. The Python service therefore serves two paths (index-time and query-time embedding), and the latency budget for a search request now includes one `/embed` round-trip.

**Recommendation (v2):**
- Add a sequence diagram or numbered steps for a Tier 2 search request:
  1. NestJS receives `POST /api/v1/skills-search`.
  2. NestJS runs Tier 1 keyword filter → candidate `employee_ids`.
  3. NestJS calls Python `/embed` with `free_text` → query vector.
  4. NestJS issues pgvector `ORDER BY embedding <=> $1` restricted to candidate `employee_ids`.
  5. NestJS combines scores, hydrates result cards, returns.
- State expected total latency budget (e.g., <500ms p95) and which step dominates.

### 2.4 Skill names are not embedded — biggest semantic miss

This is a free win that v1 misses. With ~hundreds of skills in the `skills` table, embedding each skill name once gives you free-text → structured-skill expansion:

- User types `"javascript backend framework"` → cosine-similar skills: `Node.js`, `Express`, `NestJS` → silently add to the keyword filter.

This bridges the gap between Tier 1 and Tier 2 and dramatically improves the case where the admin doesn't know the exact skill name.

**Recommendation (v2):** Add `skills` as a fifth `field_type` (or a separate small table `skills_embeddings`). Embedded on skill creation/edit. Used as a pre-filter expansion step when `free_text` is present.

### 2.5 Indexing upsert semantics not defined

When an experience row is updated, does the indexing service:
- DELETE all rows in `skills_search_index` where `(employee_id, field_type='experience', source_id=X)` then INSERT new chunks?
- Or UPSERT by some natural key?

V1 doesn't say. This matters because re-chunking can change the number of chunks for a single source row, so a naive UPSERT-by-id breaks.

**Recommendation (v2):** Add an explicit unique constraint `UNIQUE (employee_id, field_type, source_id, chunk_index)` and state the refresh strategy as **delete-then-insert for that (employee_id, field_type, source_id) tuple**, wrapped in a transaction.

Also: `source_id` is `INT` but is `NULL` for `field_type='cv'`. The unique constraint above needs to handle that (Postgres treats NULLs as distinct by default — usually fine, but call it out).

---

## 3. CORRECTNESS / SPEC BUGS

### 3.1 Cross-reference errors

| Location | Issue |
|---|---|
| Section 7 | API endpoint body refers to `Section 4.1 parameters` and `Section 4.1 + 4.2`. These are actually Section 5.1 and 5.2. |
| Section 5.3 (sort_by) | Says "See sort options in Section 5". Sort options live in Section 6.2. |

Trivial but signals haste. Fix in v2.

### 3.2 Token-to-char estimate is optimistic

V1 says "varchar 1024 ≈ ~200 tokens, safe" for `roles_and_responsibilities`. For English text, ~4 chars/token is typical, so 1024 chars ≈ **256 tokens** — right at the model's hard limit, with no safety margin. Code with identifiers, dates, or special characters tokenizes denser (closer to ~3 chars/token).

**Recommendation (v2):** Tokenize and measure before assuming. Add a chunker that explicitly counts tokens (the same tokenizer used by the model) and splits at 240 tokens (≈ 256 minus a small safety margin). Don't trust char counts.

### 3.3 `source_id` is not a real FK and can orphan

`source_id INT` is just a tag, not a foreign key. If a `trainings` row is hard-deleted (admin error, manual SQL, etc.), the corresponding index rows are orphans. ON DELETE CASCADE only applies to `users(id)` removal.

**Recommendation (v2):** Either
- Add explicit hooks (`@AfterRemove` on each source entity) that delete matching index rows, OR
- Build a periodic reconciliation job that prunes orphans (cheap at this scale).

Pick one and document it.

### 3.4 `cv_overview.introduction` may be empty for many employees

V1 punts on this. If `introduction` is empty, the CV "match source" is silently dead for that employee — they'll never surface on a CV-based semantic match even if `cv.cv` has rich content.

**Recommendation (v2):** Add a fallback policy:
- If `introduction` is empty but `cv.cv` exists, extract the first ~240 tokens as a CV chunk.
- OR chunk the entire `cv.cv` document into multiple chunks (one row per chunk, `chunk_index` column added). This costs ~3–8 rows per employee — negligible at 60 employees.

### 3.5 Edge case: keyword filter returns zero, free_text is set

V1 says "Both → Keyword filters first → semantic reranks survivors." If survivors are empty, no semantic ranking happens, and free_text becomes useless. Is this intended? Probably not — the admin likely wants the system to fall back to pure semantic when their structured filter is too tight.

**Recommendation (v2):** Define the fallback behavior. Suggested rule:
- If `free_text` is set AND keyword survivors == 0, ignore keyword filter and return top-N semantic matches with a flag in the response (`fallback_used: true`) so the UI can show "no exact skill matches; showing semantic matches."

---

## 4. ARCHITECTURE & DESIGN IMPROVEMENTS

### 4.1 Add a `chunk_index` column to the index table

Currently `(employee_id, field_type, source_id)` is the natural key for a logical source. If chunking strategy ever splits one source into multiple chunks (e.g., long CVs, long task details), you need `chunk_index` to distinguish them and to support delete-then-insert refresh cleanly.

```sql
chunk_index INT NOT NULL DEFAULT 0,
UNIQUE (employee_id, field_type, source_id, chunk_index)
```

Cheap to add now, painful to add later.

### 4.2 Add an initial bulk index plan

V1 does not describe how the existing 60–70 employees get into `skills_search_index` on day one of Phase 2. The `/index/rebuild` endpoint exists but isn't tied to the rollout plan.

**Recommendation (v2):** Add a "Bootstrapping" subsection: on Phase 2 deploy, run `/index/rebuild` once. State expected duration (60 employees × ~5 chunks × ~30ms ≈ 10 seconds).

### 4.3 Result hydration risks N+1

Each result card pulls position, seniority, all skills (collapsed), matched experiences, matched trainings. Without explicit eager-loading or a single hydration query, this is N+1 territory.

**Recommendation (v2):** Note that the result hydration uses a single `IN (...)` query per related table, joined client-side in the service. Or use TypeORM `relations` / Python equivalent — but call it out so reviewers don't approve a naive N+1 implementation.

### 4.4 Observability is missing entirely

For an internal tool, you don't need full SRE-grade dashboards, but you do want:
- Embedding service: request count, p50/p95 latency, error rate.
- Search endpoint: request count, p95 latency, fallback frequency.
- Index lag: count of failed background re-indexes (the "fire and forget with error logging" path).

**Recommendation (v2):** Add a one-paragraph section on logging/metrics. Even just structured logs with `event_type` is enough at this scale.

### 4.5 Test plan is E2E-only

Section 11 lists end-to-end scenarios but no unit tests for:
- Chunker (token counting, truncation, splitting).
- Score combiner (keyword + semantic normalization, weights).
- Indexing service (delete-then-insert idempotency).
- Embedding service client (timeout, retry, error handling).

**Recommendation (v2):** Split Section 11 into "Unit tests" and "Integration / E2E tests."

### 4.6 Access control should be assumed, not "pending"

Section 9 lists "Admin-only — pending stakeholder confirmation." This data (CVs, salaries-adjacent info, who-knows-what) is plainly HR-sensitive. The default has to be admin-gated; if a stakeholder later says "let everyone use it," that's a config flip.

**Recommendation (v2):** State "Admin-only by default. A guard is implemented in Phase 1. If broader access is later approved, lift the guard." Don't ship without a guard.

---

## 5. DETAILED DESIGN SPECIFICATIONS

This section captures concrete design decisions discussed during review. These are not gaps in v1 — they are specifications v2 should adopt verbatim or push back on with reasoning.

### 5.1 `chunk_text` format: natural-language prose, with a sidecar `metadata JSONB` column

**Question raised during review:** Should `chunk_text` be free-form prose like `"Java 5 years in banking domain"`, or pre-processed into JSON like `{"skill":"Java","years":5,"domain":"banking"}` before embedding?

**Answer: keep prose for the embedded field. Add a separate `metadata JSONB` column for structured facts.**

Why JSON in `chunk_text` is worse:

1. **Token waste.** Braces, quotes, colons, commas, and repeated keys consume 30–40% of the 256-token budget on syntactic noise. Less actual content per chunk.
2. **Distribution mismatch.** `all-MiniLM-L6-v2` was trained on prose (Reddit, Quora, StackExchange, web pages). It has never seen JSON during training. Retrieval quality drops measurably (typically 5–15%) when input format diverges from training data.
3. **Query/index asymmetry.** The admin types `"React developer with e-commerce experience"` — natural prose. If the index is JSON but the query is prose, cosine similarity compares vectors from two different distributions. Worst case for retrieval quality.

The genuine value of structured data is not semantic — it's **filtering, boosting, and display**:

- `Java` → already in `user_skills` table → Tier 1 SQL filter, no embedding needed.
- `5 years` → derivable from `experiences.start_date / end_date` → SQL filter.
- `banking domain` → no structured column → this is where embedding helps.

So structured facts belong in real columns (or a sidecar JSONB), not inside the embedded text.

**Recommended schema addition:**

```sql
ALTER TABLE skills_search_index
  ADD COLUMN metadata JSONB;

CREATE INDEX idx_skills_search_metadata ON skills_search_index USING GIN (metadata);
```

Example row for an experience:

```text
chunk_text = "Experience. Banking core platform: built REST APIs in Java and
              Spring Boot over 5 years at a tier-1 bank, handling payment
              reconciliation and fraud rules."

metadata   = {
  "skills": ["Java", "Spring Boot", "REST"],
  "years":  5,
  "domain": "banking",
  "project_name": "Banking core platform"
}
```

What this buys you:

- **Embedding quality preserved** — `chunk_text` stays in the model's training distribution.
- **Cheap filtering** — `WHERE metadata->>'domain' = 'banking'` with the GIN index.
- **Better result cards** — display "matched on: Java, 5 yrs, banking" without re-parsing the chunk.
- **Score boosting** — `final_score` can add a small bonus when `metadata.skills` intersects requested skills, even if cosine similarity alone wouldn't rank the row high.

**Middle-ground option — template-canonicalized prose.** If consistency across employees matters more than expressivity, generate `chunk_text` from a template at index time (e.g., `"[ProjectName]: used [Skill1], [Skill2] for [N] years in [Domain] domain. Responsibilities: [roles_and_responsibilities]."`). Still prose, but predictable. Probably overkill at 60 employees — start with raw prose + `metadata JSONB`.

**Comparison:**

| Approach | Embedding quality | Filter power | Verdict |
|---|---|---|---|
| JSON in `chunk_text` | Worse — model wasn't trained on it | Same as columns | **No** |
| Prose only | Good | Limited to SQL on source tables | OK |
| **Prose + `metadata JSONB`** | **Good** | **Strong** | **Yes** |
| Template prose + JSONB | Good, more consistent | Strong | Defer; add only if needed |

### 5.2 Query-side embedding pipeline (free text → pgvector query)

The full request flow for a Tier 2 search, expanding on Section 2.3. The embedding service serves two paths (index-time and query-time); this section specifies the query-time path in detail.

**Stage 0 — Service load-time setup (once at startup):**

```python
from onnxruntime import InferenceSession
from tokenizers import Tokenizer

session   = InferenceSession("model.onnx", providers=["CPUExecutionProvider"])
tokenizer = Tokenizer.from_file("tokenizer.json")
tokenizer.enable_truncation(max_length=256)
tokenizer.enable_padding(length=256)
```

Load once, reuse for every request.

**Stage 1 — Tokenize the free text:**

```python
def tokenize(text: str):
    enc = tokenizer.encode(text)
    return {
        "input_ids":      np.array([enc.ids],            dtype=np.int64),
        "attention_mask": np.array([enc.attention_mask], dtype=np.int64),
        "token_type_ids": np.array([enc.type_ids],       dtype=np.int64),
    }
```

Produces `input_ids` (with `[CLS]=101` prepended and `[SEP]=102` appended), `attention_mask` (1 for real tokens, 0 for padding), and `token_type_ids` (all zeros for single-sentence input). Input beyond 256 tokens is silently truncated.

**Stage 2 — Run ONNX inference:**

```python
def run_model(inputs):
    outputs = session.run(None, inputs)
    return outputs[0]   # shape: [1, 256, 384] — one 384-dim vector per token
```

The model produces a **per-token** embedding. You don't want 256 vectors — you want one. That's what pooling is for.

**Stage 3 — Mean pooling (the step that's easy to get wrong):**

You want the average of token embeddings, **but only over real tokens** — padding must be excluded, or short queries get systematically wrong embeddings.

```python
def mean_pool(token_embeddings, attention_mask):
    mask = attention_mask[..., np.newaxis].astype(np.float32)  # [1, 256, 1]
    summed = (token_embeddings * mask).sum(axis=1)             # [1, 384]
    counts = mask.sum(axis=1).clip(min=1e-9)                   # [1, 1]
    return summed / counts
```

The single most common bug when re-implementing sentence-transformers manually is naïve `mean(axis=1)` which averages over padding.

**Stage 4 — L2 normalize:**

```python
def l2_normalize(vec):
    norm = np.linalg.norm(vec, axis=1, keepdims=True).clip(min=1e-9)
    return vec / norm
```

After this `||vec|| = 1`. Two reasons this matters:

1. `sentence-transformers` normalizes by default. Skip it on either side and cosine similarity will look broken without obvious cause.
2. For unit vectors, cosine distance and L2 distance produce the same ranking — pgvector's `<=>` and `<->` agree.

**Stage 5 — Return vector to caller:**

```python
@router.post("/embed")
def embed(req: EmbedRequest, token: str = Header(..., alias="X-Internal-Token")):
    if token != settings.INTERNAL_TOKEN:
        raise HTTPException(401)
    inputs     = tokenize(req.text)
    token_embs = run_model(inputs)
    pooled     = mean_pool(token_embs, inputs["attention_mask"])
    normalized = l2_normalize(pooled)
    return {"vector": normalized[0].tolist()}   # length 384
```

CPU latency budget for one short query: **~5–20 ms** total (ONNX inference dominates). For hot queries, drop static padding and use dynamic ONNX shapes; an 8-token query then runs in ~1–2 ms.

**Stage 6 — Use the vector in a pgvector query (caller side):**

```ts
const { vector } = await embeddingClient.embed(freeText);
const literal = `[${vector.join(",")}]`;   // pgvector wire format

const rows = await db.query(`
  SELECT
    s.employee_id, s.field_type, s.source_id, s.chunk_text,
    1 - (s.embedding <=> $1::vector) AS similarity
  FROM skills_search_index s
  JOIN users u ON u.id = s.employee_id
  WHERE u.is_active = true
    AND ($2::int[] IS NULL OR s.employee_id = ANY($2))   -- keyword survivors
  ORDER BY s.embedding <=> $1::vector
  LIMIT 200;
`, [literal, keywordSurvivorIds ?? null]);
```

Key points:

- **Pass the vector as a string literal cast to `::vector`.** Most drivers won't auto-encode arrays into pgvector's wire format; build the string yourself.
- **`<=>` is cosine distance** (0 = identical, 2 = opposite). Smaller is better, so `ORDER BY ... <=>` ascending. `1 - distance` converts to similarity in `[−1, 1]`.
- **Filter before sorting.** Pushing `employee_id = ANY($2)` into the `WHERE` clause restricts the scan to keyword-filter survivors — the explicit "Tier 1 filter → Tier 2 rerank" implementation.
- **`LIMIT 200`** caps chunks pulled before aggregation. You still need to collapse chunks → employees in application code.

**Stage 7 — Aggregate chunks to employees:**

```ts
const byEmployee = new Map<number, number[]>();
for (const r of rows) {
  if (!byEmployee.has(r.employee_id)) byEmployee.set(r.employee_id, []);
  byEmployee.get(r.employee_id)!.push(r.similarity);
}

const semanticScores = new Map<number, number>();
for (const [empId, sims] of byEmployee) {
  const top3 = sims.sort((a, b) => b - a).slice(0, 3);
  const mean = top3.reduce((s, v) => s + v, 0) / top3.length;
  semanticScores.set(empId, (mean + 1) / 2);   // remap [-1,1] → [0,1]
}
```

That `semanticScores` map feeds into `keyword_score × 0.6 + semantic_score × 0.4` (Section 2.1).

**Verification checklist when wiring this up:**

- **Idempotency:** embed a string twice → cosine similarity must equal `1.0` (within float epsilon). If not, normalization or determinism is broken.
- **Cross-check against reference:** embed the same string with `SentenceTransformer("all-MiniLM-L6-v2").encode(text, normalize_embeddings=True)` and your ONNX path. They should match within ~1e-5 per dimension. If not, mean-pooling or input tensors are wrong.
- **Round-trip through pgvector:** insert one known embedding, query for it, similarity must be `1.0`. Catches encoding-format bugs.

Skip any of these and you risk shipping a search that "works" but returns subtly wrong rankings — the hardest class of bug to spot after the fact.

### 5.3 Text preprocessing pipeline (apply to both index and query)

Modern sentence transformers are robust to raw text. Heavy preprocessing usually hurts more than it helps. The pipeline below is intentionally minimal.

**Necessary (data hygiene):**

```python
import re
from html import unescape

def strip_html(text: str) -> str:
    text = unescape(text)                  # &nbsp; → space, &amp; → &
    text = re.sub(r"<[^>]+>", " ", text)   # drop tags
    return text

def normalize_whitespace(text: str) -> str:
    text = text.replace("​", "").replace("﻿", "")  # zero-width, BOM
    return re.sub(r"\s+", " ", text).strip()

def is_embeddable(text: str) -> bool:
    return bool(text and text.strip() and
                text.strip().lower() not in {"null", "none", "n/a"})

def truncate_to_tokens(text: str, max_tokens: int = 240) -> str:
    ids = tokenizer.encode(text).ids
    if len(ids) <= max_tokens:
        return text
    truncated  = tokenizer.decode(ids[:max_tokens])
    last_stop  = truncated.rfind(".")
    return truncated[:last_stop + 1] if last_stop > len(truncated) * 0.5 else truncated
```

Why each one:

- **Strip HTML/Markdown** — if CVs/experiences come from a rich-text editor, tags eat the 256-token budget without semantic value.
- **Normalize whitespace** — collapses runs of spaces, tabs, newlines, zero-width chars.
- **Skip empty/sentinel values** — never embed `"null"`, `"undefined"`, `"None"`. Skip the chunk entirely.
- **Token-aware truncation** — char-based estimates are unreliable (see Section 3.2). Use the actual tokenizer and prefer sentence-boundary cuts.

**Recommended (small wins):**

- **Source-type prefix** — `"Experience. ..."`, `"Training. ..."`, `"Task. ..."`, `"About. ..."` (CV). The model has seen these patterns during training and uses them as soft hints. This is a degenerate form of template-canonicalization.
- **Skill alias canonicalization** — if you maintain an alias table (`"JS" → "JavaScript"`, `"Postgres" → "PostgreSQL"`), apply it on both index and query sides. Cheap recall win.
- **URL / email replacement** — marginal. `re.sub(r"https?://\S+", "[URL]", text)` saves tokens if your data is link-heavy.

**Anti-patterns — do NOT do these:**

| Anti-pattern | Why it hurts |
|---|---|
| **Stop-word removal** | Negations and prepositions change meaning. `"experience with banking"` ≠ `"experience banking"`. |
| **Stemming / lemmatization** | WordPiece tokenization already handles morphology. Stemming destroys signal. |
| **Manual lowercasing** | `all-MiniLM-L6-v2` is uncased — the tokenizer does this internally. For a *cased* model it would actively hurt. |
| **Punctuation stripping** | Sentence boundaries help pooling. `"Java. 5 years."` ≠ `"Java 5 years"`. |
| **Spell correction** | False corrections corrupt rare tokens (esp. names and tech terms — "Vue" → "Value"). |
| **Aggressive synonym replacement** | Beyond a curated alias table, manual replacement is brittle. Let the embedder do it. |

**Critical rule — query side and index side must match:**

Whatever preprocessing applies at index time must also apply to the query before calling `/embed`. Build one shared function and call it from both paths:

```python
def preprocess(text: str, alias_map: dict | None = None) -> str | None:
    if not is_embeddable(text):
        return None
    text = strip_html(text)
    text = normalize_whitespace(text)
    if alias_map:
        text = canonicalize_skills(text, alias_map)
    return truncate_to_tokens(text, 240)
```

Five lines. Applied identically to index-time chunks and query-time free text. Anything beyond this is over-engineering at 60 employees.

**Version your preprocessing:**

If preprocessing rules change, existing index rows were built under the old rules. Queries embedded under new rules will silently mis-match.

```sql
ALTER TABLE skills_search_index
  ADD COLUMN preprocess_version SMALLINT NOT NULL DEFAULT 1;
```

When the version bumps, schedule a rebuild via `/index/rebuild`. Pair with the `model_version` column suggested in Section 6 (Nice-to-Have).

**Project-specific concern — Vietnamese text:**

The working dir is `openvn`. If any CV introductions, training descriptions, or task details land in Vietnamese, `all-MiniLM-L6-v2` will produce poor embeddings (English-only training data). Options:

- **(A)** Detect language at index time (`langdetect` / `fasttext-langdetect`); if non-English, skip and log.
- **(B)** Swap to `paraphrase-multilingual-MiniLM-L12-v2` — still 384 dims, drop-in compatible, handles 50+ languages including Vietnamese. About 2× slower on CPU but acceptable at this volume.

Worth deciding before Phase 2 — changing the model = full reindex.

---

## 6. NICE-TO-HAVE / FOLLOW-UPS

These can be deferred but are worth listing as known follow-ups in v2's "Future Work":

- **Query result caching.** Memoize the (free_text → vector) call for ~5 minutes; identical queries are common ("React developer", "Node senior") and embedding the query is the slowest step.
- **Synonym / alias table for skills.** "JS" → "JavaScript", "Postgres" → "PostgreSQL". Cheaper than embedding for the long tail of common shorthand.
- **A/B comparison harness for Phase 2.** Run Tier 1 and Tier 2 side-by-side on a logged query set and let the admin pick which ranking is better.
- **Re-ranking with a cross-encoder.** all-MiniLM is a bi-encoder; a small cross-encoder reranker on the top-20 can sharply improve quality. Defer until baseline is in.
- **Index versioning.** A `model_version TEXT` column on `skills_search_index` so swapping the embedding model is a clean rebuild rather than an ambiguous mix.
- **Internationalization.** All current text is English. If skill names or descriptions land in Vietnamese, the embedding model needs to be multilingual (paraphrase-multilingual-MiniLM is the drop-in).

---

## 7. SUMMARY: V2 ACTION LIST

In rough priority order:

1. Define `keyword_score` and `semantic_score` formulas explicitly; pick a chunk aggregation rule (recommend top-3 mean).
2. Decide stack: build skills-search module in Python from day 1, or accept NestJS-first throwaway. State which.
3. Adopt the query-side embedding pipeline in Section 5.2 (tokenize → ONNX → mean-pool → L2-normalize → pgvector); state latency budget (~5–20 ms embed + pgvector query at this scale).
4. Embed skill names; use them for free-text → skill expansion.
5. Define indexing upsert semantics: delete-then-insert per `(employee_id, field_type, source_id)`; add `chunk_index` column and unique constraint.
6. Adopt `chunk_text` = natural-language prose, plus a `metadata JSONB` sidecar column for structured facts (Section 5.1). Do **not** embed JSON.
7. Adopt the minimal preprocessing pipeline in Section 5.3, applied identically to index and query; add `preprocess_version` column.
8. Decide Vietnamese handling: detect-and-skip vs. swap to `paraphrase-multilingual-MiniLM-L12-v2`. Decide before Phase 2.
9. Fix cross-references (Section 7 and 5.3 of v1 point to wrong sections).
10. Replace char-based token estimates with actual tokenizer counts; chunk at 240 tokens.
11. Define orphan-cleanup strategy for hard-deleted source rows.
12. Add fallback rule for "keyword filter empty + free_text present."
13. Add fallback rule for empty `cv_overview.introduction`.
14. Add initial bulk-index plan for Phase 2 rollout.
15. Mark admin-only access as required, not pending.
16. Split test plan into unit and E2E sections — include verification checklist from Section 5.2 (idempotency, sentence-transformers cross-check, pgvector round-trip).
17. Add a short observability section (metrics + structured logs).
18. Note hydration strategy (single IN-query per related table).

Items 1–8 are blockers (now including chunk_text format, preprocessing, and language handling). Items 9–18 are quality improvements that don't change the architecture.

# ADR-0001: Embedding Model and Dimension Selection

**Status**: Accepted (Revised 2026-06-10 — extended 15-model benchmark)

**Date**: 2026-06-10

**Context**: Research Q1 — Which embedding model and dimension are most suitable for the employee skills search use case?

---

## Context

### Problem

Employee app requires skills-based semantic search for ~60 employees across CVs and job descriptions. Core query patterns:

- **Skills matching**: "Python developer", "React", frameworks, tools, libraries
- **Role matching**: "senior backend engineer", "data scientist"
- **Document corpus**: CVs (typically 1,000–3,000 tokens) and JDs (500–1,500 tokens)

Skills search spans two demanding domains:

- **Written** — CVs and JDs are formal written documents with structured career narrative
- **Programming** — Technical skill terms require code-domain semantics to match synonymous tool names

### Deployment Constraints

| Constraint | Value |
|------------|-------|
| Inference | CPU-only ONNX runtime |
| Vector DB | PostgreSQL + pgvector |
| Scale | ~60 employees, low query volume |
| Latency SLA | < 500ms P95 |
| Language | English primary, Vietnamese roadmap |

### Benchmark

**Extended benchmark**: 15 models, 16 MTEB domains, 9 scoring criteria.

- **Data source**: MTEB Leaderboard, collected 2026-06-04
- **Scoring scenario**: Balanced (Search Quality 55% / Operational Cost 45%) — correct for CPU-only deployment where efficiency is a real constraint but not a hard bottleneck at 60-employee scale
- **Domain composite for this use case**: Written 60% + Programming 40% (reflects corpus composition — CVs are primarily written documents with embedded technical sections)

Full methodology in [references.md](../q1-embedding-model-by-domain/references.md).

**Top 6 models — App Composite Score (Balanced scenario)**

| Model | Written | Programming | **App Score** | License |
|-------|:-------:|:-----------:|:-------------:|:-------:|
| snowflake-arctic-embed-l-v2.0 | 82.62 | 84.77 | **83.48** | Apache-2.0 |
| **bge-m3** | 83.55 | 82.84 | **83.27** | MIT |
| multilingual-e5-large | 78.40 | 82.57 | 80.07 | MIT |
| snowflake-arctic-embed-m-v2.0 | 75.17 | 81.99 | 77.90 | Apache-2.0 |
| multilingual-e5-base | 76.27 | 80.03 | 77.77 | MIT |
| multilingual-e5-small | 74.65 | 78.40 | 76.15 | MIT |

App Score = 0.6 × Written + 0.4 × Programming (Balanced scenario final scores).

---

## Decision

**Adopt `BAAI/bge-m3` with 1024-dimensional embeddings.**

---

## Rationale

### Why bge-m3 over snowflake-arctic-embed-l-v2.0

App composite scores are within 0.25 points (83.27 vs 83.48). The two models are equivalent on active params (0.31B), embedding dimension (1024), and max tokens (~8,192). Tiebreakers all favor bge-m3:

**1. STS 74.12 — highest of all 15 models (+4 points over snowflake-l)**

STS (Semantic Textual Similarity) is the MTEB metric most directly aligned with skills search quality: it measures whether semantically equivalent phrases — "Python 3 developer" and "backend engineer with Python expertise" — are embedded close together. bge-m3 leads every other model on this metric.

**2. Written domain advantage (83.55 vs 82.62)**

CVs and JDs compose 60% of the corpus weight. bge-m3 wins the Written domain. snowflake-l's Programming lead (84.77 vs 82.84) is outweighed by its Written deficit.

**3. Multilingual coverage**

bge-m3 supports 100+ languages per its model card (note: the benchmark data column may show "EN only" due to a collection artifact — the HuggingFace model card explicitly documents multilingual support). Vietnamese expansion requires no model change.

**4. MIT license**

More permissive than Apache-2.0 for internal tooling with no attribution requirements.

### Why 1024 dimensions

At 60 employees × ~20 chunks each = 1,200 vectors, the storage delta between 384-dim and 1024-dim is **2.9 MB** — negligible.

| Dimension | Storage (1,200 vectors × 4B/float) | Note |
|:---------:|:----------------------------------:|------|
| 384 | 1.8 MB | Current floor |
| 768 | 3.5 MB | +1.7 MB |
| **1024** | **4.7 MB** | **+2.9 MB** |

The representation capacity of a 1024-dim space is meaningfully larger than 384-dim. At this data scale, there is no operational reason to constrain to a lower dimension.

### Why Balanced scenario

At 60 employees and low query volume, latency and memory are not binding constraints. CPU-only is a deployment reality, not a capacity ceiling. Balanced (55/45) correctly reflects this: efficiency shapes the tradeoff but does not override retrieval quality.

### Why Max Tokens matters here

CVs frequently exceed 512 tokens. At 8,194 max tokens, bge-m3 can embed a full CV as a single vector — preserving full skill context across sections (experience, education, skills). Models with 512-token limits require mid-document chunking that fragments skill mentions across embedding boundaries, degrading retrieval quality for multi-skill queries.

---

## Consequences

### Positive

1. **Best STS quality (74.12/100)** across the full 15-model benchmark — the most coherent embedding space for skills matching
2. **Full CV ingestion without chunking**: 8,194 max tokens handles even long CVs as single embeddings, preserving end-to-end skill context
3. **Multilingual ready**: 100+ language support — Vietnamese expansion requires no model change
4. **No query prefix required**: unlike the E5 model family, bge-m3 performs correctly without "query:"/"passage:" prefixes, reducing prompt-engineering surface area

### Negative

1. **Schema migration required**: pgvector vector column must be updated to 1024 dimensions; existing embeddings must be re-indexed
   - One SQL migration + one re-index run, ~5–15 minutes for 60 employees

2. **CPU inference latency**: ~300–500ms per query at 0.31B active params on commodity CPU
   - Within the <500ms SLA; verify on target hardware before production deploy
   - int8 quantization halves inference time if margin is tight

3. **Larger model file**: ~1.2 GB ONNX (or ~600 MB int8 quantized)
   - One-time artifact download; not a runtime memory cost

### Risks

| Risk | Severity | Mitigation |
|------|:--------:|------------|
| P95 latency exceeds 500ms on production CPU | Medium | Benchmark on target hardware first; use int8 quantized ONNX variant |
| pgvector migration corrupts existing index | Low | Validate in staging; backup vector DB before applying to production |
| bge-m3 ONNX unavailable or runtime issues | Low | snowflake-arctic-embed-l-v2.0 is a 0.25-point drop and same model size — drop-in fallback |

---

## Implementation

**Scope**: 1 SQL migration + 3 file changes

### 1. SQL migration

```sql
-- Drop and recreate vector column at 1024 dims
ALTER TABLE employee_embeddings
  DROP COLUMN embedding;
ALTER TABLE employee_embeddings
  ADD COLUMN embedding vector(1024);
```

### 2. `common/constants.py`

```python
PREPROCESS_VERSION = 3  # bge-m3 1024-dim
EMBEDDING_DIM = 1024
```

### 3. `.env`

```
EMBEDDING_MODEL_PATH=models/bge-m3/model.onnx
EMBEDDING_DIM=1024
```

### 4. `common/embedding.py`

Remove any E5-family query/passage prefix logic — bge-m3 does not use prefixes.

### Deployment steps

1. Download ONNX model from `BAAI/bge-m3` on HuggingFace (prefer int8 quantized for CPU)
2. Apply SQL migration in staging; verify vector column shape
3. Update `.env` and `constants.py`; bump `PREPROCESS_VERSION`
4. Run `POST /index` — re-embeds all 60 employees (~5–15 min)
5. Run validation queries; verify Precision@3 ≥ 50%
6. Apply migration to production during off-hours

**Rollback**: revert `constants.py` + `.env`, restore vector DB backup from step 2, re-index (~15 min)

---

## Alternatives Considered

### snowflake-arctic-embed-l-v2.0 (Apache-2.0, 74 langs) — closest alternative

App score 83.48 vs 83.27. Programming domain winner (84.77 vs 82.84). Rejected because:

- STS 70.11 vs 74.12 — the primary metric for skills matching quality is 4 points lower
- Written domain deficit (82.62 vs 83.55) — primary corpus domain
- 74 language support vs 100+ — narrower multilingual coverage for future expansion
- Apache-2.0 vs MIT — less permissive

**This is the recommended fallback** if bge-m3 inference latency exceeds SLA on target hardware.

### multilingual-e5-large (MIT, 94 langs)

App score 80.07, STS 73.30. Hard disqualifier: **Max Tokens 514** — cannot embed full CVs in a single pass. Chunking at 514 tokens on a 2,000-token CV creates 4 fragments; skill mentions split across chunk boundaries are lost to multi-skill queries (e.g., "Python + AWS developer" where Python appears in experience and AWS in the skills section).

### multilingual-e5-small (MIT, 94 langs)

App score 76.15 — 7 points below bge-m3. Fastest CPU inference at 0.02B active params. Appropriate only when inference latency is a hard constraint or hardware is severely resource-constrained. The accuracy loss is not justified at 60-employee scale.

### snowflake-arctic-embed-m-v2.0 (Apache-2.0, 74 langs)

App score 77.90, STS 66.60. A 768-dim middle option — pays migration cost without reaching top-tier quality. 5+ points below top-2 on composite and 7.5 points below bge-m3 on STS. No compelling advantage over the other options.

### e5-mistral-7b-instruct (MIT)

App score 61.06. 7B parameters — CPU inference is impractical (~10–30s per query). Even with GPU, the 4096-dim storage cost is 4× bge-m3 with no accuracy gain on the relevant domains.

---

## References

- **Benchmark Index**: [../q1-embedding-model-by-domain/benchmark-data.md](../q1-embedding-model-by-domain/benchmark-data.md)
- **Balanced Scenario Results**: [../q1-embedding-model-by-domain/benchmark-data-balanced.md](../q1-embedding-model-by-domain/benchmark-data-balanced.md)
- **Methodology & Weight Allocation**: [../q1-embedding-model-by-domain/references.md](../q1-embedding-model-by-domain/references.md)
- **Term Definitions**: [../q1-embedding-model-by-domain/glossary.md](../q1-embedding-model-by-domain/glossary.md)
- **MTEB Leaderboard**: https://huggingface.co/spaces/mteb/leaderboard
- **bge-m3 Model Card**: https://huggingface.co/BAAI/bge-m3
- **snowflake-arctic-embed-l-v2.0 (fallback)**: https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0

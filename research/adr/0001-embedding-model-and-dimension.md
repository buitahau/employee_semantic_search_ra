# ADR-0001: Embedding Model and Dimension Selection

**Status**: Accepted

**Date**: 2026-06-05

**Context**: Research Q1 — Which embedding model and dimension are most suitable for each domain?

---

## Context

### Problem

Current embedding model (`all-MiniLM-L6-v2`) shows poor performance:
- MTEB Score: **32.51** (#11/11 — worst in benchmark)
- Tech Domain: **77.0** (#5/10)
- General EN: **41.8** (#7/10)

Employee app requires skills-based semantic search for ~60 employees across:
- **Tech domain (70%)**: "Python developer", "React", programming languages, frameworks
- **General EN (30%)**: CVs, job descriptions, soft skills

Current search quality is suboptimal, affecting HR productivity.

### Requirements

1. **Performance**: Significantly better retrieval accuracy (>50% improvement)
2. **Deployment**: No DB schema change (keep 384 dimensions)
3. **Efficiency**: CPU-friendly inference (<250ms per query)
4. **Future-proof**: Multilingual support for Vietnamese expansion
5. **Migration**: Low effort (<2 days implementation)

### Options Evaluated

11 models from MTEB leaderboard, scored across 8 criteria (25% MTEB, 30% Domain Score, 23% Efficiency, 22% Other).

**Weighted Score** = 0.7 × Tech + 0.3 × General EN (employee app specific)

| Model | Tech | Gen EN | Weighted | Dims | Params | DB Migration |
|-------|:----:|:------:|:--------:|:----:|:------:|:------------:|
| **multilingual-e5-small** | 88.0 | 72.9 | **83.47** | 384 | 0.022B | ✅ None |
| multilingual-e5-base | 84.2 | 61.4 | 77.36 | 768 | 0.278B | ❌ Required |
| all-mpnet-base-v2 | 83.6 | 33.5 | 68.57 | 768 | 0.109B | ❌ Required |
| ibm-granite-125m | 82.0 | 46.8 | 71.44 | 768 | 0.125B | ❌ Required |
| Snowflake Arctic | 73.3 | 53.1 | 69.24 | 1024 | 0.568B | ❌ Required |
| all-MiniLM-L6-v2 (current) | 77.0 | 41.8 | **66.44** | 384 | 0.011B | Current |

---

## Decision

**Migrate to `intfloat/multilingual-e5-small`**

### Rationale

1. **Best performance**: +25.6% weighted score (66.44 → 83.47)
   - Tech: +14.3% (77.0 → 88.0)
   - General EN: +74.4% (41.8 → 72.9)
   - MTEB: +56.5% (32.51 → 50.91)

2. **Zero DB migration**: Same 384 dimensions
   - No schema change
   - No storage increase
   - No index rebuild

3. **Lightweight**: 0.022B params (2× current, still CPU-friendly)
   - Expected inference: ~200ms (vs current ~150ms)
   - Well within <500ms SLA

4. **Future-proof**:
   - 94 languages (ready for Vietnamese)
   - MIT license (no restrictions)
   - 2024 model (vs 2020 current)

5. **Wins 6/7 domains**: Best general-purpose choice

### Implementation

**Code changes** (4 files):

1. `common/embedding.py`:
```python
def embed(text: str, prefix: str = "passage") -> list[float]:
    prefixed_text = f"{prefix}: {text}"
    # ... rest unchanged
```

2. `query/retrieve.py`:
```python
vector = embed(analysis.query, prefix="query")
```

3. `etl/load.py`:
```python
embedding = embed(chunk_text, prefix="passage")
```

4. `common/constants.py`:
```python
PREPROCESS_VERSION = 2  # Trigger re-indexing
```

**Deployment**:
1. Update `.env`: `EMBEDDING_MODEL_PATH=models/multilingual-e5-small/model.onnx`
2. Run `POST /index` to re-index (~5-10 min for 60 employees)
3. Test with 5 validation queries

**Timeline**: 1.5 days (0.5 prep + 0.5 test + 0.5 deploy)

**Rollback**: <15 minutes (revert env + re-index with old model)

---

## Consequences

### Positive

1. **+25.6% accuracy improvement** for employee search
2. **No infrastructure changes** (same 384 dims, same storage cost)
3. **Multilingual ready** (Vietnamese expansion enabled)
4. **Low risk** (quick rollback, proven model)
5. **Better HR productivity** (faster candidate matching)

### Negative

1. **Inference latency increase**: +50ms per query (150ms → 200ms)
   - Still well within <500ms SLA
   - Acceptable trade-off for +25% accuracy

2. **Prefix requirement**: E5 models REQUIRE "query:" and "passage:" prefixes
   - Without prefixes: Performance degrades to random results
   - Mitigation: Add validation tests for prefix usage

3. **Re-indexing required**: 5-10 minutes downtime for re-embedding
   - Minimal impact for ~60 employees
   - Can schedule during off-hours

### Risks

| Risk | Severity | Mitigation |
|------|:--------:|------------|
| Prefix forgotten | High | Add unit tests, validation checks |
| Inference too slow | Low | Benchmark shows <250ms, well within SLA |
| Re-indexing issues | Low | Keep old model, quick rollback |

### Metrics

Success criteria after 1 week:

| Metric | Baseline | Target | How to Measure |
|--------|:--------:|:------:|----------------|
| Precision@3 (Semantic) | 11% | **≥50%** | Test queries ("backend engineer") |
| Precision@3 (Tech keywords) | Unknown | **≥70%** | Test queries ("Python developer") |
| Response Time | ~150ms | **<250ms** | API latency P95 |
| HR Satisfaction | Baseline | **+30%** | Survey after 1 week |

---

## Alternatives Considered

### Option 2: multilingual-e5-base
- **Pros**: Slightly better Tech (84.2 vs 88.0)
- **Cons**:
  - Requires 384→768 dims migration (double storage)
  - 12.6× heavier (0.278B vs 0.022B)
  - Only +4 points better, not worth migration cost
- **Rejected**: Migration cost too high for marginal gain

### Option 3: all-mpnet-base-v2
- **Pros**: Good Tech score (83.6)
- **Cons**:
  - General EN 33.5 **worse than current** (41.8)
  - Will fail on CV searches
  - Requires 384→768 dims migration
- **Rejected**: Performance regression on General EN domain

### Option 4: Snowflake Arctic
- **Pros**: Highest MTEB (58.36)
- **Cons**:
  - Tech score 73.3 **worse than current** (77.0)
  - 25.8× heavier (0.568B params)
  - Requires 384→1024 dims migration
  - Overkill for 60 employees
- **Rejected**: Heavy model with worse domain performance

### Option 5: Keep all-MiniLM-L6-v2
- **Pros**: No changes needed
- **Cons**:
  - Worst MTEB (#11/11)
  - Poor search quality continues
  - HR productivity remains low
- **Rejected**: Status quo is unacceptable

---

## References

- **Benchmark Report**: [../q1-embedding-model-by-domain/benchmark-data.md](../q1-embedding-model-by-domain/benchmark-data.md)
- **Methodology**: [../q1-embedding-model-by-domain/references.md](../q1-embedding-model-by-domain/references.md)
- **MTEB Leaderboard**: https://huggingface.co/spaces/mteb/leaderboard
- **E5 Model**: https://huggingface.co/intfloat/multilingual-e5-small

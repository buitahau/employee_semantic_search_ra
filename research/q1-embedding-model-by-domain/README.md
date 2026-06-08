# Q1: Embedding Model Selection by Domain

**Research Question**: Which embedding model and dimension are most suitable for each domain?

**Status**: ✅ Completed
**Date**: 2026-06-05
**Decision**: [ADR-0001](../adr/0001-embedding-model-and-dimension.md)

---

## Executive Summary

**Winner**: `intfloat/multilingual-e5-small`

- Wins **6 out of 7 domains** (all except Legal)
- Same **384 dimensions** as current model (no DB migration)
- **Lightweight** (0.022B params) - 2× current but still CPU-friendly
- **Multilingual** support (94 languages)
- **MIT license**

---

## Key Findings

### Performance vs Current Model (all-MiniLM-L6-v2)

| Metric | Current | Recommended | Improvement |
|--------|:-------:|:-----------:|:-----------:|
| **MTEB Score** | 32.51 (#11/11) | 50.91 (#7/11) | **+56.5%** |
| **Tech Domain** | 77.0 | 88.0 | **+14.3%** |
| **General EN** | 41.8 | 72.9 | **+74.4%** |
| **Embed Dim** | 384 | 384 | Same |
| **Params** | 0.011B | 0.022B | 2× |

### Domain Rankings

| Domain | 🥇 Winner | Score | 🥈 Second | Score |
|--------|-----------|:-----:|-----------|:-----:|
| **Tech** | multilingual-e5-small | 88.0 | multilingual-e5-base | 84.2 |
| **General EN** | multilingual-e5-small | 72.9 | multilingual-e5-base | 61.4 |
| **Multilingual** | multilingual-e5-small | 80.6 | multilingual-e5-base | 75.3 |
| **Medical** | multilingual-e5-small | 83.5 | multilingual-e5-base | 73.5 |
| **Legal** | ibm-granite (EN) | 72.1 | paraphrase-multilingual | 65.9 |
| **Social** | multilingual-e5-small | 72.8 | multilingual-e5-base | 67.1 |
| **Scientific** | multilingual-e5-small | 54.8 | multilingual-e5-base | 50.8 |

---

## Models Evaluated

**Total**: 11 models (6 multilingual, 5 English-only)

**Data Source**: [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)

**Scoring**: 8 weighted criteria (MTEB 25%, Domain Score 30%, Efficiency 23%, Other 22%)

See [benchmark-data.md](./benchmark-data.md) for full tables.

---

## Recommendation

**Default**: `intfloat/multilingual-e5-small`

**Alternatives**:
- **Accuracy-first**: Snowflake Arctic (MTEB 58.36, but 14× heavier)
- **Pure English Tech**: all-mpnet-base-v2 (Tech 83.6, but poor General EN)
- **Long documents**: Snowflake Arctic / BAAI/bge-m3 (8192+ tokens)
- **Legal (EN only)**: ibm-granite-125m (Legal 72.1)

---

## Files

- **[benchmark-data.md](./benchmark-data.md)** - Full benchmark tables (5 tables, 11 models, 7 domains)
- **[references.md](./references.md)** - Methodology, formulas, data sources
- **[validation-results/](./validation-results/)** - Test query results for model validation
- **[../adr/0001-embedding-model-and-dimension.md](../adr/0001-embedding-model-and-dimension.md)** - Architecture Decision Record

**Raw Data**: [mteb-raw-data.md](./mteb-raw-data.md) (collected 2026-06-04)

---

## Next Steps

See [ADR-0001](../adr/0001-embedding-model-and-dimension.md) for implementation plan.

**IMPORTANT**: E5 models require text prefixes:
- Query: `"query: Python developer"`
- Document: `"passage: Alice has 5 years Python experience"`

Without prefixes, performance degrades significantly.

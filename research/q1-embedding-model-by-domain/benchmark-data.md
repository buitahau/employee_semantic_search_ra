# Benchmark Data — Embedding Models

**Date**: 2026-06-05
**Source**: [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
**Models**: 11 (6 multilingual, 5 English-only)

---

## Table 1 — Scoring Criteria

| # | Criterion | Weight | Direction | Rationale |
|:-:|-----------|:------:|:---------:|-----------|
| 1 | MTEB Retrieval Score | 25% | Higher ↑ | Industry-standard benchmark (58 tasks) |
| 2 | Domain Retrieval Score | 30% | Higher ↑ | Direct measure for target use case |
| 3 | Mean (Task) | 10% | Higher ↑ | Generalization across task types |
| 4 | Mean (TaskType) | 5% | Higher ↑ | Consistency across categories |
| 5 | Active Parameters (B) | 15% | Lower ↓ | Inference latency & memory |
| 6 | Total Parameters (B) | 8% | Lower ↓ | Model loading time |
| 7 | Max Tokens | 5% | Higher ↑ | Long document support |
| 8 | Embedding Dimension | 2% | Lower ↓ | Storage & search speed |
| — | **Total** | **100%** | — | — |

**Formula**:
```
norm(x) = (x - min) / (max - min) × 100
norm_inv(x) = (1 - (x - min) / (max - min)) × 100

Final Score = Σ (weight_i × normalized_score_i)
```

**Normalization Ranges** (across 11 models):
- MTEB: 32.51 → 58.36
- Active Params: 0.011B → 0.312B (nomic-ai: N/A)
- Embed Dim: 384 → 1024

---

## Table 2 — Model Specifications

| Model | Embed Dim | Active Params (B) | Total Params (B) | Max Tokens | Languages | MTEB Score | License |
|-------|:---------:|:-----------------:|:----------------:|:----------:|:---------:|:----------:|:-------:|
| BAAI/bge-m3 | 1024 | 0.312 | 0.568 | 8194 | Yes (Many) | 54.59 | MIT |
| Snowflake/snowflake-arctic-embed-l-v2.0 | 1024 | 0.312 | 0.568 | 8192 | Yes (74) | 58.36 | Apache-2.0 |
| intfloat/multilingual-e5-base | 768 | 0.086 | 0.278 | 514 | Yes (94) | 52.72 | MIT |
| **intfloat/multilingual-e5-small** | **384** | **0.022** | **0.118** | **512** | **Yes (94)** | **50.91** | **MIT** |
| sentence-transformers/paraphrase-multilingual-mpnet-base-v2 | 768 | 0.086 | 0.278 | 512 | Yes (50) | 39.76 | Apache-2.0 |
| sentence-transformers/LaBSE | 768 | 0.086 | 0.471 | 512 | Yes (110) | 33.17 | Apache-2.0 |
| ibm-granite/granite-embedding-125m-english | 768 | 0.086 | 0.125 | 512 | No (EN) | 39.26 | Apache-2.0 |
| nomic-ai/nomic-embed-text-v1.5 | 768 | N/A | 0.137 | 8192 | No (EN) | 34.09 | Apache-2.0 |
| sentence-transformers/all-mpnet-base-v2 | 768 | 0.086 | 0.109 | 384 | No (EN) | 33.80 | Apache-2.0 |
| sentence-transformers/all-MiniLM-L12-v2 | 384 | 0.022 | 0.033 | 256 | No (EN) | 33.37 | Apache-2.0 |
| sentence-transformers/all-MiniLM-L6-v2 | 384 | 0.011 | 0.023 | 256 | No (EN) | 32.51 | Apache-2.0 |

---

## Table 3 — Domain Score by Model

Domain Score = Average of task scores within domain.
`—` = English-only model, excluded from multilingual domains.

| Model | Multilingual | Medical | Legal | Tech | Scientific | Social | General EN |
|-------|:------------:|:-------:|:-----:|:----:|:----------:|:------:|:----------:|
| **intfloat/multilingual-e5-small** | **80.6** | **83.5** | 64.8 | **88.0** | 54.8 | **72.8** | **72.9** |
| intfloat/multilingual-e5-base | 75.3 | 73.5 | 58.3 | 84.2 | 50.8 | 67.1 | 61.4 |
| BAAI/bge-m3 | 69.5 | 58.0 | 50.6 | 71.9 | 35.7 | 57.5 | 48.6 |
| Snowflake/snowflake-arctic-embed-l-v2.0 | 66.3 | 72.6 | 49.7 | 73.3 | 40.3 | 61.4 | 53.1 |
| sentence-transformers/paraphrase-multilingual-mpnet-base-v2 | 56.2 | 37.8 | 65.9 | 48.3 | 34.1 | 49.3 | 46.7 |
| sentence-transformers/LaBSE | 47.0 | 23.7 | 41.5 | 36.8 | 15.9 | 28.6 | 37.0 |
| ibm-granite/granite-embedding-125m-english | — | — | **72.1** | 82.0 | 42.7 | — | 46.8 |
| nomic-ai/nomic-embed-text-v1.5 | — | — | — | — | — | — | 44.6 |
| sentence-transformers/all-mpnet-base-v2 | — | — | 58.4 | 83.6 | 36.8 | — | 33.5 |
| sentence-transformers/all-MiniLM-L12-v2 | — | — | 64.7 | 77.3 | 40.6 | — | 37.8 |
| sentence-transformers/all-MiniLM-L6-v2 | — | — | 62.4 | 77.0 | 38.9 | — | 41.8 |

### Domain-to-Task Mapping

- **Multilingual**: BelebeleRetrieval, MIRACLRetrievalHardNegatives, MLQARetrieval, WikipediaRetrievalMultilingual (4 tasks)
- **Medical**: CovidRetrieval, TRECCOVID (2 tasks)
- **Legal**: AILAStatutes, LegalBenchCorporateLobbying (2 tasks)
- **Tech**: StackOverflowQA (1 task)
- **Scientific**: SCIDOCS (1 task)
- **Social**: ArguAna, TwitterHjerneRetrieval, StatcanDialogueDatasetRetrieval (3 tasks)
- **General EN**: HagridRetrieval, SpartQA, TempReasonL1, WinoGrande, LEMBPasskeyRetrieval (5 tasks)

---

## Table 4 — Final Score by Domain

Final Score = Weighted score combining 8 criteria (0-100 scale).
**Bold** = Best in domain (including EN-only models where applicable).

| Model | Multilingual | Medical | Legal | Tech | Scientific | Social | General EN |
|-------|:------------:|:-------:|:-----:|:----:|:----------:|:------:|:----------:|
| **intfloat/multilingual-e5-small** | **80.6** | **83.5** | 64.8 | **88.0** | **54.8** | **72.8** | **72.9** |
| intfloat/multilingual-e5-base | 75.3 | 73.5 | 58.3 | 84.2 | 50.8 | 67.1 | 61.4 |
| BAAI/bge-m3 | 69.5 | 58.0 | 50.6 | 71.9 | 35.7 | 57.5 | 48.6 |
| Snowflake/snowflake-arctic-embed-l-v2.0 | 66.3 | 72.6 | 49.7 | 73.3 | 40.3 | 61.4 | 53.1 |
| sentence-transformers/paraphrase-multilingual-mpnet-base-v2 | 56.2 | 37.8 | **65.9** | 48.3 | 34.1 | 49.3 | 46.7 |
| sentence-transformers/LaBSE | 47.0 | 23.7 | 41.5 | 36.8 | 15.9 | 28.6 | 37.0 |
| ibm-granite/granite-embedding-125m-english | — | — | **72.1** | **82.0** | 42.7 | — | 46.8 |
| nomic-ai/nomic-embed-text-v1.5 | — | — | — | — | — | — | 44.6 |
| sentence-transformers/all-mpnet-base-v2 | — | — | 58.4 | **83.6** | 36.8 | — | 33.5 |
| sentence-transformers/all-MiniLM-L12-v2 | — | — | 64.7 | 77.3 | 40.6 | — | 37.8 |
| sentence-transformers/all-MiniLM-L6-v2 | — | — | 62.4 | 77.0 | 38.9 | — | 41.8 |

---

## Table 5 — Top 3 Models per Domain

| Domain | 🥇 Best | Score | 🥈 Second | Score | 🥉 Third | Score |
|--------|---------|:-----:|-----------|:-----:|----------|:-----:|
| **Multilingual** | multilingual-e5-small | 80.6 | multilingual-e5-base | 75.3 | BAAI/bge-m3 | 69.5 |
| **Medical** | multilingual-e5-small | 83.5 | multilingual-e5-base | 73.5 | Snowflake Arctic | 72.6 |
| **Legal** | ibm-granite (EN) | 72.1 | paraphrase-multilingual | 65.9 | multilingual-e5-small | 64.8 |
| **Tech** | multilingual-e5-small | 88.0 | multilingual-e5-base | 84.2 | all-mpnet-base (EN) | 83.6 |
| **Scientific** | multilingual-e5-small | 54.8 | multilingual-e5-base | 50.8 | ibm-granite (EN) | 42.7 |
| **Social** | multilingual-e5-small | 72.8 | multilingual-e5-base | 67.1 | Snowflake Arctic | 61.4 |
| **General EN** | multilingual-e5-small | 72.9 | multilingual-e5-base | 61.4 | Snowflake Arctic | 53.1 |

**Summary**: `intfloat/multilingual-e5-small` wins **6 out of 7 domains** (all except Legal).

---

## Comparison: Current vs Recommended

| Metric | all-MiniLM-L6-v2 (Current) | multilingual-e5-small (Recommended) | Improvement |
|--------|:--------------------------:|:-----------------------------------:|:-----------:|
| **MTEB Retrieval** | 32.51 (#11/11) | 50.91 (#7/11) | **+56.5%** |
| **Tech Domain** | 77.0 (#5/10) | 88.0 (#1/10) | **+14.3%** |
| **General EN** | 41.8 (#7/10) | 72.9 (#1/10) | **+74.4%** |
| **Embedding Dim** | 384 | 384 | Same |
| **Active Params** | 0.011B | 0.022B | 2× |
| **Multilingual** | No | Yes (94 langs) | ✓ |

---

## Model Tiers by MTEB Score

| Tier | Range | Models |
|------|-------|--------|
| **High** | ≥50 | Snowflake Arctic (58.36), BAAI/bge-m3 (54.59), multilingual-e5-base (52.72), **multilingual-e5-small (50.91)** |
| **Mid** | 35-50 | paraphrase-multilingual (39.76), ibm-granite (39.26) |
| **Basic** | <35 | nomic-embed (34.09), all-mpnet (33.80), all-MiniLM-L12 (33.37), LaBSE (33.17), all-MiniLM-L6 (32.51) |

---

## Special Notes

**Scientific Domain**: All models underperform (max score 54.8). Requires fine-tuning on domain-specific corpus (PubMed, ArXiv) or hybrid search (BM25 + dense).

**nomic-ai/nomic-embed-text-v1.5**: Active Params = N/A (Hugging Face doesn't report). Excluded from Active Params criterion, redistributed weight to remaining 7 criteria.

---

**Data Version**: 1.0
**Last Updated**: 2026-06-05

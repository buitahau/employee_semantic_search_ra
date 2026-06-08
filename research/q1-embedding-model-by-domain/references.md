# References & Methodology

**Research Question**: Which embedding model and dimension are most suitable for each domain?

**Date**: 2026-06-05

---

## Data Sources

### Primary Source

**MTEB Leaderboard** (Massive Text Embedding Benchmark)
- URL: https://huggingface.co/spaces/mteb/leaderboard
- Tasks: 58 retrieval tasks across multiple domains
- Metric: ndcg@10 (normalized discounted cumulative gain)

### Reproducible Data Collection Process

**Selection Criteria**: Models must be production-ready, popular, and benchmarked.

Applied filters on [Hugging Face Model Hub](https://huggingface.co/models):

| Filter | Value | Rationale |
|--------|-------|-----------|
| **Pipeline** | `sentence-similarity` | Correct embedding type for semantic search |
| **Library** | `sentence-transformers` | Standardized loading/serving method |
| **Other** | `text-embeddings-inference` | Ensures deployable with TEI (Text Embeddings Inference) |
| **Other** | `eval-results` | Has public benchmark scores available |
| **License** | `apache-2.0` + `mit` | Commercial use allowed (requires 2 passes, HF doesn't support multi-license filter) |
| **Sort** | `downloads` ↓ | Prioritize popular, battle-tested models |

**Reproducible URLs** (2 passes for license filter):

1. Apache 2.0 License:
```
https://huggingface.co/models?pipeline_tag=sentence-similarity&library=sentence-transformers&license=license:apache-2.0&other=text-embeddings-inference,eval-results&sort=downloads
```

2. MIT License:
```
https://huggingface.co/models?pipeline_tag=sentence-similarity&library=sentence-transformers&license=license:mit&other=text-embeddings-inference,eval-results&sort=downloads
```

**Result**: 11 models shortlisted (see [mteb-raw-data.md](./mteb-raw-data.md))

**Data Collection Date**: 2026-06-04

**Scoring Data**: Retrieved from [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) for each model.

---

### Model Sources

All models from [Hugging Face Model Hub](https://huggingface.co/models?pipeline_tag=sentence-similarity):

| Model | HuggingFace URL |
|-------|-----------------|
| intfloat/multilingual-e5-small | https://huggingface.co/intfloat/multilingual-e5-small |
| intfloat/multilingual-e5-base | https://huggingface.co/intfloat/multilingual-e5-base |
| sentence-transformers/all-MiniLM-L6-v2 | https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 |
| sentence-transformers/all-mpnet-base-v2 | https://huggingface.co/sentence-transformers/all-mpnet-base-v2 |
| Snowflake/snowflake-arctic-embed-l-v2.0 | https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0 |
| BAAI/bge-m3 | https://huggingface.co/BAAI/bge-m3 |
| ibm-granite/granite-embedding-125m-english | https://huggingface.co/ibm-granite/granite-embedding-125m-english |
| nomic-ai/nomic-embed-text-v1.5 | https://huggingface.co/nomic-ai/nomic-embed-text-v1.5 |
| sentence-transformers/paraphrase-multilingual-mpnet-base-v2 | https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2 |
| sentence-transformers/all-MiniLM-L12-v2 | https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2 |
| sentence-transformers/LaBSE | https://huggingface.co/sentence-transformers/LaBSE |

---

## Methodology

### Scoring System

**8 Weighted Criteria** (Total: 100%)

| # | Criterion | Weight | Formula | Range (min → max) |
|:-:|-----------|:------:|---------|-------------------|
| 1 | MTEB Retrieval Score | 25% | norm(x) | 32.51 → 58.36 |
| 2 | Domain Retrieval Score | 30% | norm(x) | Varies by domain |
| 3 | Mean (Task) | 10% | norm(x) | 41.39 → 59.55 |
| 4 | Mean (TaskType) | 5% | norm(x) | 35.12 → 52.17 |
| 5 | Active Parameters (B) | 15% | norm_inv(x) | 0.011 → 0.312 |
| 6 | Total Parameters (B) | 8% | norm_inv(x) | 0.023 → 0.568 |
| 7 | Max Tokens | 5% | norm(x) | 256 → 8194 |
| 8 | Embedding Dimension | 2% | norm_inv(x) | 384 → 1024 |

### Normalization Formulas

**For "higher is better" criteria** (1-4, 7):
```
norm(x) = (x - min) / (max - min) × 100
```

**For "lower is better" criteria** (5-6, 8):
```
norm_inv(x) = (1 - (x - min) / (max - min)) × 100
```

**Final Score**:
```
Final Score = Σ (weight_i × normalized_score_i)

= 0.25 × norm(MTEB)
+ 0.30 × norm(DomainScore)
+ 0.10 × norm(MeanTask)
+ 0.05 × norm(MeanTaskType)
+ 0.15 × norm_inv(ActiveParams)
+ 0.08 × norm_inv(TotalParams)
+ 0.05 × norm(MaxTokens)
+ 0.02 × norm_inv(EmbedDim)
```

### Domain Score Calculation

Domain Score = Average of task scores within domain.

**Example: BAAI/bge-m3 Multilingual Domain**
- Tasks: BelebeleRetrieval (78.16), MIRACLRetrievalHardNegatives (69.59), MLQARetrieval (74.81), WikipediaRetrievalMultilingual (89.87)
- Domain Score: (78.16 + 69.59 + 74.81 + 89.87) / 4 = **78.11**

**Example: multilingual-e5-small Tech Domain**
- Tasks: StackOverflowQA (81.94)
- Domain Score: 81.94 / 1 = **81.94**

### Domain-to-Task Mapping

| Domain | Tasks | Count |
|--------|-------|:-----:|
| **Multilingual** | BelebeleRetrieval, MIRACLRetrievalHardNegatives, MLQARetrieval, WikipediaRetrievalMultilingual | 4 |
| **Medical** | CovidRetrieval, TRECCOVID | 2 |
| **Legal** | AILAStatutes, LegalBenchCorporateLobbying | 2 |
| **Tech** | StackOverflowQA | 1 |
| **Scientific** | SCIDOCS | 1 |
| **Social** | ArguAna, TwitterHjerneRetrieval, StatcanDialogueDatasetRetrieval | 3 |
| **General EN** | HagridRetrieval, SpartQA, TempReasonL1, WinoGrande, LEMBPasskeyRetrieval | 5 |

---

## Calculation Verification

### Sample 1: MTEB Normalization

**all-MiniLM-L6-v2** (worst):
```
norm(32.51) = (32.51 - 32.51) / (58.36 - 32.51) × 100
            = 0 / 25.85 × 100
            = 0.0 ✓
```

**multilingual-e5-small**:
```
norm(50.91) = (50.91 - 32.51) / (58.36 - 32.51) × 100
            = 18.40 / 25.85 × 100
            = 71.2 ✓
```

**Snowflake Arctic** (best):
```
norm(58.36) = (58.36 - 32.51) / (58.36 - 32.51) × 100
            = 25.85 / 25.85 × 100
            = 100.0 ✓
```

### Sample 2: Active Params Normalization (inverse)

**all-MiniLM-L6-v2** (lightest):
```
norm_inv(0.011) = (1 - (0.011 - 0.011) / (0.312 - 0.011)) × 100
                = (1 - 0 / 0.301) × 100
                = 100.0 ✓
```

**multilingual-e5-small**:
```
norm_inv(0.022) = (1 - (0.022 - 0.011) / (0.312 - 0.011)) × 100
                = (1 - 0.011 / 0.301) × 100
                = (1 - 0.0365) × 100
                = 96.3 ✓
```

**Snowflake Arctic** (heaviest):
```
norm_inv(0.312) = (1 - (0.312 - 0.011) / (0.312 - 0.011)) × 100
                = (1 - 0.301 / 0.301) × 100
                = 0.0 ✓
```

### Sample 3: Domain Score Calculation

**BAAI/bge-m3 Multilingual Domain**:
- BelebeleRetrieval: 78.16
- MIRACLRetrievalHardNegatives: 69.59
- MLQARetrieval: 74.81
- WikipediaRetrievalMultilingual: 89.87

```
Domain Score = (78.16 + 69.59 + 74.81 + 89.87) / 4
             = 312.43 / 4
             = 78.11 ✓
```

**multilingual-e5-small General EN Domain**:
- HagridRetrieval: 98.55
- SpartQA: 5.43
- TempReasonL1: 0.80
- WinoGrande: 37.46
- LEMBPasskeyRetrieval: 38.25

```
Domain Score = (98.55 + 5.43 + 0.80 + 37.46 + 38.25) / 5
             = 180.49 / 5
             = 36.10 ✓
```

---

## Special Handling

### nomic-ai/nomic-embed-text-v1.5

**Issue**: Active Params = N/A (not reported on Hugging Face)

**Solution**:
- Exclude Active Params criterion (15% weight)
- Redistribute weight proportionally to remaining 7 criteria
- New weights: MTEB 29.4%, Domain 35.3%, MeanTask 11.8%, MeanTaskType 5.9%, TotalParams 9.4%, MaxTokens 5.9%, EmbedDim 2.4%

### Scientific Domain Underperformance

**Observation**: Max score only 54.8 (multilingual-e5-small)

**Root Cause**:
- SCIDOCS measures citation context understanding
- Requires deep academic domain knowledge
- Beyond capability of general-purpose embedding models

**Recommendations**:
1. Fine-tune on domain corpus (PubMed, ArXiv)
2. Use hybrid search (BM25 + dense retrieval)
3. Consider domain-specific models (SciBERT, BioBERT)

---

## Papers & Documentation

### MTEB Benchmark

**Paper**: Muennighoff et al., "MTEB: Massive Text Embedding Benchmark" (2022)
- ArXiv: https://arxiv.org/abs/2210.07316
- Tasks: 58 embedding tasks across 8 task types
- Languages: 112 languages
- Metric: Primarily ndcg@10, recall@k

### E5 Models

**Paper**: Wang et al., "Text Embeddings by Weakly-Supervised Contrastive Pre-training" (2022)
- ArXiv: https://arxiv.org/abs/2212.03533
- Key Innovation: Prefix-based training ("query:", "passage:")
- Training: 1B text pairs from web, Wikipedia, StackExchange

**IMPORTANT**: E5 models require prefixes for optimal performance:
```python
# Query
embed("query: Python developer")

# Document
embed("passage: Alice has 5 years Python experience")
```

Without prefixes, performance degrades significantly.

### Sentence Transformers

**Paper**: Reimers & Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks" (2019)
- ArXiv: https://arxiv.org/abs/1908.10084
- Framework: https://www.sbert.net/

---

## Limitations

1. **MTEB Coverage**: Benchmark may not cover all real-world use cases
2. **Domain Granularity**: Only 7 domains evaluated, actual use cases may span multiple domains
3. **Static Benchmark**: Models and leaderboard constantly evolving
4. **Efficiency Metrics**: Weights based on general assumptions, may not match specific deployment constraints
5. **Scientific Domain**: All models underperform, requires domain-specific evaluation

---

## Update History

| Version | Date | Changes |
|:-------:|------|---------|
| 2.0 | 2026-06-05 | Reorganized structure, corrected Tech/Medical rankings, added verification |
| 1.0 | 2026-06-04 | Initial benchmark report |

---

**Last Updated**: 2026-06-05

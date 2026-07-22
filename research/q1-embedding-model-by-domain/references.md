# References & Methodology

**Research Question**: Which embedding model and dimension are most suitable for each domain?

**Date**: 2026-06-09

---

## Data Sources

### Primary Source

**MTEB Leaderboard** (Massive Text Embedding Benchmark)
- URL: https://huggingface.co/spaces/mteb/leaderboard
---

### Reproducible Data Collection Process

**Platform**: [Hugging Face Model Hub](https://huggingface.co/models)

Hugging Face is the world's largest repository for sharing and discovering AI models. The filters below narrow the candidate set to embedding models suitable for semantic search / RAG, with a commercial-friendly license and publicly available benchmark scores.

#### Filter Table

| Filter | Value | Why this value |
|--------|-------|----------------|
| **Pipeline** | `feature-extraction` + `sentence-similarity` | Pipeline is the label that classifies a model by the task it performs. Both pipeline types are relevant for embedding: **Feature Extraction** is the primary task for generating embeddings/vectors used in semantic search and RAG. **Sentence Similarity** measures the degree of semantic equivalence between two texts and shares the same encoder architecture. Many high-quality models on Hugging Face are tagged under only one of the two — searching both ensures no model is missed. |
| **Library** | `sentence-transformers` | Library indicates the framework used to run the model. `sentence-transformers` is the de facto standard for embedding models, providing a unified API (`SentenceTransformer("model-id")`) that works consistently across models without custom loading code. Excluding this filter would include models requiring per-model integration work. |
| **Other** | `eval-results` | The `eval-results` tag means the model has publicly attached benchmark evaluation results in the standard MTEB format. Models without this tag have no reported benchmark scores — comparing them would require running the full MTEB suite locally, which takes several hours per model. This filter ensures all shortlisted models can be compared on equal, reproducible ground. |
| **License** | `apache-2.0` + `mit` | Licenses fall into four groups: (1) **Commercial-safe** (Apache-2.0, MIT, BSD): allow commercial use, modification, and redistribution without restriction; (2) **Commercial with conditions** (Llama3, Gemma, OpenRAIL): require additional agreements; (3) **Non-Commercial** (CC-BY-NC): prohibit commercial use; (4) **Custom** (other, apple-ascl): unclear terms. Apache-2.0 and MIT are selected as the two most common commercial-safe licenses, suitable for production deployment with no legal risk. Two separate searches are required because Hugging Face does not support multi-license filtering in a single query. |
| **Sort** | `downloads` ↓ | Download count is a reliable proxy for community validation. Widely downloaded models have been tested across many real-world use cases, are actively maintained, and are more likely to have known issues documented. Low-download models may be experimental or abandoned. |

> For a full reference of all available filter options on Hugging Face (Tasks, Libraries, Other tags), see [glossary.md — Hugging Face Filter Options](./glossary.md#hugging-face-filter-options).

#### Reproducible Search URLs (4 passes)

```
# sentence-similarity + MIT
https://huggingface.co/models?pipeline_tag=sentence-similarity&library=sentence-transformers&license=license:mit&other=eval-results&sort=downloads

# sentence-similarity + Apache-2.0
https://huggingface.co/models?pipeline_tag=sentence-similarity&library=sentence-transformers&license=license:apache-2.0&other=eval-results&sort=downloads

# feature-extraction + Apache-2.0
https://huggingface.co/models?pipeline_tag=feature-extraction&library=sentence-transformers&license=license:apache-2.0&other=eval-results&sort=downloads

# feature-extraction + MIT
https://huggingface.co/models?pipeline_tag=feature-extraction&library=sentence-transformers&license=license:mit&other=eval-results&sort=downloads
```

**Result**: 15 models shortlisted (see [mteb-raw-data.md](./mteb-raw-data.md))

**Data Collection Date**: 2026-06-04

**Scoring Data**: Retrieved from [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) for each model.

---

### Model Sources

All models from [Hugging Face Model Hub](https://huggingface.co/models):

| # | Model | HuggingFace URL |
|:-:|-------|-----------------|
| 1 | sentence-transformers/all-mpnet-base-v2 | https://huggingface.co/sentence-transformers/all-mpnet-base-v2 |
| 2 | sentence-transformers/paraphrase-multilingual-mpnet-base-v2 | https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2 |
| 3 | sentence-transformers/static-similarity-mrl-multilingual-v1 | https://huggingface.co/sentence-transformers/static-similarity-mrl-multilingual-v1 |
| 4 | sentence-transformers/LaBSE | https://huggingface.co/sentence-transformers/LaBSE |
| 5 | ibm-granite/granite-embedding-125m-english | https://huggingface.co/ibm-granite/granite-embedding-125m-english |
| 6 | nomic-ai/nomic-embed-text-v1.5 | https://huggingface.co/nomic-ai/nomic-embed-text-v1.5 |
| 7 | Snowflake/snowflake-arctic-embed-l-v2.0 | https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0 |
| 8 | Snowflake/snowflake-arctic-embed-m-v2.0 | https://huggingface.co/Snowflake/snowflake-arctic-embed-m-v2.0 |
| 9 | BAAI/bge-m3 | https://huggingface.co/BAAI/bge-m3 |
| 10 | BAAI/bge-large-en-v1.5 | https://huggingface.co/BAAI/bge-large-en-v1.5 |
| 11 | intfloat/multilingual-e5-base | https://huggingface.co/intfloat/multilingual-e5-base |
| 12 | intfloat/multilingual-e5-small | https://huggingface.co/intfloat/multilingual-e5-small |
| 13 | intfloat/multilingual-e5-large | https://huggingface.co/intfloat/multilingual-e5-large |
| 14 | intfloat/e5-mistral-7b-instruct | https://huggingface.co/intfloat/e5-mistral-7b-instruct |
| 15 | HIT-TMG/KaLM-embedding-multilingual-mini-instruct-v2 | https://huggingface.co/HIT-TMG/KaLM-embedding-multilingual-mini-instruct-v2 |

---

## Methodology

### Criteria

9 criteria across 2 groups. **Search Quality** measures how accurately the model finds and encodes meaning. **Operational Cost** measures what it costs to serve the model in a CPU-only ONNX environment.

| # | Group | Criterion | Direction | Formula | Range (min → max) |
|:-:|-------|-----------|:---------:|---------|-------------------|
| 1 | Search Quality | Domain Score | ↑ | norm(x) | Varies per domain |
| 2 | Search Quality | Retrieval | ↑ | norm(x) | 33.17 → 58.36 |
| 3 | Search Quality | STS | ↑ | norm(x) | 57.60 → 74.12 |
| 4 | Search Quality | Mean (Task) | ↑ | norm(x) | 42.56 → 60.25 |
| 5 | Search Quality | Mean (TaskType) | ↑ | norm(x) | 36.37 → 53.08 |
| 6 | Operational Cost | Active Parameters (B) | ↓ | norm_inv(x) | 0 → 6.98 |
| 7 | Operational Cost | Total Parameters (B) | ↓ | norm_inv(x) | 0.108 → 7.111 |
| 8 | Operational Cost | Max Tokens | ↑ | norm(x) | 384 → 32768 |
| 9 | Operational Cost | Embedding Dimension | ↓ | norm_inv(x) | 384 → 4096 |

> Ranges are computed across the 15 study models. Domain Score range is computed per-domain at scoring time (min/max of that domain's scores across all models).

---

### Weight Ranges

Principled min–max bounds for each criterion. No scenario may assign a weight outside these bounds.

| # | Criterion | Min | Max | Basis for Min | Basis for Max |
|:-:|-----------|:---:|:---:|---------------|---------------|
| 1 | Domain Score | 15% | 40% | Below 15%: domain-specific performance becomes decorative — the score is effectively domain-agnostic, defeating the purpose of domain benchmarking. | Above 40%: some domains cover only 1–2 tasks (Entertainment = CovidRetrieval only; Fiction = LEMBPasskeyRetrieval only). High concentration creates noise risk from a single benchmark task. |
| 2 | Retrieval | 10% | 30% | Below 10%: a model fundamentally poor at retrieval can still rank high, directly contradicting the system's purpose. | Above 30%: a general signal should not outweigh the domain-specific signal. Domain Score must remain the leading criterion. |
| 3 | STS | 5% | 20% | Below 5%: STS measures whether the embedding space faithfully encodes semantic distance — the mathematical foundation of cosine similarity search. Dropping below 5% accepts models where the vector space may be semantically meaningless. | Above 20%: high STS is necessary but not sufficient for retrieval quality. A model can have excellent STS scores on sentence pairs but poor document retrieval performance. Over-indexing on one signal is unsafe. |
| 4 | Mean (Task) | 2% | 10% | Below 2%: loses the generalization signal that catches models overfitted to specific task types. | Above 10%: highly correlated with Retrieval + STS; marginal information gain is near zero above this threshold. |
| 5 | Mean (TaskType) | 1% | 5% | Pure tiebreaker; zero would eliminate a signal that catches task-type imbalance not visible in Mean (Task). | Derived from Mean (Task) — additional weight inflates a redundant signal. |
| 6 | Active Parameters | 5% | 35% | Below 5%: CPU-only environments have hard latency limits. Even in quality-first scenarios, minimum penalty for very large models is required. | Above 35%: parameter count becomes the de facto selection criterion, overriding embedding quality entirely. |
| 7 | Total Parameters | 3% | 18% | Below 3%: a model exceeding available RAM cannot run regardless of accuracy — a minimum penalty is required in every scenario. | Above 18%: one-time startup cost should never outweigh per-query cost. Active Parameters must always carry more weight than Total Parameters. |
| 8 | Max Tokens | 4% | 15% | Below 4%: CVs and JDs routinely exceed 512 tokens. Ignoring context window capacity invites chunking overhead and context loss at chunk boundaries. | Above 15%: benefit plateaus for documents in the 1,000–3,000 token range typical of CVs. A 32,768-token window adds negligible advantage over 8,192 for this corpus. |
| 9 | Embedding Dimension | 1% | 10% | Tiebreaker for pgvector storage size and ANN search speed; cannot be entirely zero. | Dimension in the 384–4,096 range has limited quality impact. Over 10% penalizes architecturally larger models that may be significantly better at retrieval. |

**Ordering constraints** — must hold in every scenario:

| Constraint | Rationale |
|-----------|-----------|
| Domain Score ≥ Retrieval | Specific signal must outweigh general signal |
| Active Parameters ≥ Total Parameters | Per-query cost outweighs one-time startup cost |
| Mean (Task) ≥ Mean (TaskType) | Direct signal outweighs its derived counterpart |

---

### Weight Allocation by Use Case

| # | Criterion | Quality First | Cost First | Balanced |
|:-:|-----------|:-------------:|:----------:|:--------:|
| 1 | Domain Score | 35% | 20% | 22% |
| 2 | Retrieval | 22% | 13% | 17% |
| 3 | STS | 15% | 8% | 10% |
| 4 | Mean (Task) | 5% | 3% | 4% |
| 5 | Mean (TaskType) | 3% | 1% | 2% |
| — | **Search Quality** | **80%** | **45%** | **55%** |
| 6 | Active Parameters | 8% | 28% | 20% |
| 7 | Total Parameters | 4% | 12% | 10% |
| 8 | Max Tokens | 6% | 10% | 10% |
| 9 | Embedding Dimension | 2% | 5% | 5% |
| — | **Operational Cost** | **20%** | **55%** | **45%** |
| — | **Total** | **100%** | **100%** | **100%** |

> **Note**: These weights are reference values based on domain reasoning, not empirical calibration. Recalibrate against real query results before treating them as production-ready.

---

### Normalization Formulas

**For "higher is better" criteria** (Domain Score, Retrieval, STS, Mean Task, Mean TaskType, Max Tokens):
```
norm(x) = (x - min) / (max - min) × 100
```

**For "lower is better" criteria** (Active Parameters, Total Parameters, Embedding Dimension):
```
norm_inv(x) = (1 - (x - min) / (max - min)) × 100
```

All normalized scores are in [0, 100]. When a criterion value is missing (N/A), that criterion is excluded and remaining weights are rescaled proportionally.

**Final Score structure**:
```
Final Score = Σ (weight_i × norm_i)  /  Σ (weight_i for valid criteria)
```

Expanded by use case:

*Quality First — Search Quality 80% / Operational Cost 20%*
```
Final Score = 0.35×norm(DomainScore) + 0.22×norm(Retrieval) + 0.15×norm(STS)
            + 0.05×norm(MeanTask)    + 0.03×norm(MeanTaskType)
            + 0.08×norm_inv(ActiveParams) + 0.04×norm_inv(TotalParams)
            + 0.06×norm(MaxTokens)        + 0.02×norm_inv(EmbedDim)
```

*Cost First — Search Quality 45% / Operational Cost 55%*
```
Final Score = 0.20×norm(DomainScore) + 0.13×norm(Retrieval) + 0.08×norm(STS)
            + 0.03×norm(MeanTask)    + 0.01×norm(MeanTaskType)
            + 0.28×norm_inv(ActiveParams) + 0.12×norm_inv(TotalParams)
            + 0.10×norm(MaxTokens)        + 0.05×norm_inv(EmbedDim)
```

*Balanced — Search Quality 55% / Operational Cost 45%*
```
Final Score = 0.22×norm(DomainScore) + 0.17×norm(Retrieval) + 0.10×norm(STS)
            + 0.04×norm(MeanTask)    + 0.02×norm(MeanTaskType)
            + 0.20×norm_inv(ActiveParams) + 0.10×norm_inv(TotalParams)
            + 0.10×norm(MaxTokens)        + 0.05×norm_inv(EmbedDim)
```

### Domain Score Calculation

Domain Score = Average of task scores within domain (from MTEB benchmark results).

### Domain Descriptions

16 content domains derived from MTEB task metadata. Each domain groups tasks that share the same content type, allowing models to be evaluated on specific text genres.

| Domain | Tasks | Content |
|--------|:-----:|---------|
| **Academic** | 2 | Scientific papers and research documents across natural and social sciences. Dense technical text with specialized vocabulary and formal citation structure. |
| **Blog** | 3 | Informal web writing including personal blogs and opinion pieces. Sentence-level STS tasks reflect short, expressive text with varied phrasing. |
| **Encyclopaedic** | 8 | Reference content including Wikipedia articles, multilingual fact retrieval, and commonsense reasoning text. Largest task count among single-genre domains. |
| **Entertainment** | 1 | In MTEB this domain is represented by CovidRetrieval — a Chinese-language COVID news retrieval dataset. The "Entertainment" label reflects MTEB's taxonomy rather than traditional entertainment content. |
| **Fiction** | 1 | Long-form literary text. LEMBPasskeyRetrieval specifically tests retrieval of specific information buried deep in extended narratives, stressing long-context semantic understanding. |
| **Government** | 1 | Bilingual (English/French) government statistical reports and public-sector dialogue sourced from Statistics Canada. |
| **Legal** | 2 | Formal legal documents: Indian statutes (AILAStatutes) and corporate legal benchmarks (LegalBenchCorporate). Dense, formulaic language with precise legal terminology. |
| **Medical** | 2 | Clinical and biomedical literature including COVID-related medical retrieval (CovidRetrieval) and TREC COVID research documents. Overlaps with Academic domain. |
| **News** | 13 | News articles and sentence pairs across multiple languages (German, Finnish, Faroese, Spanish, Arabic, Chinese, and others). The largest non-Written domain by task count; strong multilingual signal. |
| **Non-fiction** | 2 | General informational cross-lingual non-fiction text represented by STS tasks. Broad genre with limited task coverage in this benchmark. |
| **Programming** | 1 | Technical Q&A from Stack Overflow. Mixed natural language and technical content — variable names, code snippets, error messages alongside plain-language explanations. |
| **Social** | 2 | User-generated online content: debate arguments (ArguAna) and Danish Twitter posts (TwitterHjerneRetrieval). Short-form, informal, often argumentative text. |
| **Spoken** | 2 | Transcribed and speech-derived text. STS14 includes news interview transcriptions; SemRel24STS covers spoken language across many languages. Reflects informal, fragmented sentence structure. |
| **Subtitles** | 1 | Finnish movie and TV subtitle sentence pairs (FinParaSTS). Very short text fragments with colloquial and translated language patterns. |
| **Web** | 13 | Broad general-purpose web content spanning argument retrieval, news, government documents, and general STS tasks. Most heterogeneous domain — serves as a wide-coverage signal. |
| **Written** | 27 | The most comprehensive domain. Aggregates formal written text across legal, academic, news, fiction, social, technical, and encyclopaedic genres. Overlaps significantly with all other domains. High task count makes it a reliable general written-text signal. |

> **Note**: Some tasks appear in multiple domains (e.g., CovidRetrieval is tagged as both Entertainment and Medical; STS12 appears in both Encyclopaedic and News). Domain Score for each model is the average of task scores for tasks mapped to that domain.

---

**Domain-to-Task Mapping** (16 domains, sourced from `domain_task_mapping` sheet in raw_data.xlsx):

| Domain | Tasks |
|--------|-------|
| **Academic** | SCIDOCS, TRECCOVID |
| **Blog** | STS14, STS15, STSBenchmark |
| **Encyclopaedic** | HagridRetrieval, MIRACLRetrievalHard, MLQARetrieval, SpartQA, TempReasonL1, WikipediaRetrieval, WinoGrande, STS12 |
| **Entertainment** | CovidRetrieval |
| **Fiction** | LEMBPasskeyRetrieval |
| **Government** | StatcanDialogueData |
| **Legal** | AILAStatutes, LegalBenchCorporate |
| **Medical** | CovidRetrieval, TRECCOVID |
| **News** | BelebeleRetrieval, FaroeseSTS, FinParaSTS, GermanSTSBenchmark, IndicCrosslingualSTS, STS12, STS13, STS15, STS17, STS22.v2, STSB, STSBenchmark, STSES |
| **Non-fiction** | IndicCrosslingualSTS, STS13 |
| **Programming** | StackOverflowQA |
| **Social** | ArguAna, TwitterHjerneRetrieval |
| **Spoken** | STS14, SemRel24STS |
| **Subtitles** | FinParaSTS |
| **Web** | ArguAna, BelebeleRetrieval, StatcanDialogueData, FaroeseSTS, GermanSTSBenchmark, JSICK, SICK-R, STS13, STS14, STS15, STS17, STSB, STSES |
| **Written** | AILAStatutes, ArguAna, BelebeleRetrieval, HagridRetrieval, LEMBPasskeyRetrieval, LegalBenchCorporate, MIRACLRetrievalHard, MLQARetrieval, SCIDOCS, SpartQA, StackOverflowQA, StatcanDialogueData, TempReasonL1, TwitterHjerneRetrieval, WikipediaRetrieval, WinoGrande, FaroeseSTS, FinParaSTS, GermanSTSBenchmark, JSICK, SICK-R, STS17, STS22.v2, STSB, STSBenchmark, STSES, SemRel24STS |

---

**Last Updated**: 2026-06-10

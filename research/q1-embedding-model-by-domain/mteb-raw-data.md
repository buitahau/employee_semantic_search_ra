# MTEB Raw Data — Embedding Models

**Data Collection Date**: 2026-06-04

**Source**: [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)

**Models**: 15 embedding models

---

## 1. Model Overview

| No | Model | Rank | Active Params (B) | Total Params (B) | Embed Dim | Max Tokens | Mean (Task) | Mean (TaskType) | Multilanguage | License |
|----|-------|:----:|:-----------------:|:----------------:|:---------:|:----------:|:-----------:|:---------------:|:-------------:|:-------:|
| 1 | [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) | 132 | 0.09 | 0.11 | 768 | 384 | 42.56 | 36.37 | No (EN only) | apache 2.0 |
| 2 | [paraphrase-multilingual-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2) | 77 | 0.09 | 0.28 | 768 | 512 | 51.98 | 45.17 | Yes (50 langs) | apache 2.0 |
| 3 | [static-similarity-mrl-multilingual-v1](https://huggingface.co/sentence-transformers/static-similarity-mrl-multilingual-v1) | 114 | 0 | 0.11 | 1024 | N/A | 47.24 | 41.38 | No (EN only) | apache 2.0 |
| 4 | [LaBSE](https://huggingface.co/sentence-transformers/LaBSE) | 79 | 0.09 | 0.47 | 768 | 512 | 52.07 | 45.65 | Yes (50 langs) | apache 2.0 |
| 5 | [granite-embedding-125m-english](https://huggingface.co/ibm-granite/granite-embedding-125m-english) | 121 | 0.09 | 0.12 | 768 | 512 | 44.04 | 38.09 | No (EN only) | apache 2.0 |
| 6 | [nomic-embed-text-v1.5](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) | 109 | N/A | 0.14 | 768 | 8192 | 44.10 | 37.84 | No (EN only) | mit |
| 7 | [snowflake-arctic-embed-l-v2.0](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0) | 59 | 0.31 | 0.57 | 1024 | 8192 | 57.03 | 49.95 | Yes (74 langs) | apache 2.0 |
| 8 | [snowflake-arctic-embed-m-v2.0](https://huggingface.co/Snowflake/snowflake-arctic-embed-m-v2.0) | 71 | 0.11 | 0.30 | 768 | 8192 | 53.70 | 46.89 | Yes (74 langs) | apache 2.0 |
| 9 | [bge-m3](https://huggingface.co/BAAI/bge-m3) | 48 | 0.31 | 0.57 | 1024 | 8194 | 59.55 | 52.17 | No (EN only) | mit |
| 10 | [bge-large-en-v1.5](https://huggingface.co/BAAI/bge-large-en-v1.5) | 91 | 0.30 | 0.34 | 1024 | 512 | 45.08 | 39.06 | No (EN only) | mit |
| 11 | [multilingual-e5-base](https://huggingface.co/intfloat/multilingual-e5-base) | 63 | 0.09 | 0.28 | 768 | 514 | 57.03 | 49.84 | Yes (94 langs) | mit |
| 12 | [multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small) | 66 | 0.02 | 0.12 | 384 | 512 | 56.35 | 49.45 | Yes (94 langs) | mit |
| 13 | [multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large) | 50 | 0.30 | 0.56 | 1024 | 514 | 58.61 | 51.41 | No (EN only) | mit |
| 14 | [e5-mistral-7b-instruct](https://huggingface.co/intfloat/e5-mistral-7b-instruct) | 34 | 6.98 | 7.11 | 4096 | 32768 | 60.25 | 53.08 | No (EN only) | mit |
| 15 | [KaLM-embedding-multilingual-mini-instruct-v2](https://huggingface.co/HIT-TMG/KaLM-embedding-multilingual-mini-instruct-v2) | 239 | 0.36 | 0.49 | 896 | 512 | N/A | N/A | No (EN only) | mit |

---

## 2. Model and Domain Score

| Model | Academic | Blog | Encyclopaedic | Entertainment | Fiction | Government | Legal | Medical | News | Non Fiction | Programming | Social | Spoken | Subtitles | Web | Written |
|-------|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| all-mpnet-base-v2 | 37.55 | 82.36 | 34.81 | 3.70 | 24.50 | 12.85 | 55.16 | 27.51 | 52.16 | 40.49 | 90.32 | 30.70 | 58.00 | 9.55 | 58.32 | 42.88 |
| paraphrase-multilingual-mpnet-base-v2 | 25.92 | 85.04 | 49.15 | 28.85 | 7.75 | 18.95 | 54.93 | 33.36 | 68.34 | 59.60 | 43.11 | 42.79 | 68.10 | 25.52 | 68.88 | 51.78 |
| static-similarity-mrl-multilingual-v1 | 23.13 | 78.43 | 44.95 | 45.66 | 100 | 3.02 | 50.98 | 40.51 | 60.76 | 41.17 | 50.10 | 34.46 | 62.62 | 16.82 | 63.33 | 50.96 |
| LaBSE | 10.99 | 70.96 | 44.22 | 28.60 | 20 | 4.17 | 43.05 | 22.47 | 64.08 | 60.37 | 38.23 | 24.28 | 63.15 | 24.82 | 61.86 | 47.08 |
| granite-embedding-125m-english | 46.70 | 79.34 | 37.02 | 2.98 | 38.75 | 30.71 | 61.55 | 36.12 | 52.52 | 42.01 | 89.85 | 32.16 | 58.29 | 12.42 | 60.08 | 45.91 |
| nomic-embed-text-v1.5 | 40.53 | 81.07 | 37.62 | 13.11 | 17.25 | 12.76 | 55.67 | 38.27 | 54.81 | 44.21 | 63.62 | 29.38 | 60.07 | 11.76 | 59.64 | 43.22 |
| snowflake-arctic-embed-l-v2.0 | 51.95 | 79.06 | 57.73 | 78.53 | 77.25 | 19.06 | 58.31 | 81.08 | 69.14 | 63.82 | 86.94 | 51.82 | 70.72 | 22.15 | 70.70 | 61.23 |
| snowflake-arctic-embed-m-v2.0 | 50.33 | 76.90 | 56.52 | 70.42 | 58.00 | 21.59 | 60.82 | 75.38 | 64.85 | 54.09 | 90.68 | 40.61 | 65.91 | 22.92 | 67.54 | 58.08 |
| bge-m3 | 35.52 | 83.90 | 57.75 | 77.51 | 59 | 21.86 | 59.69 | 66.12 | 73.90 | 65.86 | 80.60 | 45.93 | 72.19 | 30.43 | 73.72 | 61.45 |
| bge-large-en-v1.5 | 48.66 | 86.11 | 37.74 | 17.18 | 36.75 | 21.01 | 56.91 | 45.94 | 56.03 | 45.13 | 83.07 | 39.62 | 59.29 | 8.83 | 62.65 | 45.64 |
| multilingual-e5-base | 43.33 | 83.47 | 57.75 | 73.48 | 38.25 | 13.72 | 54.67 | 71.49 | 70.46 | 59.57 | 85.11 | 43.18 | 69.04 | 22.72 | 70.73 | 58.83 |
| multilingual-e5-small | 43.09 | 82.87 | 54.11 | 72.82 | 38.25 | 10.33 | 54.24 | 72.55 | 70.39 | 61.70 | 81.94 | 48.63 | 69.53 | 20.16 | 69.89 | 57.51 |
| multilingual-e5-large | 44.30 | 84.78 | 58.34 | 75.61 | 38.25 | 10.63 | 55.28 | 73.38 | 73.10 | 62.71 | 88.89 | 44.79 | 70.19 | 24.92 | 73.28 | 60.01 |
| e5-mistral-7b-instruct | 51.67 | 87.85 | 55.95 | 73.11 | 30.75 | 44.83 | 64.57 | 80.07 | 71.96 | 55.70 | 91.02 | 47.53 | 75.46 | 20.58 | 77.95 | 61.54 |
| KaLM-embedding-multilingual-mini-instruct-v2 | 50.04 | 85.00 | 82.27 | 83.30 | N/A | N/A | N/A | 81.29 | 81.22 | 85.96 | N/A | 57.42 | 83.50 | N/A | 77.25 | 65.12 |

---

## 3. Task Domain Reference

| No | Task Name | Task Type | Languages | Domains | Metric | Modality | Public |
|----|-----------|-----------|-----------|---------|--------|----------|--------|
| 1 | AILAStatutes | Retrieval | eng | Legal, Written | ndcg_at_10 | text | true |
| 2 | ArguAna | Retrieval | eng | Social, Web, Written | ndcg_at_10 | text | true |
| 3 | BelebeleRetrieval | Retrieval | acm, afr, als... | Web, News, Written | ndcg_at_10 | text | true |
| 4 | CovidRetrieval | Retrieval | cmn | Medical, Entertainment | ndcg_at_10 | text | true |
| 5 | HagridRetrieval | Retrieval | eng | Encyclopaedic, Written | ndcg_at_10 | text | true |
| 6 | LEMBPasskeyRetrieval | Retrieval | eng | Fiction, Written | ndcg_at_1 | text | true |
| 7 | LegalBenchCorporate | Retrieval | eng | Legal, Written | ndcg_at_10 | text | true |
| 8 | MIRACLRetrievalHard | Retrieval | ara, ben, deu... | Encyclopaedic, Written | ndcg_at_10 | text | true |
| 9 | MLQARetrieval | Retrieval | ara, deu, eng... | Encyclopaedic, Written | ndcg_at_10 | text | true |
| 10 | SCIDOCS | Retrieval | eng | Academic, Written | ndcg_at_10 | text | true |
| 11 | SpartQA | Retrieval | eng | Encyclopaedic, Written | ndcg_at_10 | text | true |
| 12 | StackOverflowQA | Retrieval | eng | Programming, Written | ndcg_at_10 | text | true |
| 13 | StatcanDialogueData | Retrieval | eng, fra | Government, Web, Written | recall_at_10 | text | true |
| 14 | TRECCOVID | Retrieval | eng | Medical, Academic | ndcg_at_10 | text | true |
| 15 | TempReasonL1 | Retrieval | eng | Encyclopaedic, Written | ndcg_at_10 | text | true |
| 16 | TwitterHjerneRetrieval | Retrieval | dan | Social, Written | ndcg_at_10 | text | true |
| 17 | WikipediaRetrieval | Retrieval | ben, bul, ces... | Encyclopaedic, Written | ndcg_at_10 | text | true |
| 18 | WinoGrande | Retrieval | eng | Encyclopaedic, Written | ndcg_at_10 | text | true |
| 19 | FaroeseSTS | STS | fao | News, Web, Written | cosine_spearman | text | true |
| 20 | FinParaSTS | STS | fin | News, Subtitles, Written | cosine_spearman | text | true |
| 21 | GermanSTSBenchmark | STS | deu | News, Web, Written | cosine_spearman | text | true |
| 22 | IndicCrosslingualSTS | STS | asm, ben, eng... | News, Non-fiction | cosine_spearman | text | true |
| 23 | JSICK | STS | jpn | Web, Written | cosine_spearman | text | true |
| 24 | SICK-R | STS | eng | Web, Written | cosine_spearman | text | true |
| 25 | STS12 | STS | eng | Encyclopaedic, News | cosine_spearman | text | true |
| 26 | STS13 | STS | eng | Web, News, Non-fiction | cosine_spearman | text | true |
| 27 | STS14 | STS | eng | Blog, Web, Spoken | cosine_spearman | text | true |
| 28 | STS15 | STS | eng | Blog, News, Web | cosine_spearman | text | true |
| 29 | STS17 | STS | ara, deu, eng... | News, Web, Written | cosine_spearman | text | true |
| 30 | STS22.v2 | STS | ara, cmn, deu... | News, Written | cosine_spearman | text | true |
| 31 | STSB | STS | cmn | News, Web, Written | cosine_spearman | text | true |
| 32 | STSBenchmark | STS | eng | Blog, News, Written | cosine_spearman | text | true |
| 33 | STSES | STS | spa | News, Web, Written | cosine_spearman | text | true |
| 34 | SemRel24STS | STS | afr, amh, arb... | Spoken, Written | cosine_spearman | text | true |

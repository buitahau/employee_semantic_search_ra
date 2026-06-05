# MTEB Raw Data — Embedding Models

**Data Collection Date**: 2026-06-04

**Source**: [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)

**Models**: 11 embedding models (6 multilingual, 5 English-only)

---

## 1. Model Overview

| No | Model | Active Params (B) | Total Params (B) | Embedding Dim | Max Tokens | Mean (Task) | Mean (TaskType) | Multilanguage | MTEB Score (Retrieval) | License | Source |
|----|-------|:-----------------:|:----------------:|:-------------:|:----------:|:-----------:|:---------------:|:-------------:|:----------------------:|---------|--------|
| 1 | sentence-transformers/all-MiniLM-L6-v2 | 0.011 | 0.023 | 384 | 256 | 41.39 | 35.12 | No (English only) | 32.51 | apache-2.0 | [HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| 2 | sentence-transformers/all-MiniLM-L12-v2 | 0.022 | 0.033 | 384 | 256 | 42.28 | 36.39 | No (English only) | 33.37 | apache-2.0 | [HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2) |
| 3 | sentence-transformers/LaBSE | 0.086 | 0.471 | 768 | 512 | 52.07 | 45.65 | Yes (110 langs) | 33.17 | apache-2.0 | [HuggingFace](https://huggingface.co/sentence-transformers/LaBSE) |
| 4 | sentence-transformers/all-mpnet-base-v2 | 0.086 | 0.109 | 768 | 384 | 42.56 | 36.37 | No (English only) | 33.80 | apache-2.0 | [HuggingFace](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) |
| 5 | sentence-transformers/paraphrase-multilingual-mpnet-base-v2 | 0.086 | 0.278 | 768 | 512 | 51.98 | 45.17 | Yes (50 langs) | 39.76 | apache-2.0 | [HuggingFace](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2) |
| 6 | intfloat/multilingual-e5-base | 0.086 | 0.278 | 768 | 514 | 57.03 | 49.84 | Yes (94 langs) | 52.72 | mit | [HuggingFace](https://huggingface.co/intfloat/multilingual-e5-base) |
| 7 | intfloat/multilingual-e5-small | 0.022 | 0.118 | 384 | 512 | 56.35 | 49.45 | Yes (94 langs) | 50.91 | mit | [HuggingFace](https://huggingface.co/intfloat/multilingual-e5-small) |
| 8 | nomic-ai/nomic-embed-text-v1.5 | - | 0.137 | 768 | 8192 | 44.10 | 37.84 | No (English only) | 34.09 | apache-2.0 | [HuggingFace](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) |
| 9 | Snowflake/snowflake-arctic-embed-l-v2.0 | 0.312 | 0.568 | 1024 | 8192 | 57.03 | 49.95 | Yes (74 langs) | 58.36 | apache-2.0 | [HuggingFace](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0) |
| 10 | ibm-granite/granite-embedding-125m-english | 0.086 | 0.125 | 768 | 512 | 44.04 | 38.09 | No (English only) | 39.26 | apache-2.0 | [HuggingFace](https://huggingface.co/ibm-granite/granite-embedding-125m-english) |
| 11 | BAAI/bge-m3 | 0.312 | 0.568 | 1024 | 8194 | 59.55 | 52.17 | Yes | 54.59 | mit | [HuggingFace](https://huggingface.co/BAAI/bge-m3) |

---

## 2. Model Performance by Task


| Model | AILAStatutes | ArguAna | BelebeleRetrieval | CovidRetrieval | HagridRetrieval | LEMBPasskeyRetrieval | LegalBenchCorporateLobbying | MIRACLRetrievalHardNegatives | MLQARetrieval | SCIDOCS | SpartQA | StackOverflowQA | StatcanDialogueDatasetRetrieval | TRECCOVID | TempReasonL1 | TwitterHjerneRetrieval | WikipediaRetrievalMultilingual | WinoGrande |
|-------|:------------:|:-------:|:-----------------:|:--------------:|:---------------:|:--------------------:|:---------------------------:|:----------------------------:|:-------------:|:-------:|:-------:|:---------------:|:-------------------------------:|:---------:|:------------:|:----------------------:|:------------------------------:|:----------:|
| BAAI/bge-m3 | 29.04 | 54.04 | 78.16 | 77.51 | 98.77 | 59.00 | 90.34 | 69.59 | 74.81 | 16.31 | 7.49 | 80.60 | 21.86 | 54.72 | 0.99 | 37.82 | 89.87 | 41.72 |
| Snowflake/snowflake-arctic-embed-l-v2.0 | 22.82 | 59.11 | 74.02 | 78.53 | 98.69 | 77.25 | 93.80 | 66.53 | 73.10 | 20.28 | 5.74 | 86.94 | 19.06 | 83.63 | 1.00 | 44.52 | 90.50 | 55.03 |
| intfloat/multilingual-e5-base | 20.37 | 44.21 | 70.72 | 73.48 | 98.77 | 38.25 | 88.97 | 62.76 | 70.24 | 17.17 | 7.91 | 85.11 | 13.72 | 69.49 | 0.72 | 42.16 | 88.75 | 56.18 |
| intfloat/multilingual-e5-small | 19.01 | 39.09 | 66.29 | 72.82 | 98.55 | 38.25 | 89.47 | 60.09 | 63.85 | 13.90 | 5.43 | 81.94 | 10.33 | 72.29 | 0.80 | 58.18 | 88.66 | 37.46 |
| sentence-transformers/paraphrase-multilingual-mpnet-base-v2 | 22.24 | 48.91 | 54.39 | 28.85 | 98.52 | 7.75 | 87.62 | 27.19 | 61.16 | 13.96 | 5.69 | 43.11 | 18.95 | 37.87 | 1.94 | 36.68 | 71.79 | 49.01 |
| sentence-transformers/LaBSE | 16.72 | 34.18 | 60.73 | 28.60 | 94.76 | 20.00 | 69.39 | 17.49 | 52.70 | 5.63 | 1.56 | 38.23 | 4.17 | 16.34 | 1.56 | 14.38 | 66.31 | 54.30 |
| nomic-ai/nomic-embed-text-v1.5 | 19.16 | 52.02 | 25.98 | 13.11 | 98.55 | 17.25 | 92.19 | 8.77 | 17.00 | 17.63 | 6.30 | 63.62 | 12.76 | 63.44 | 1.71 | 6.74 | 50.70 | 46.79 |
| ibm-granite/granite-embedding-125m-english | 30.84 | 58.40 | 33.37 | 2.98 | 98.78 | 38.75 | 92.25 | 16.35 | 22.90 | 24.15 | 0.64 | 89.85 | 30.71 | 69.26 | 1.43 | 5.92 | 52.70 | 37.48 |
| sentence-transformers/all-MiniLM-L12-v2 | 20.71 | 47.13 | 23.22 | 10.79 | 98.40 | 14.75 | 88.69 | 11.32 | 16.22 | 21.44 | 2.67 | 80.63 | 16.70 | 50.82 | 1.66 | 6.62 | 61.42 | 27.16 |
| sentence-transformers/all-mpnet-base-v2 | 21.27 | 46.52 | 24.42 | 3.70 | 98.71 | 24.50 | 89.04 | 8.67 | 17.14 | 23.77 | 0.22 | 90.32 | 12.85 | 51.33 | 1.77 | 14.89 | 58.54 | 20.77 |
| sentence-transformers/all-MiniLM-L6-v2 | 20.52 | 50.17 | 20.80 | 0.80 | 98.84 | 23.25 | 86.41 | 8.78 | 13.24 | 21.64 | 1.65 | 83.96 | 10.47 | 47.23 | 1.53 | 9.81 | 38.81 | 47.35 |

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
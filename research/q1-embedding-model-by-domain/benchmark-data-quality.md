# Benchmark Data — Quality First

**Use case**: Maximize domain-specific retrieval accuracy. Tolerates higher operational cost.
**Search Quality weight**: 80% | **Operational Cost weight**: 20%
**Weight details & normalization formulas**: [references.md](./references.md)

**Date**: 2026-06-10
**Source**: [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
**Models**: 15

---

## Table 1 — Model Specifications

| Model | Embed Dim | Active Params (B) | Total Params (B) | Max Tokens | Mean (Task) | Mean (TaskType) | Retrieval | STS | Languages | License |
|-------|:---------:|:-----------------:|:----------------:|:----------:|:-----------:|:---------------:|:---------:|:---:|:---------:|:-------:|
| all-mpnet-base-v2 | 768 | 0.09 | 0.11 | 384 | 42.56 | 36.37 | 33.80 | 57.60 | No (EN only) | apache 2.0 |
| paraphrase-multilingual-mpnet-base-v2 | 768 | 0.09 | 0.28 | 512 | 51.98 | 45.17 | 39.76 | 69.66 | Yes (50 langs) | apache 2.0 |
| static-similarity-mrl-multilingual-v1 | 1024 | 0 | 0.11 | N/A | 47.24 | 41.38 | 41.21 | 64.02 | No (EN only) | apache 2.0 |
| LaBSE | 768 | 0.09 | 0.47 | 512 | 52.07 | 45.65 | 33.17 | 65.35 | Yes (50 langs) | apache 2.0 |
| granite-embedding-125m-english | 768 | 0.09 | 0.12 | 512 | 44.04 | 38.09 | 39.26 | 57.08 | No (EN only) | apache 2.0 |
| nomic-embed-text-v1.5 | 768 | N/A | 0.14 | 8192 | 44.10 | 37.84 | 34.09 | 59.45 | No (EN only) | mit |
| snowflake-arctic-embed-l-v2.0 | 1024 | 0.31 | 0.57 | 8192 | 57.03 | 49.95 | 58.36 | 70.11 | Yes (74 langs) | apache 2.0 |
| snowflake-arctic-embed-m-v2.0 | 768 | 0.11 | 0.30 | 8192 | 53.70 | 46.89 | 54.83 | 66.60 | Yes (74 langs) | apache 2.0 |
| bge-m3 | 1024 | 0.31 | 0.57 | 8194 | 59.55 | 52.17 | 54.59 | 74.12 | Yes (100+ langs) | mit |
| bge-large-en-v1.5 | 1024 | 0.30 | 0.34 | 512 | 45.08 | 39.06 | 39.00 | 60.14 | No (EN only) | mit |
| multilingual-e5-base | 768 | 0.09 | 0.28 | 514 | 57.03 | 49.84 | 52.72 | 71.44 | Yes (94 langs) | mit |
| multilingual-e5-small | 384 | 0.02 | 0.12 | 512 | 56.35 | 49.45 | 50.91 | 71.74 | Yes (94 langs) | mit |
| multilingual-e5-large | 1024 | 0.30 | 0.56 | 514 | 58.61 | 51.41 | 53.71 | 73.30 | No (EN only) | mit |
| e5-mistral-7b-instruct | 4096 | 6.98 | 7.11 | 32768 | 60.25 | 53.08 | 55.75 | 74.02 | No (EN only) | mit |
| KaLM-embedding-multilingual-mini-instruct-v2 | 896 | 0.36 | 0.49 | 512 | N/A | N/A | N/A | N/A | No (EN only) | mit |

---

## Table 2 — Domain Score by Model (Raw)

Domain Score = average of task scores within domain from MTEB. `N/A` = score not available.

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

## Table 3 — Final Score by Domain

Weighted final score (Search Quality 80% / Operational Cost 20%). **Bold** = best score per domain.
`N/A` = domain score unavailable; final score cannot be computed.

| Model | Academic | Blog | Encyclopaedic | Entertainment | Fiction | Government | Legal | Medical | News | Non Fiction | Programming | Social | Spoken | Subtitles | Web | Written |
|-------|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| all-mpnet-base-v2 | 36.93 | 37.87 | 14.24 | 14.56 | 20.60 | 22.47 | 33.94 | 17.24 | 14.24 | 14.24 | 48.78 | 21.03 | 14.24 | 15.41 | 14.24 | 14.24 |
| paraphrase-multilingual-mpnet-base-v2 | 47.33 | 63.73 | 45.15 | 45.84 | 34.57 | 47.91 | 53.88 | 41.05 | 54.06 | 49.28 | 37.81 | 54.12 | 48.43 | 61.61 | 53.40 | 48.58 |
| static-similarity-mrl-multilingual-v1 | 41.60 | 47.03 | 38.52 | 50.35 | 67.80 | 30.56 | 44.29 | 41.99 | 41.58 | 31.12 | 38.94 | 42.00 | 37.31 | 44.34 | 40.06 | 44.09 |
| LaBSE | 24.90 | 24.90 | 31.84 | 36.06 | 29.55 | 25.87 | 24.90 | 24.90 | 39.26 | 40.20 | 24.90 | 24.90 | 31.97 | 50.82 | 31.22 | 31.52 |
| granite-embedding-125m-english | 50.27 | 37.11 | 21.39 | 19.75 | 31.52 | 42.94 | 49.84 | 27.88 | 20.18 | 20.93 | 53.98 | 28.08 | 20.15 | 25.57 | 22.90 | 24.52 |
| nomic-embed-text-v1.5 | 38.75 | 34.08 | 13.57 | 16.11 | 15.23 | 20.18 | 33.63 | 21.53 | 14.78 | 14.42 | 29.61 | 17.16 | 14.39 | 16.48 | 13.86 | 11.90 |
| snowflake-arctic-embed-l-v2.0 | **89.37** | 71.15 | 71.27 | 87.29 | 80.74 | 67.80 | 79.19 | **89.25** | 74.81 | 72.33 | **86.66** | 83.45 | 71.83 | 75.95 | 76.45 | 83.25 |
| snowflake-arctic-embed-m-v2.0 | 80.74 | 59.44 | 63.14 | 76.51 | 66.19 | 62.67 | 76.02 | 78.61 | 62.41 | 57.60 | 81.90 | 64.37 | 57.98 | 69.95 | 63.57 | 71.05 |
| bge-m3 | 76.78 | 82.63 | 72.75 | **88.30** | 75.27 | 71.60 | 82.89 | 81.80 | 82.01 | 75.36 | 83.92 | 78.69 | 75.30 | **90.83** | 83.29 | 85.04 |
| bge-large-en-v1.5 | 53.98 | 53.18 | 23.96 | 27.98 | 32.80 | 36.85 | 44.34 | 35.76 | 26.46 | 25.37 | 51.53 | 38.00 | 23.57 | 21.79 | 29.52 | 26.14 |
| multilingual-e5-base | 77.40 | 75.68 | 66.69 | 80.49 | 61.34 | 58.73 | 68.67 | 78.94 | 71.81 | 64.46 | 80.86 | 69.74 | 64.92 | 72.28 | 71.90 | 74.88 |
| multilingual-e5-small | 76.00 | 73.25 | 62.81 | 79.00 | 60.14 | 54.69 | 66.77 | 78.37 | 70.53 | 64.90 | 77.55 | 74.29 | 64.39 | 66.93 | 69.19 | 71.59 |
| multilingual-e5-large | 80.96 | 81.12 | 69.86 | 84.15 | 64.08 | 58.87 | 72.39 | 82.80 | 77.73 | 69.61 | 86.09 | 74.16 | 69.23 | 78.58 | 79.19 | 79.46 |
| e5-mistral-7b-instruct | 83.39 | **83.63** | 64.22 | 79.19 | 57.36 | **83.63** | **83.63** | 82.91 | 72.48 | 60.34 | 83.63 | 73.18 | 72.59 | 67.67 | **83.63** | 78.00 |
| KaLM-embedding-multilingual-mini-instruct-v2 | 84.51 | 76.75 | **87.49** | 87.49 | N/A | N/A | N/A | 87.49 | **87.49** | **87.49** | N/A | **87.49** | **87.49** | N/A | 85.22 | **87.49** |

---

## Table 4 — Top 3 Models per Domain

| Domain | 1st | Score | 2nd | Score | 3rd | Score |
|--------|-----|:-----:|-----|:-----:|-----|:-----:|
| **Academic** | snowflake-arctic-embed-l-v2.0 | 89.37 | KaLM-embedding-multilingual-mini-instruct-v2 | 84.51 | e5-mistral-7b-instruct | 83.39 |
| **Blog** | e5-mistral-7b-instruct | 83.63 | bge-m3 | 82.63 | multilingual-e5-large | 81.12 |
| **Encyclopaedic** | KaLM-embedding-multilingual-mini-instruct-v2 | 87.49 | bge-m3 | 72.75 | snowflake-arctic-embed-l-v2.0 | 71.27 |
| **Entertainment** | bge-m3 | 88.30 | KaLM-embedding-multilingual-mini-instruct-v2 | 87.49 | snowflake-arctic-embed-l-v2.0 | 87.29 |
| **Fiction** | snowflake-arctic-embed-l-v2.0 | 80.74 | bge-m3 | 75.27 | static-similarity-mrl-multilingual-v1 | 67.80 |
| **Government** | e5-mistral-7b-instruct | 83.63 | bge-m3 | 71.60 | snowflake-arctic-embed-l-v2.0 | 67.80 |
| **Legal** | e5-mistral-7b-instruct | 83.63 | bge-m3 | 82.89 | snowflake-arctic-embed-l-v2.0 | 79.19 |
| **Medical** | snowflake-arctic-embed-l-v2.0 | 89.25 | KaLM-embedding-multilingual-mini-instruct-v2 | 87.49 | e5-mistral-7b-instruct | 82.91 |
| **News** | KaLM-embedding-multilingual-mini-instruct-v2 | 87.49 | bge-m3 | 82.01 | multilingual-e5-large | 77.73 |
| **Non Fiction** | KaLM-embedding-multilingual-mini-instruct-v2 | 87.49 | bge-m3 | 75.36 | snowflake-arctic-embed-l-v2.0 | 72.33 |
| **Programming** | snowflake-arctic-embed-l-v2.0 | 86.66 | multilingual-e5-large | 86.09 | bge-m3 | 83.92 |
| **Social** | KaLM-embedding-multilingual-mini-instruct-v2 | 87.49 | snowflake-arctic-embed-l-v2.0 | 83.45 | bge-m3 | 78.69 |
| **Spoken** | KaLM-embedding-multilingual-mini-instruct-v2 | 87.49 | bge-m3 | 75.30 | e5-mistral-7b-instruct | 72.59 |
| **Subtitles** | bge-m3 | 90.83 | multilingual-e5-large | 78.58 | snowflake-arctic-embed-l-v2.0 | 75.95 |
| **Web** | KaLM-embedding-multilingual-mini-instruct-v2 | 85.22 | e5-mistral-7b-instruct | 83.63 | bge-m3 | 83.29 |
| **Written** | KaLM-embedding-multilingual-mini-instruct-v2 | 87.49 | bge-m3 | 85.04 | snowflake-arctic-embed-l-v2.0 | 83.25 |

---

**Last Updated**: 2026-06-10

# Benchmark Data — Cost First

**Use case**: Minimize operational cost in CPU-only environments. Accepts lower accuracy in exchange for deployability.
**Search Quality weight**: 45% | **Operational Cost weight**: 55%
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
| bge-m3 | 1024 | 0.31 | 0.57 | 8194 | 59.55 | 52.17 | 54.59 | 74.12 | No (EN only) | mit |
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

Weighted final score (Search Quality 45% / Operational Cost 55%). **Bold** = best score per domain.
`N/A` = domain score unavailable; final score cannot be computed.

| Model | Academic | Blog | Encyclopaedic | Entertainment | Fiction | Government | Legal | Medical | News | Non Fiction | Programming | Social | Spoken | Subtitles | Web | Written |
|-------|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| all-mpnet-base-v2 | 57.43 | 57.96 | 44.46 | 44.64 | 48.09 | 49.16 | 55.71 | 46.18 | 44.46 | 44.46 | 64.20 | 48.34 | 44.46 | 45.13 | 44.46 | 44.46 |
| paraphrase-multilingual-mpnet-base-v2 | 62.54 | 71.92 | 61.30 | 61.69 | 55.25 | 62.87 | 66.29 | 58.96 | 66.39 | 63.66 | 57.10 | 66.43 | 63.17 | 70.70 | 66.01 | 63.26 |
| static-similarity-mrl-multilingual-v1 | 64.91 | 68.15 | 63.07 | 70.13 | 80.54 | 58.32 | 66.51 | 65.14 | 64.90 | 58.66 | 63.32 | 65.15 | 62.35 | 66.55 | 63.99 | 66.39 |
| LaBSE | 49.48 | 49.48 | 53.44 | 55.86 | 52.13 | 50.03 | 49.48 | 49.48 | 57.68 | 58.22 | 49.48 | 49.48 | 53.52 | 64.29 | 53.09 | 53.26 |
| granite-embedding-125m-english | 65.08 | 57.56 | 48.58 | 47.65 | 54.37 | 60.89 | 64.83 | 52.29 | 47.89 | 48.32 | 67.20 | 52.40 | 47.87 | 50.97 | 49.44 | 50.37 |
| nomic-embed-text-v1.5 | 48.59 | 45.19 | 30.21 | 32.06 | 31.42 | 35.03 | 44.86 | 36.02 | 31.10 | 30.83 | 41.92 | 32.83 | 30.81 | 32.34 | 30.43 | 28.99 |
| snowflake-arctic-embed-l-v2.0 | **86.83** | 76.42 | 76.49 | 85.64 | 81.90 | 74.51 | 81.02 | **86.76** | 78.52 | 77.10 | **85.29** | **83.45** | 76.81 | 79.16 | 79.45 | 83.34 |
| snowflake-arctic-embed-m-v2.0 | 83.37 | 71.19 | 73.31 | 80.95 | 75.05 | 73.04 | 80.67 | 82.15 | 72.89 | 70.14 | 84.03 | 74.01 | 70.36 | 77.20 | 73.56 | 77.83 |
| bge-m3 | 79.37 | **82.70** | 77.06 | **85.95** | 78.50 | **76.40** | **82.86** | 82.23 | **82.35** | 78.55 | 83.44 | 80.46 | 78.52 | **87.39** | **83.08** | **84.08** |
| bge-large-en-v1.5 | 65.79 | 65.33 | 48.63 | 50.93 | 53.68 | 56.00 | 60.28 | 55.38 | 50.06 | 49.44 | 64.39 | 56.65 | 48.41 | 47.40 | 51.81 | 49.88 |
| multilingual-e5-base | 79.73 | 78.74 | 73.61 | 81.49 | 70.55 | 69.06 | 74.74 | 80.61 | 76.53 | 72.33 | 81.70 | 75.35 | 72.60 | 76.80 | 76.58 | 78.28 |
| multilingual-e5-small | 79.73 | 78.16 | 72.19 | 81.45 | 70.67 | 67.56 | 74.46 | 81.09 | 76.60 | 73.39 | 80.62 | 78.76 | 73.10 | 74.55 | 75.84 | 77.21 |
| multilingual-e5-large | 80.27 | 80.36 | 73.93 | 82.09 | 70.62 | 67.65 | 75.37 | 81.32 | 78.42 | 73.78 | 83.20 | 76.39 | 73.57 | 78.91 | 79.26 | 79.41 |
| e5-mistral-7b-instruct | 53.47 | 53.60 | 42.52 | 51.07 | 38.59 | 53.60 | 53.60 | 53.19 | 47.23 | 40.30 | 53.60 | 47.64 | 47.29 | 44.48 | 53.60 | 50.39 |
| KaLM-embedding-multilingual-mini-instruct-v2 | 81.76 | 78.50 | **83.00** | 83.00 | N/A | N/A | N/A | 83.00 | 83.00 | **83.00** | N/A | 83.00 | **83.00** | N/A | 82.05 | 83.00 |

---

## Table 4 — Top 3 Models per Domain

| Domain | 1st | Score | 2nd | Score | 3rd | Score |
|--------|-----|:-----:|-----|:-----:|-----|:-----:|
| **Academic** | snowflake-arctic-embed-l-v2.0 | 86.83 | snowflake-arctic-embed-m-v2.0 | 83.37 | KaLM-embedding-multilingual-mini-instruct-v2 | 81.76 |
| **Blog** | bge-m3 | 82.70 | multilingual-e5-large | 80.36 | multilingual-e5-base | 78.74 |
| **Encyclopaedic** | KaLM-embedding-multilingual-mini-instruct-v2 | 83.00 | bge-m3 | 77.06 | snowflake-arctic-embed-l-v2.0 | 76.49 |
| **Entertainment** | bge-m3 | 85.95 | snowflake-arctic-embed-l-v2.0 | 85.64 | KaLM-embedding-multilingual-mini-instruct-v2 | 83.00 |
| **Fiction** | snowflake-arctic-embed-l-v2.0 | 81.90 | static-similarity-mrl-multilingual-v1 | 80.54 | bge-m3 | 78.50 |
| **Government** | bge-m3 | 76.40 | snowflake-arctic-embed-l-v2.0 | 74.51 | snowflake-arctic-embed-m-v2.0 | 73.04 |
| **Legal** | bge-m3 | 82.86 | snowflake-arctic-embed-l-v2.0 | 81.02 | snowflake-arctic-embed-m-v2.0 | 80.67 |
| **Medical** | snowflake-arctic-embed-l-v2.0 | 86.76 | KaLM-embedding-multilingual-mini-instruct-v2 | 83.00 | bge-m3 | 82.23 |
| **News** | KaLM-embedding-multilingual-mini-instruct-v2 | 83.00 | bge-m3 | 82.35 | snowflake-arctic-embed-l-v2.0 | 78.52 |
| **Non Fiction** | KaLM-embedding-multilingual-mini-instruct-v2 | 83.00 | bge-m3 | 78.55 | snowflake-arctic-embed-l-v2.0 | 77.10 |
| **Programming** | snowflake-arctic-embed-l-v2.0 | 85.29 | snowflake-arctic-embed-m-v2.0 | 84.03 | bge-m3 | 83.44 |
| **Social** | snowflake-arctic-embed-l-v2.0 | 83.45 | KaLM-embedding-multilingual-mini-instruct-v2 | 83.00 | bge-m3 | 80.46 |
| **Spoken** | KaLM-embedding-multilingual-mini-instruct-v2 | 83.00 | bge-m3 | 78.52 | snowflake-arctic-embed-l-v2.0 | 76.81 |
| **Subtitles** | bge-m3 | 87.39 | snowflake-arctic-embed-l-v2.0 | 79.16 | multilingual-e5-large | 78.91 |
| **Web** | bge-m3 | 83.08 | KaLM-embedding-multilingual-mini-instruct-v2 | 82.05 | snowflake-arctic-embed-l-v2.0 | 79.45 |
| **Written** | bge-m3 | 84.08 | snowflake-arctic-embed-l-v2.0 | 83.34 | KaLM-embedding-multilingual-mini-instruct-v2 | 83.00 |

---

**Last Updated**: 2026-06-10

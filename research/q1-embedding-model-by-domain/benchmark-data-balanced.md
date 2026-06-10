# Benchmark Data — Balanced

**Use case**: No hard constraint on accuracy or compute. Default for most production systems.
**Search Quality weight**: 55% | **Operational Cost weight**: 45%
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

Weighted final score (Search Quality 55% / Operational Cost 45%). **Bold** = best score per domain.
`N/A` = domain score unavailable; final score cannot be computed.

| Model | Academic | Blog | Encyclopaedic | Entertainment | Fiction | Government | Legal | Medical | News | Non Fiction | Programming | Social | Spoken | Subtitles | Web | Written |
|-------|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| all-mpnet-base-v2 | 48.92 | 49.51 | 34.66 | 34.86 | 38.65 | 39.83 | 47.04 | 36.55 | 34.66 | 34.66 | 56.37 | 38.93 | 34.66 | 35.39 | 34.66 | 34.66 |
| paraphrase-multilingual-mpnet-base-v2 | 56.98 | 67.29 | 55.61 | 56.05 | 48.96 | 57.35 | 61.10 | 53.04 | 61.21 | 58.21 | 51.00 | 61.26 | 57.68 | 65.96 | 60.80 | 57.77 |
| static-similarity-mrl-multilingual-v1 | 57.37 | 60.93 | 55.35 | 63.11 | 74.56 | 50.12 | 59.13 | 57.62 | 57.36 | 50.49 | 55.62 | 57.63 | 54.55 | 59.17 | 56.36 | 59.00 |
| LaBSE | 41.71 | 41.71 | 46.07 | 48.73 | 44.63 | 42.32 | 41.71 | 41.71 | 50.73 | 51.33 | 41.71 | 41.71 | 46.16 | 58.00 | 45.68 | 45.87 |
| granite-embedding-125m-english | 58.08 | 49.81 | 39.93 | 38.90 | 46.30 | 53.48 | 57.81 | 44.01 | 39.17 | 39.64 | 60.41 | 44.13 | 39.15 | 42.56 | 40.88 | 41.90 |
| nomic-embed-text-v1.5 | 43.73 | 40.36 | 25.53 | 27.36 | 26.73 | 30.30 | 40.03 | 31.29 | 26.41 | 26.15 | 37.13 | 28.13 | 26.12 | 27.63 | 25.74 | 24.32 |
| snowflake-arctic-embed-l-v2.0 | **86.47** | 75.02 | 75.09 | 85.16 | 81.04 | 72.91 | 80.07 | **86.39** | 77.32 | 75.76 | **84.77** | **82.75** | 75.44 | 78.03 | 78.35 | 82.62 |
| snowflake-arctic-embed-m-v2.0 | 81.26 | 67.87 | 70.20 | 78.60 | 72.12 | 69.90 | 78.30 | 79.92 | 69.74 | 66.72 | 81.99 | 70.97 | 66.96 | 74.48 | 70.47 | 75.17 |
| bge-m3 | 78.36 | **82.03** | 75.82 | **85.60** | 77.41 | **75.10** | **82.20** | 81.51 | **81.65** | 77.47 | 82.84 | 79.56 | 77.43 | **87.19** | **82.45** | **83.55** |
| bge-large-en-v1.5 | 59.58 | 59.07 | 40.71 | 43.23 | 46.26 | 48.81 | 53.52 | 48.12 | 42.28 | 41.59 | 58.03 | 49.53 | 40.46 | 39.35 | 44.20 | 42.08 |
| multilingual-e5-base | 77.86 | 76.77 | 71.13 | 79.80 | 67.76 | 66.12 | 72.37 | 78.82 | 74.34 | 69.72 | 80.03 | 73.04 | 70.01 | 74.64 | 74.40 | 76.27 |
| multilingual-e5-small | 77.42 | 75.69 | 69.13 | 79.31 | 67.45 | 64.02 | 71.62 | 78.91 | 73.98 | 70.44 | 78.40 | 76.34 | 70.12 | 71.72 | 73.14 | 74.65 |
| multilingual-e5-large | 79.35 | 79.45 | 72.36 | 81.35 | 68.73 | 65.46 | 73.96 | 80.50 | 77.31 | 72.21 | 82.57 | 75.07 | 71.97 | 77.85 | 78.23 | 78.40 |
| e5-mistral-7b-instruct | 63.03 | 63.18 | 50.98 | 60.39 | 46.66 | 63.18 | 63.18 | 62.72 | 56.17 | 48.54 | 63.18 | 56.61 | 56.24 | 53.14 | 63.18 | 59.64 |
| KaLM-embedding-multilingual-mini-instruct-v2 | 80.22 | 76.21 | **81.75** | 81.75 | N/A | N/A | N/A | 81.75 | 81.75 | **81.75** | N/A | 81.75 | **81.75** | N/A | 80.58 | 81.75 |

---

## Table 4 — Top 3 Models per Domain

| Domain | 1st | Score | 2nd | Score | 3rd | Score |
|--------|-----|:-----:|-----|:-----:|-----|:-----:|
| **Academic** | snowflake-arctic-embed-l-v2.0 | 86.47 | snowflake-arctic-embed-m-v2.0 | 81.26 | KaLM-embedding-multilingual-mini-instruct-v2 | 80.22 |
| **Blog** | bge-m3 | 82.03 | multilingual-e5-large | 79.45 | multilingual-e5-base | 76.77 |
| **Encyclopaedic** | KaLM-embedding-multilingual-mini-instruct-v2 | 81.75 | bge-m3 | 75.82 | snowflake-arctic-embed-l-v2.0 | 75.09 |
| **Entertainment** | bge-m3 | 85.60 | snowflake-arctic-embed-l-v2.0 | 85.16 | KaLM-embedding-multilingual-mini-instruct-v2 | 81.75 |
| **Fiction** | snowflake-arctic-embed-l-v2.0 | 81.04 | bge-m3 | 77.41 | static-similarity-mrl-multilingual-v1 | 74.56 |
| **Government** | bge-m3 | 75.10 | snowflake-arctic-embed-l-v2.0 | 72.91 | snowflake-arctic-embed-m-v2.0 | 69.90 |
| **Legal** | bge-m3 | 82.20 | snowflake-arctic-embed-l-v2.0 | 80.07 | snowflake-arctic-embed-m-v2.0 | 78.30 |
| **Medical** | snowflake-arctic-embed-l-v2.0 | 86.39 | KaLM-embedding-multilingual-mini-instruct-v2 | 81.75 | bge-m3 | 81.51 |
| **News** | KaLM-embedding-multilingual-mini-instruct-v2 | 81.75 | bge-m3 | 81.65 | snowflake-arctic-embed-l-v2.0 | 77.32 |
| **Non Fiction** | KaLM-embedding-multilingual-mini-instruct-v2 | 81.75 | bge-m3 | 77.47 | snowflake-arctic-embed-l-v2.0 | 75.76 |
| **Programming** | snowflake-arctic-embed-l-v2.0 | 84.77 | bge-m3 | 82.84 | multilingual-e5-large | 82.57 |
| **Social** | snowflake-arctic-embed-l-v2.0 | 82.75 | KaLM-embedding-multilingual-mini-instruct-v2 | 81.75 | bge-m3 | 79.56 |
| **Spoken** | KaLM-embedding-multilingual-mini-instruct-v2 | 81.75 | bge-m3 | 77.43 | snowflake-arctic-embed-l-v2.0 | 75.44 |
| **Subtitles** | bge-m3 | 87.19 | snowflake-arctic-embed-l-v2.0 | 78.03 | multilingual-e5-large | 77.85 |
| **Web** | bge-m3 | 82.45 | KaLM-embedding-multilingual-mini-instruct-v2 | 80.58 | snowflake-arctic-embed-l-v2.0 | 78.35 |
| **Written** | bge-m3 | 83.55 | snowflake-arctic-embed-l-v2.0 | 82.62 | KaLM-embedding-multilingual-mini-instruct-v2 | 81.75 |

---

**Last Updated**: 2026-06-10

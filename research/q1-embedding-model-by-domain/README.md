# Q1: Embedding Model Selection by Domain

**Research Question**: Which embedding model and dimension are most suitable for each domain?

**Date**: 2026-06-09

---

## Overview

This study benchmarks embedding models across 16 content domains to identify which models perform best for domain-specific semantic search. Models are evaluated using a weighted scoring system that combines performance quality and operational efficiency.

---

## Models Evaluated

**Total**: 15 models

**Data Source**: [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)

**Collection date**: 2026-06-04

**Selection criteria**: sentence-transformers library, eval-results tag, Apache-2.0 or MIT license, sorted by downloads. See [references.md](./references.md) for full filter details.

---

## Files

| File | Description |
|------|-------------|
| [benchmark-data.md](./benchmark-data.md) | Index of 3 scoring scenarios — links to each use-case benchmark file |
| [benchmark-data-quality.md](./benchmark-data-quality.md) | **Quality First** — Search Quality 80% / Operational Cost 20% |
| [benchmark-data-cost.md](./benchmark-data-cost.md) | **Cost First** — Search Quality 45% / Operational Cost 55% |
| [benchmark-data-balanced.md](./benchmark-data-balanced.md) | **Balanced** — Search Quality 55% / Operational Cost 45% |
| [mteb-raw-data.md](./mteb-raw-data.md) | Raw MTEB data — model overview, domain scores, task domain reference |
| [references.md](./references.md) | Data collection, weight ranges, weight allocation by use case, normalization formulas |
| [glossary.md](./glossary.md) | Plain-language definitions of key terms: parameters, embedding dimension, max tokens, MTEB metrics, Hugging Face filter options |

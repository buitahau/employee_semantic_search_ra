# AGG2 — Aggregate BM25 and Semantic Results

**Phase:** Query

**Status:** todo


**Depend:** AGG1

---

## Description

Once both retrieval paths exist — semantic search via pgvector (`query/retrieve.py`) and BM25 via PostgreSQL full-text search (`query/bm25_retrieve.py`) — their result sets must be merged into a single ranked list before deduplication and re-ranking.

The two paths use different scoring scales and distributions: cosine similarity is bounded `[0, 1]` with most useful results clustering above `0.5`; BM25 (`ts_rank_cd`) is also normalized to `[0, 1]` but behaves differently under sparse vs. dense queries. A naïve union or simple average would distort rankings. Reciprocal Rank Fusion (RRF) is the preferred approach: it converts each result's rank position (not its raw score) into a contribution score, making it robust to scale differences between retrievers.

This task replaces the single-path retrieval call in `query/__init__.py` with a two-path fan-out and fuses the results with RRF before handing off to the existing deduplication and re-ranking steps.

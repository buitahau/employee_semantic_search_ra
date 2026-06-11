# AGG1 — BM25 Search

**Phase:** Query

**Status:** todo

**Depend:**

---

## Description

The current search pipeline relies solely on cosine similarity against pgvector embeddings (`skills_search_index.embedding`). Semantic search is strong at capturing meaning but weak on exact-term recall — a query like `"AWS Lambda"` may rank below chunks that discuss cloud computing in general but never mention the exact phrase.

BM25 is a lexical ranking function that scores documents by how well they match the exact terms in the query, weighted by term frequency and inverse document frequency. Adding a BM25 retrieval path alongside the semantic path gives the pipeline a complementary signal: semantic handles paraphrase and intent, BM25 handles exact-term and rare-keyword recall.

This task implements BM25 search against `skills_search_index.chunk_text` using PostgreSQL full-text search (`tsvector` / `ts_rank_cd`), keeping the implementation inside the existing stack with no new infrastructure.


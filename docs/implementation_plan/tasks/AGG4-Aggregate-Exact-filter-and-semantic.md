# AGG4 — Aggregate Exact Filter and Semantic Results

**Phase:** Improvement — Aggregation with Exact Filter Revalidation  
**Status:** todo

**Depend:** AGG3

---

## Description

The exact filter post-pass removes non-qualifying candidates (see [[AGG3-Exact-filter]]), there is a complementary retrieval gap: employees who satisfy all hard constraints but whose embeddings rank poorly due to sparse or noisy skill descriptions. These candidates are invisible to the semantic path yet would be highly relevant to a user applying structured filters.

This task introduces a direct exact-match retrieval path that runs a parameterized SQL query against `skills_search_index.metadata` JSONB fields to surface candidates matching all extracted predicates, independent of their embedding similarity. The two result sets — semantic (post-exact-filter) and exact-match — are then merged using Reciprocal Rank Fusion (RRF) before deduplication and re-ranking.

### Pipeline position

```
┌─ semantic retrieve ─────────────────────────────────┐
│   pgvector cosine similarity                         │
│   → exact_filter (post-pass)                         │
└──────────────────────────────────────────────────────┤
                                                       ├─ RRF merge → deduplicate → re_rank
┌─ exact-match retrieve ───────────────────────────────┤
│   SQL JSONB containment on metadata predicates       │
└──────────────────────────────────────────────────────┘
```

### Scoring and fusion

The exact-match path returns no similarity score — every returned row satisfies the constraints equally. Candidates are assigned a synthetic rank based on their order from the SQL query (e.g. ordered by `employee_id` for determinism).

Candidates returned by both paths receive contributions from both rank lists, naturally boosting employees who both match the structured filter and score well semantically.

---

## Deliverables Checklist


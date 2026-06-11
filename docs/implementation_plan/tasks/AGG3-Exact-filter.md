# AGG3 — Exact Filter

**Phase:** Improvement — Aggregation with Exact Filter Revalidation  
**Status:** todo

**Depend:** IQ3, QP1

---

## Description

After BM25 and semantic retrieval produce a fused candidate set (see [[AGG1-BM25-search]] and [[AGG2-Aggregate-BM25-and-semantic]]), the merged results may still contain employees who do not satisfy hard constraints expressed in the query. For example, a query for "senior Python engineers" must not return junior employees, regardless of how well their embedding matches.

The exact filter is a post-retrieval pass that revalidates each candidate against structured predicates extracted from the query. Predicates target indexed metadata fields (e.g. `level`, `position`, `contract_type`, `skills`) and are evaluated as SQL WHERE clauses against the `skills_search_index.metadata` JSONB column. Candidates that fail any predicate are removed from the result set before re-ranking.

At this stage the filter handles simple equality predicates joined by AND only. Negation (NOT, exclusion) is handled in [[NCC1-Negation-handling]]; compound OR logic is handled in [[NCC2-Complex-condition-handling]].

### Filter fields

| Metadata key    | Source field              | Example values                        |
|-----------------|---------------------------|---------------------------------------|
| `level`         | `user_levels.label`       | `"Junior"`, `"Middle"`, `"Senior"`    |
| `position`      | `positions.name`          | `"Backend Developer"`, `"DevOps"`     |
| `contract_type` | `users.contract_type`     | `"FULLTIME"`, `"PART_TIME"`, `"INTERN"` |
| `skills`        | detected skill names      | `["Python", "AWS"]`                   |

### Pipeline position

```
retrieve (semantic + BM25 fused)
  → exact_filter          ← this task
  → deduplicate
  → re_rank
```

### Filter evaluation

Each predicate maps to a JSONB containment or equality check:

| Predicate type   | SQL fragment                                      |
|------------------|---------------------------------------------------|
| skill match      | `metadata @> '{"skills": ["Python"]}'::jsonb`     |
| level equality   | `metadata @> '{"level": "Senior"}'::jsonb`        |
| position match   | `metadata @> '{"position": "Backend Developer"}'::jsonb` |
| contract type    | `metadata @> '{"contract_type": "FULLTIME"}'::jsonb` |

Multiple predicates are combined with AND. The filter is applied as a second-pass SQL query over the candidate `employee_id` set returned by retrieval, avoiding a full table scan.

---

## Deliverables Checklist

- [ ] Add `level`, `position`, and `contract_type` fields to the metadata produced by `etl/impl/transform/metadata.py` so they are stored in `skills_search_index.metadata` at index time.
- [ ] Update `query/impl/analyze_query/metadata.py` (`build_filter`) to extract level, position, and contract_type predicates from the normalized query in addition to skills.
- [ ] Implement `query/impl/filter/exact_filter.py` — a function `exact_filter(hits: list[ChunkHit], criteria: dict) -> list[ChunkHit]` that re-evaluates each candidate against the parsed predicates using a parameterized SQL WHERE clause.
- [ ] Wire `exact_filter` into `query/__init__.py` between `retrieve` and `deduplicate`.
- [ ] Predicates are combined with AND; the filter must handle an empty criteria dict (no-op passthrough).
- [ ] All SQL in `exact_filter` uses parameterized queries (`%s` placeholders) — no string interpolation.

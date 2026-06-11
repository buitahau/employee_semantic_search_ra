# NCC1 — Negation Handling

**Phase:** Improvement — Exact Filter

**Status:** todo

**Depend:** QP1

---

## Description

Currently, the exact-filter step has no concept of exclusion. If a user writes "not a junior developer" or "no frontend-only candidates", those negations are silently ignored — junior or frontend-only candidates pass the filter as if the constraint were never stated.

This task adds NOT support to the exact filter: negated predicates are detected during query parsing and translated into SQL exclusion clauses (e.g. `seniority != 'junior'`, `NOT ('frontend' = ANY(roles))`). Negated candidates are hard-excluded in the filter pass rather than relying on the vector search to implicitly down-rank them.

---

## Deliverables Checklist

- [ ] Extend the query-parsing step to detect negation signals ("not", "no", "except", "without", "exclude") and annotate the corresponding predicate with a `negated` flag.
- [ ] Update the SQL translator to emit `!=` / `NOT IN` / `NOT (... = ANY(...))` clauses for negated predicates.
- [ ] Verify that negated predicates compose correctly with non-negated predicates (AND-ed together in the WHERE clause).

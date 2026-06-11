# NCC2 — Complex Condition Handling

**Phase:** Improvement — Exact Filter

**Status:** todo

**Depend:** QP1

---

## Description

Currently, the exact-filter step flattens all extracted criteria into a flat AND list. This breaks queries that express alternatives or mixed logic:

- "Python or Java" → requires *either* skill, not both; flat AND over-filters
- "senior and (React or Vue)" → AND/OR grouping; flat AND forces React AND Vue
- "backend or fullstack but not frontend-only" → OR branches with a nested NOT

This task introduces a condition tree to represent compound logic. Nodes are AND, OR, or NOT operators; leaves are individual field predicates. The tree is built during query parsing and translated into the corresponding SQL WHERE clause, replacing the current flat conjunction.

---

## Deliverables Checklist

- [ ] Define a condition tree data structure (AND / OR / NOT nodes, leaf predicates with field, operator, value) in `common/types.py`.
- [ ] Update the query-parsing step to produce a condition tree instead of a flat criterion list, covering disjunctions ("or", "either") and mixed AND/OR groupings ("X and (Y or Z)").
- [ ] Implement a translator that converts a condition tree into a parameterized SQL WHERE clause fragment (using `AND`, `OR`, parenthesised sub-expressions).
- [ ] Ensure the condition tree composes with negation (see [[Negation-handling]]) — NOT nodes are handled by the same translator.

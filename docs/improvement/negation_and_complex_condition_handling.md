## Negation and Complex Condition Handling

**Status:** Open

Currently, the exact-filter step (Set B in the aggregation pipeline) applies only simple conjunctive filters — all extracted criteria are AND-ed together. This fails to represent queries that express exclusion, alternatives, or compound logic.

### Why this matters

Users often phrase requirements with implicit or explicit negation and disjunctions:

- "not a junior developer" → should exclude candidates with seniority = junior
- "Python or Java" → should match candidates with *either* skill, not require both
- "backend or fullstack but not frontend-only" → combines OR and NOT
- "senior and (React or Vue)" → mixed AND/OR grouping

Flattening these into a simple AND list either over-filters (drops valid candidates) or under-filters (admits candidates the user explicitly excluded).

### Approach

To be determined.

### Benefit

- Queries with OR alternatives no longer silently drop valid candidates that match one branch but not all.
- Negations are honored deterministically in the exact-filter pass rather than relying on the vector search to implicitly down-rank excluded candidates.
- The condition tree is reusable: the same structure drives the SQL filter (Set B), the score-penalty logic in aggregation, and any future explanation layer that shows users *why* a candidate was included or excluded.

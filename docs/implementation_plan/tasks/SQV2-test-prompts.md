# SQV2 — Search Quality Test Prompts

**Phase:** Search Quality Validation  
**Status:** todo

---

## Description

Without a fixed list of queries and their expected results, it is impossible to measure whether the search pipeline is improving or regressing. Ad-hoc manual testing is not repeatable and misses edge cases.

This task produces a structured test prompt file that pairs each query with the expected search outcome. Prompts should cover the main intent categories supported by the pipeline (`find_employees` and `others`), realistic phrasings a recruiter or manager would type, and edge cases such as abbreviations, typos, multi-skill queries, and queries that should return no results. Each entry states the query, the expected response type, the expected top result(s) by name or ID, and the minimum acceptable score threshold.

The file must be machine-readable (JSON or YAML) so it can be consumed directly by the test runner in SQV3.

---

## Deliverables Checklist

- [ ] Test prompt file created in JSON or YAML format under `tests/search_quality/`
- [ ] At least 15 prompt entries covering `find_employees` and `others` intents
- [ ] Each entry includes: `query`, `expected_type`, `expected_top_ids` (ordered list), `min_score`
- [ ] Edge cases covered: abbreviations (e.g. "FE", "BE"), typos, multi-skill queries, language variations
- [ ] At least 2 prompts that should return no strong match (expected results empty or below threshold)
- [ ] Prompts reference employees defined in SQV1 seed data by ID or name

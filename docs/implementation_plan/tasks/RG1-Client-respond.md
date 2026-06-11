# RG1 — Client Response Generation

**Phase:** 5 — Hydration & Response  
**Status:** cancelled

> **Cancellation reason:** Response generation (re-ranking, `match_reason` population, and final response shaping) will be handled by a dedicated LLM service. This module is not needed in the current architecture.

---

## Description

After aggregation and hydration, the pipeline has a ranked list of `EmployeeDisplay` objects but no client-facing response yet. The shape and content of the response depends on what the user actually asked for — determined by `QueryAnalysis.intent` and `heuristic` from the rewrite step.

This task implements `query/respond.py`, which branches on intent to produce the final response dict. For `find_employees`, it calls GPT-4.1 mini to re-rank the list and generate a human-readable `match_reason` per employee. For `others` queries, it applies the heuristic deterministically without an LLM call — returning a count integer or a skill list for the top-matched employee. Unrecognised `others` heuristics fall back to the `find_employees` LLM path with a WARNING log.

Three response shapes are possible:

- `{"type": "employee_list", "results": [...]}` — ranked employees with `match_reason`
- `{"type": "count", "value": <int>}` — employees above the score threshold
- `{"type": "skill_list", "employee": {...}, "skills": [...]}` — skills for the top match

On any LLM failure for `find_employees`, the function returns the employee list with `match_reason: null` for all entries and never raises. The score threshold used for count queries defaults to `0.5` and is configurable via the `SEARCH_SCORE_THRESHOLD` env var.

---

## Deliverables Checklist

- [ ] `SkillDisplay` and `EmployeeDisplay` dataclasses added to `query/types.py`
- [ ] `query/respond.py` created with `respond(intent, heuristic, employees, hits) -> dict`
- [ ] LLM system prompt stored as a versioned module-level constant (not inlined in the function body)
- [ ] `find_employees`: calls GPT-4.1 mini, populates `match_reason` per employee, returns `{"type": "employee_list", "results": [...]}`
- [ ] `others` with count heuristic: returns `{"type": "count", "value": <int>}` without an LLM call
- [ ] `others` with skill-lookup heuristic: returns `{"type": "skill_list", "employee": {...}, "skills": [...]}`
- [ ] Unrecognised `others` heuristic falls back to `find_employees` path and logs WARNING
- [ ] LLM failure for `find_employees`: returns employee list with `match_reason: null` for all entries, logs WARNING, never raises
- [ ] `SEARCH_SCORE_THRESHOLD` read from env with default `0.5`

# Discussion — Improvement Points

| No | Title | Goal | Description | Priority | Status | Comment |
|----|-------|------|-------------|----------|--------|---------|
| 1 | T3.2 — AI Cleanup (GPT-4.1 mini) | Remove boilerplate/filler from normalized text while preserving skills, tools, frameworks, project names, roles, dates, and certifications | Call OpenAI GPT-4.1 mini with `normalized_text`, receive `ai_search_text`; fall back to `normalized_text` on API failure; store both fields without discarding the original | Low | Pending analysis | Need to decide whether the quality improvement justifies the added latency, cost, and OpenAI dependency. Will analyze before committing to implementation. |

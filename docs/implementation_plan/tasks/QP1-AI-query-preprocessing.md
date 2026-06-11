# QP1 — AI-Powered Query Preprocessing

**Phase:** Query

**Status:** todo

**Depend:** IQ3

---

## Description

Before generating an embedding, route the user's query through GPT-4.1 Mini as part of the analyze_query step to improve query quality. Raw user input is often noisy—containing typos, grammatical errors, ambiguous wording, or vague phrases such as "someone who knows cloud." These issues can degrade embedding quality and reduce retrieval accuracy.

The LLM rewrites the query into clean, unambiguous text and predicts the user's intent. The rewritten query is then used for embedding generation and downstream retrieval.

Current pipeline (in `query/__init__.py`):

```
normalize_query → analyze_query → retrieve → deduplicate → re_rank
```

Pipeline remains unchanged:

```
normalize_query → analyze_query → retrieve → deduplicate → re_rank
```

Example: 
analyze_query will be enhanced to invoke GPT-4.1 Mini and return:

- query — the AI-rewritten query used for embedding generation

- intent — the predicted intent (find_employee, count_employee, or other)

- heuristic — optional plain-language instructions to guide later ranking or filtering steps

- filter — structured filters extracted from the query when applicable

---

## Deliverables Checklist
- [ ] Update AI-query-preprocessing.md to define the JSON structure returned by the LLM.
- [ ] Update analyze_query to invoke LLM and parse the response.
- [ ] `OPENAI_API_KEY` consumed from `common/config.py` `settings` — no direct `os.environ` access

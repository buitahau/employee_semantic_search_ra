# Contextual Headers

**Phase:** 3 — Transform
**Status:** todo

---

## Description

Currently, each context section (CV, Experience, Training, etc.) is passed directly into the chunking step as plain text. The chunker has no knowledge of who the section belongs to, what document type it comes from, or what role/level the employee holds. This means every resulting chunk is context-free — the embedding model encodes only the raw content, with no identity or structural signal.

This task prepends a structured header to each context section **before** chunking. The header encodes the employee's identity (name, trigram, role, level) and the section type. Because the header is injected into the input text prior to windowing, it becomes part of every chunk produced from that section — no post-processing required. The embedding model then encodes this richer context into the vector, directly improving retrieval relevance and reranking accuracy.

---

## Deliverables Checklist

- [ ] Update `docs/implementation_plan/task/Contextual-headers.md` file that specifies the exact header template for each context section (CV, Experience, Training, etc.), field definitions, and examples.
- [ ] Implementation that prepends the structured header to each context section before it is passed to the chunker, without breaking existing chunking or embedding behavior.

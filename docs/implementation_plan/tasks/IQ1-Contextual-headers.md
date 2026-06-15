# IQ1 — Contextual Headers

**Phase:** 3 — Transform
**Status:** in progress

---

## Description

Currently, each context section (CV, Experience, Training, etc.) is passed directly into the chunking step as plain text. The chunker has no knowledge of who the section belongs to, what document type it comes from, or what role/level the employee holds. This means every resulting chunk is context-free — the embedding model encodes only the raw content, with no identity or structural signal.

This task prepends a structured header to each context section **before** chunking. The header encodes the employee's identity (name, trigram, role, level) and the section type. Because the header is injected into the input text prior to windowing, it becomes part of every chunk produced from that section — no post-processing required. The embedding model then encodes this richer context into the vector, directly improving retrieval relevance and reranking accuracy.

---

## Header Template

A single line, prepended to the section's text, separated by a blank line:

```text
[Employee: {first_name} {last_name} ({trigram}) | Position: {position} | Level: {level} | Section: {section_label}]

{original section text}
```

- Fields with a `None` value are omitted entirely, together with their label and the surrounding `" | "` separator.
- If `user_detail` is `None`, only the `Section:` field is emitted: `[Section: {section_label}]`.
- If the section's text is empty/`None`, no header is added (nothing to chunk).

### Section labels (`field_type` → `section_label`)

| `field_type`         | `section_label`     |
|-----------------------|----------------------|
| `user_detail`         | User Detail          |
| `cv`                  | CV                   |
| `experience`          | Experience           |
| `employment_history`  | Employment History   |
| `training`            | Training             |
| `task`                | Task                 |
| `user_skill`          | Skills               |

### Examples

Full identity:

```text
[Employee: Jane Doe (JDO) | Position: Software Engineer | Level: Senior | Section: Experience]

Worked on the OWT Employee App Search project as a backend developer...
```

Missing level:

```text
[Employee: Jane Doe (JDO) | Position: Software Engineer | Section: Training]

AWS Certified Solutions Architect ...
```

No `user_detail`:

```text
[Section: CV]

Experienced backend engineer with 5 years...
```

---

## Implementation Notes

- New module: `etl/impl/transform/header.py`, exposing `prepend_headers(state: EtlPipelineState, user_detail: UserDetail | None) -> EtlPipelineState`.
- Wired into `etl/transform.py` between `enrich_with_metadata` (T3.3) and `chunking` (T3.4/T3.5), so metadata extraction runs against the original section text and headers are injected immediately before sentence splitting/chunking.
- Mutates each entity's `text` in place (prepends the header), consistent with how other `etl/` transform steps mutate the pipeline state.

---

## Deliverables Checklist

- [x] Update `docs/implementation_plan/tasks/IQ1-Contextual-headers.md` file that specifies the exact header template for each context section (CV, Experience, Training, etc.), field definitions, and examples.
- [x] Implementation that prepends the structured header to each context section before it is passed to the chunker, without breaking existing chunking or embedding behavior.

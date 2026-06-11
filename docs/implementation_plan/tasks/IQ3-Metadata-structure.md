# IQ3 — Metadata Structure per Section

**Phase:** Indexing
**Status:** todo

---

## Description

Each chunk stored in `skills_search_index` carries a `metadata` JSON column, but there is currently no defined schema for what that metadata should contain per document section. Without a consistent structure, filtering and ranking logic must guess at field names, and new sections get added ad-hoc with no shared conventions.

This task defines the canonical metadata structure for every section type that can appear in a pgvector chunk. The structure specifies which fields are required, which are optional, and what their types and allowed values are.

For example, a chunk derived from a CV **Experience** section would carry:

```json
{
  "section": "experience",
  "employee_id": 42,
  "company": "Acme Corp",
  "title": "Senior Engineer",
  "start_date": "2021-03",
  "end_date": "2023-08",
  "is_current": false
}
```

A chunk from a CV **Skills** section would carry:

```json
{
  "section": "skills",
  "employee_id": 42,
  "skill_name": "AWS Lambda",
  "level": "advanced"
}
```

The metadata schema drives two downstream improvements:
- **Exact filtering** (AGG3, NCC1, NCC2) — filters can reference typed, predictable field names.
- **Contextual headers** (IQ1) — the header prepended before chunking is generated from the same metadata fields, keeping both in sync.

---

## Deliverables Checklist
- [ ] For each section type, document the required and optional metadata fields with their types and example values in this file.
- [ ] Update `etl/transform.py` so every chunk is emitted with metadata that conforms to the defined structure.

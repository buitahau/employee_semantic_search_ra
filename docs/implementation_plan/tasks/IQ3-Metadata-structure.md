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

## Metadata Schema per Section Type

All chunks share two required base fields:

| Field | Type | Description |
|-------|------|-------------|
| `section` | `string` | Section type identifier (see values below) |
| `employee_id` | `integer` | Source user ID |

---

### `user_detail`

Chunk of the employee's profile (position, level, contract, university, etc.). Always present — used as fallback when CV is missing.

**Required**

| Field | Type | Example |
|-------|------|---------|
| `section` | `string` | `"user_detail"` |
| `employee_id` | `integer` | `001` |
| `company_email` | `string` | `"abc@owt.swiss"` |
| `gender` | `string` | `"MALE"` · `"FEMALE"` |
| `start_date` | `string (ISO 8601)` | `"2023-06-26T00:00:00"` |

**Optional**

| Field | Type | Example |
|-------|------|---------|
| `first_name` | `string \| null` | `"A"` |
| `last_name` | `string \| null` | `"Nguyen Van"` |
| `date_of_birth` | `string (YYYY-MM-DD) \| null` | `"1990-01-10"` |
| `university` | `string \| null` | `"Da Nang University"` |
| `position` | `string \| null` | `"Dev"` |
| `level` | `string \| null` | `"Senior"` |

---

### `cv`

Chunk of the CV narrative text (introduction and/or body `cv` field).

**Required**

| Field | Type | Example |
|-------|------|---------|
| `section` | `string` | `"cv"` |
| `employee_id` | `integer` | `42` |

**Optional**

| Field | Type | Example |
|-------|------|---------|
| `custom_position` | `string \| null` | `"Full-Stack Developer"` |

---

### `experiences`

One chunk aggregating all project experience entries for the employee. Skills are deduplicated across all entries.

**Required**

| Field | Type | Example |
|-------|------|---------|
| `section` | `string` | `"experiences"` |
| `employee_id` | `integer` | `42` |

**Optional**

| Field | Type | Example |
|-------|------|---------|
| `skills` | `string[]` | `["Python", "AWS Lambda"]` |

---

### `employment_histories`

One chunk aggregating all external employment history entries for the employee.

**Required**

| Field | Type | Example |
|-------|------|---------|
| `section` | `string` | `"employment_histories"` |
| `employee_id` | `integer` | `42` |

---

### `trainings`

One chunk aggregating all training/certification records for the employee.

**Required**

| Field | Type | Example |
|-------|------|---------|
| `section` | `string` | `"trainings"` |
| `employee_id` | `integer` | `42` |

---

### `task`

One chunk aggregating all task assignments for the employee.

**Required**

| Field | Type | Example |
|-------|------|---------|
| `section` | `string` | `"task"` |
| `employee_id` | `integer` | `42` |

---

### `skills`

One chunk aggregating all skill entries for the employee. Skill names are deduplicated and collected into a list.

**Required**

| Field | Type | Example |
|-------|------|---------|
| `section` | `string` | `"skills"` |
| `employee_id` | `integer` | `42` |

**Optional**

| Field | Type | Example |
|-------|------|---------|
| `skills` | `string[]` | `["AWS Lambda", "Python"]` |

---

## Deliverables Checklist
- [x] For each section type, document the required and optional metadata fields with their types and example values in this file.
- [x] Update `etl/transform.py` so every chunk is emitted with metadata that conforms to the defined structure.

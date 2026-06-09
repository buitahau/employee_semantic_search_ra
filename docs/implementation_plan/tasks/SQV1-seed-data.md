# Search Quality Seed Data

**Phase:** Search Quality Validation  
**Status:** todo

---

## Description

The current seed data is minimal and does not reflect the variety of real employee profiles in the OWT Employee App. Thin or uniform data produces misleading search quality results — a pipeline can appear to work correctly on simple cases while failing silently on edge cases that only appear in richer data.

This task replaces or extends the existing seed data with a more complex and realistic dataset. The dataset should include employees with overlapping skill sets (to test ranking), employees with similar roles but different seniority levels, employees with skills mentioned only in CV text (not in structured skill fields), and employees who should clearly not match certain queries. Data variations should cover different languages, different formats for the same concept (e.g. "JS" vs "JavaScript"), and mixed proficiency levels.

The seed data must be documented alongside the SQL or fixture files so that the prompt/expected-result list in SQV2 can reference it precisely.

---

## Deliverables Checklist

- [ ] Seed data file(s) created (SQL inserts or fixture format) covering at least 10 distinct employee profiles
- [ ] Profiles include overlapping skills across employees to test ranking differentiation
- [ ] At least one employee has skills mentioned only in free-text CV content (not in structured skill fields)
- [ ] At least one employee should clearly not match a given skill query (true negative)
- [ ] Variations in terminology covered (e.g. abbreviations, alternate spellings, mixed languages)
- [ ] A brief summary document describes each seeded employee — name, role, key skills, and notable characteristics — so SQV2 can reference them by name when defining expected results

# Field Mapping Table

**Phase:** 2 — Extract
**Status:** todo

---

## Description

The ETL pipeline pulls data from multiple source tables in the OWT Employee App database, but there is currently no explicit documentation of which tables and fields are used during extraction. Without this visibility, it is difficult to audit data coverage, identify missing signals, and ensure the extraction logic remains aligned with business requirements.

This task creates a comprehensive field mapping document that lists every source table and field used by the ETL pipeline, providing a clear reference for data lineage and extraction coverage.

---

## Deliverables Checklist

- [ ] Update `docs/implementation_plan/tasks/Field-mapping-table.md` with a detailed mapping of every source table and field used to retrieve data.
- [ ] Update the ETL source code so it follows the field mapping table.

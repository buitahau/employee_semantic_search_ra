# IQ2 — Field Mapping Table

**Phase:** 2 — Extract
**Status:** done

---

## Description

The ETL pipeline pulls data from multiple source tables in the OWT Employee App database, but there is currently no explicit documentation of which tables and fields are used during extraction. Without this visibility, it is difficult to audit data coverage, identify missing signals, and ensure the extraction logic remains aligned with business requirements.

This task creates a comprehensive field mapping document that lists every source table and field used by the ETL pipeline, providing a clear reference for data lineage and extraction coverage.

---

## Field Mapping

Each subsection corresponds to one `_get_*` function in `etl/extract.py` and one dataclass in `common/types.py`.

### `user_detail` → `UserDetail`

Source: `users`, left-joined to `positions` (`position_id`) and `user_levels` (`level_id`, nullable FK).

| Output field | Type | Source | Notes |
|---|---|---|---|
| `first_name` | `str \| None` | `users.first_name` | |
| `last_name` | `str \| None` | `users.last_name` | |
| `trigram` | `str \| None` | `users.trigram` | |
| `company_email` | `str` | `users.company_email` | |
| `gender` | `str` | `users.gender` | enum: `MALE` \| `FEMALE` |
| `date_of_birth` | `datetime \| None` | `users.date_of_birth` | |
| `university` | `str \| None` | `users.university` | |
| `position` | `str \| None` | `positions.name` | via `users.position_id` |
| `level` | `str \| None` | `user_levels.label` | via `users.level_id` (nullable FK) |
| `contract_type` | `str` | `users.contract_type` | enum: `FULLTIME` \| `PART_TIME` \| `INTERN` |
| `start_date` | `date` | `users.start_date` | |
| `updated_at` | `datetime` | `users.updated_at` | |

Filter: `users.id = employee_id`.

---

### `cv` → `Cv`

Source: `user_cvs`, left-joined to `cv_overview` on `user_id`.

| Output field | Type | Source | Notes |
|---|---|---|---|
| `cv` | `str \| None` | `user_cvs.cv` | |
| `custom_position` | `str \| None` | `cv_overview.custom_position` | |
| `introduction` | `str \| None` | `cv_overview.introduction` | |
| `updated_at` | `datetime` | `GREATEST(user_cvs.updated_at, cv_overview.updated_at)` | |

Filter: `user_cvs.user_id = employee_id`. Only the most recently updated `user_cvs` row is used (`ORDER BY uc.updated_at DESC LIMIT 1`).

---

### `experiences` → `list[Experience]`

Source: `experiences`, left-joined through `experience_skills` to `skills`, grouped by `experiences.id`.

| Output field | Type | Source | Notes |
|---|---|---|---|
| `project_name` | `str \| None` | `experiences.project_name` | |
| `domain` | `str \| None` | `experiences.domain` | |
| `description` | `str \| None` | `experiences.description` | |
| `roles_and_responsibilities` | `str \| None` | `experiences.roles_and_responsibilities` | |
| `date_from` | `date` | `experiences.date_from` | |
| `date_to` | `date \| None` | `experiences.date_to` | |
| `is_currently_working` | `bool` | `experiences.is_currently_working` | |
| `skills` | `list[str]` | `skills.name` | `array_agg(s.name)` via `experience_skills`, `'{}'` if none |
| `updated_at` | `datetime` | `experiences.updated_at` | |

Filter: `experiences.user_id = employee_id`. One row per experience.

---

### `employment_histories` → `list[EmploymentHistory]`

Source: `employment_histories`.

| Output field | Type | Source | Notes |
|---|---|---|---|
| `company` | `str \| None` | `employment_histories.company` | |
| `date_from` | `date` | `employment_histories.date_from` | |
| `date_to` | `date \| None` | `employment_histories.date_to` | |
| `is_currently_working` | `bool` | `employment_histories.is_currently_working` | |
| `updated_at` | `datetime` | `employment_histories.updated_at` | |

Filter: `employment_histories.user_id = employee_id`. One row per entry.

---

### `trainings` → `list[Training]`

Source: `trainings`, left-joined to `training_topics` (`topic_id`) and `training_levels` (`level_id`).

| Output field | Type | Source | Notes |
|---|---|---|---|
| `training_title` | `str \| None` | `trainings.training_title` | |
| `training_description` | `str \| None` | `trainings.training_description` | |
| `training_date` | `date` | `trainings.training_date` | |
| `topic_label` | `str \| None` | `training_topics.label` | via `trainings.topic_id` |
| `level_label` | `str \| None` | `training_levels.label` | via `trainings.level_id` |
| `updated_at` | `datetime` | `trainings.updated_at` | |

Filter: `trainings.user_id = employee_id`. One row per training/certification entry.

---

### `tasks` → `list[Task]`

Source: `task_assignments`, joined to `task_assignments_assignees` and left-joined to `task_assignments_categories` (`category_id`).

| Output field | Type | Source | Notes |
|---|---|---|---|
| `title` | `str \| None` | `task_assignments.title` | |
| `details` | `str \| None` | `task_assignments.details` | |
| `category_label` | `str \| None` | `task_assignments_categories.label` | via `task_assignments.category_id` |
| `updated_at` | `datetime` | `task_assignments.updated_at` | |

Filter: `task_assignments_assignees.user_id = employee_id` (join on `task_assignment_id`). One row per task assignment where the employee is an assignee.

---

### `skills` → `list[UserSkill]`

Source: `user_skills`, joined to `skills` on `skill_id`.

| Output field | Type | Source | Notes |
|---|---|---|---|
| `skill_name` | `str \| None` | `skills.name` | |
| `level` | `int` | `user_skills.level` | |
| `updated_at` | `datetime` | `user_skills.updated_at` | |

Filter: `user_skills.user_id = employee_id AND user_skills.is_selected = true`. One row per selected skill.

---

### Employee IDs → `get_all_employee_ids`

| Output field | Type | Source | Notes |
|---|---|---|---|
| `employee_id` | `int` | `users.id` | All rows, ordered by `id` |

---

## Deliverables Checklist

- [x] Update `docs/implementation_plan/tasks/IQ2-Field-mapping-table.md` with a detailed mapping of every source table and field used to retrieve data.
- [x] Update the ETL source code so it follows the field mapping table.

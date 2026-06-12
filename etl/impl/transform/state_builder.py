from typing import Any

from common.states import (
    CvState,
    EmploymentHistoryState,
    EtlPipelineState,
    ExperienceState,
    TaskState,
    TrainingState,
    UserDetailState,
    UserSkillState,
)
from common.types import EmployeeData


def _join(*values: Any) -> str | None:
    parts = []
    for v in values:
        if v is None:
            continue
        if isinstance(v, list):
            parts.extend(str(i) for i in v if i is not None)
        else:
            parts.append(str(v))
    joined = " ".join(parts)
    return joined or None


def to_pipeline_state(data: EmployeeData) -> EtlPipelineState:
    user_detail = None
    if data.user_detail:
        ud = data.user_detail
        user_detail = UserDetailState(
            text=_join(
                ud.first_name, ud.last_name, ud.trigram, ud.company_email,
                ud.gender, ud.date_of_birth, ud.university, ud.position,
                ud.level, ud.contract_type, ud.start_date, ud.updated_at,
            )
        )

    cv = None
    if data.cv:
        c = data.cv
        cv = CvState(text=_join(c.cv, c.custom_position, c.introduction, c.updated_at))

    exp_text = _join(*[
        _join(
            e.project_name, e.domain, e.description, e.roles_and_responsibilities,
            e.date_from, e.date_to, e.is_currently_working, e.skills, e.updated_at,
        )
        for e in data.experiences
    ])
    eh_text = _join(*[
        _join(eh.company, eh.date_from, eh.date_to, eh.is_currently_working, eh.updated_at)
        for eh in data.employment_histories
    ])
    training_text = _join(*[
        _join(
            t.training_title, t.training_description, t.training_date,
            t.topic_label, t.level_label, t.updated_at,
        )
        for t in data.trainings
    ])
    task_text = _join(*[
        _join(t.title, t.details, t.category_label, t.updated_at)
        for t in data.tasks
    ])
    skill_text = _join(*[_join(s.skill_name, s.level, s.updated_at) for s in data.skills])

    return EtlPipelineState(
        employee_id=data.employee_id,
        user_detail=user_detail,
        cv=cv,
        experiences=ExperienceState(text=exp_text) if exp_text else None,
        employment_histories=EmploymentHistoryState(text=eh_text) if eh_text else None,
        trainings=TrainingState(text=training_text) if training_text else None,
        task=TaskState(text=task_text) if task_text else None,
        skills=UserSkillState(text=skill_text) if skill_text else None,
    )

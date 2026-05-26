from common.states import (
    CvState,
    EmploymentHistoryState,
    EtlPipelineState,
    ExperienceState,
    TaskState,
    TrainingState,
    UserSkillState,
)
from common.types import EmployeeData


def _join(*values: str | None) -> str | None:
    joined = " ".join(v for v in values if v)
    return joined or None


def to_pipeline_state(data: EmployeeData) -> EtlPipelineState:
    cv = None
    if data.cv:
        cv = CvState(text=_join(data.cv.cv, data.cv.custom_position, data.cv.introduction))

    exp_text = _join(*[
        _join(e.project_name, e.domain, e.description, e.roles_and_responsibilities)
        for e in data.experiences
    ])
    eh_text = _join(*[_join(eh.company) for eh in data.employment_histories])
    training_text = _join(*[
        _join(t.training_title, t.training_description, t.topic_label, t.level_label)
        for t in data.trainings
    ])
    task_text = _join(*[_join(t.title, t.details, t.category_label) for t in data.tasks])
    skill_text = _join(*[_join(s.skill_name) for s in data.skills])

    return EtlPipelineState(
        employee_id=data.employee_id,
        user_detail=data.user_detail,
        cv=cv,
        experiences=ExperienceState(text=exp_text) if exp_text else None,
        employment_histories=EmploymentHistoryState(text=eh_text) if eh_text else None,
        trainings=TrainingState(text=training_text) if training_text else None,
        task=TaskState(text=task_text) if task_text else None,
        skills=UserSkillState(text=skill_text) if skill_text else None,
    )

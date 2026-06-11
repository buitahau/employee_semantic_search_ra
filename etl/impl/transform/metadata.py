from common.states import EtlPipelineState
from common.types import (
    Cv,
    EmployeeData,
    EmploymentHistory,
    Experience,
    Task,
    Training,
    UserDetail,
    UserSkill,
)


def _user_detail_metadata(employee_id: int, ud: UserDetail) -> dict:
    m: dict = {
        "section": "user_detail",
        "employee_id": employee_id,
        "company_email": ud.company_email,
        "gender": ud.gender,
        "start_date": ud.start_date.isoformat(),
    }
    if ud.first_name is not None:
        m["first_name"] = ud.first_name
    if ud.last_name is not None:
        m["last_name"] = ud.last_name
    if ud.date_of_birth is not None:
        m["date_of_birth"] = ud.date_of_birth.strftime("%Y-%m-%d")
    if ud.university is not None:
        m["university"] = ud.university
    if ud.position is not None:
        m["position"] = ud.position
    if ud.level is not None:
        m["level"] = ud.level
    return m


def _cv_metadata(employee_id: int, cv: Cv) -> dict:
    m: dict = {"section": "cv", "employee_id": employee_id}
    if cv.custom_position is not None:
        m["custom_position"] = cv.custom_position
    return m


def _experiences_metadata(employee_id: int, experiences: list[Experience]) -> dict:
    all_skills: list[str] = []
    for e in experiences:
        for s in e.skills:
            if s not in all_skills:
                all_skills.append(s)
    m: dict = {"section": "experiences", "employee_id": employee_id}
    if all_skills:
        m["skills"] = all_skills
    return m


def _employment_histories_metadata(employee_id: int) -> dict:
    return {"section": "employment_histories", "employee_id": employee_id}


def _trainings_metadata(employee_id: int) -> dict:
    return {"section": "trainings", "employee_id": employee_id}


def _task_metadata(employee_id: int) -> dict:
    return {"section": "task", "employee_id": employee_id}


def _skills_metadata(employee_id: int, skills: list[UserSkill]) -> dict:
    all_skills: list[str] = []
    for s in skills:
        if s.skill_name is not None and s.skill_name not in all_skills:
            all_skills.append(s.skill_name)
    m: dict = {"section": "skills", "employee_id": employee_id}
    if all_skills:
        m["skills"] = all_skills
    return m


def enrich_with_metadata(state: EtlPipelineState, data: EmployeeData) -> EtlPipelineState:
    eid = state.employee_id

    if state.user_detail and data.user_detail:
        state.user_detail.metadata = _user_detail_metadata(eid, data.user_detail)
    if state.cv and data.cv:
        state.cv.metadata = _cv_metadata(eid, data.cv)
    if state.experiences:
        state.experiences.metadata = _experiences_metadata(eid, data.experiences)
    if state.employment_histories:
        state.employment_histories.metadata = _employment_histories_metadata(eid)
    if state.trainings:
        state.trainings.metadata = _trainings_metadata(eid)
    if state.task:
        state.task.metadata = _task_metadata(eid)
    if state.skills:
        state.skills.metadata = _skills_metadata(eid, data.skills)

    return state

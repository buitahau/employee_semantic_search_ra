from common.db import _connect
from common.states import EtlPipelineState


def get_all_skill_names() -> list[str]:
    with _connect() as cur:
        cur.execute("SELECT name FROM skills ORDER BY name")
        return [row["name"] for row in cur.fetchall()]


def detect_skills(text: str | None, skill_names: list[str]) -> list[str]:
    if not text:
        return []
    text_lower = text.lower()
    return [name for name in skill_names if name.lower() in text_lower]


def extract_metadata(employee_id: int, skills: list[str], **optional_fields) -> dict:
    return {
        "employee_id": employee_id,
        "skills": skills,
        **{k: v for k, v in optional_fields.items() if v is not None},
    }


def enrich_with_metadata(state: EtlPipelineState) -> EtlPipelineState:
    skill_names = get_all_skill_names()
    eid = state.employee_id

    if state.cv:
        state.cv.metadata = extract_metadata(eid, detect_skills(state.cv.text, skill_names))
    if state.experiences:
        state.experiences.metadata = extract_metadata(eid, detect_skills(state.experiences.text, skill_names))
    if state.employment_histories:
        state.employment_histories.metadata = extract_metadata(eid, detect_skills(state.employment_histories.text, skill_names))
    if state.trainings:
        state.trainings.metadata = extract_metadata(eid, detect_skills(state.trainings.text, skill_names))
    if state.task:
        state.task.metadata = extract_metadata(eid, detect_skills(state.task.text, skill_names))
    if state.skills:
        state.skills.metadata = extract_metadata(eid, detect_skills(state.skills.text, skill_names))

    return state

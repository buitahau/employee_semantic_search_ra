import dataclasses

from common.db import _connect
from common.types import EmployeeData


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


def enrich_with_metadata(data: EmployeeData) -> EmployeeData:
    skill_names = get_all_skill_names()
    eid = data.employee_id

    cv = None
    if data.cv:
        text = _join_texts(data.cv.cv, data.cv.introduction)
        cv = dataclasses.replace(
            data.cv,
            metadata=extract_metadata(eid, detect_skills(text, skill_names)),
        )

    experiences = [
        dataclasses.replace(
            row,
            metadata=extract_metadata(
                eid,
                detect_skills(_join_texts(row.description, row.roles_and_responsibilities), skill_names),
            ),
        )
        for row in data.experiences
    ]

    employment_histories = [
        dataclasses.replace(
            row,
            metadata=extract_metadata(eid, detect_skills(row.company, skill_names)),
        )
        for row in data.employment_histories
    ]

    trainings = [
        dataclasses.replace(
            row,
            metadata=extract_metadata(
                eid,
                detect_skills(_join_texts(row.training_title, row.training_description), skill_names),
            ),
        )
        for row in data.trainings
    ]

    tasks = [
        dataclasses.replace(
            row,
            metadata=extract_metadata(
                eid,
                detect_skills(_join_texts(row.title, row.details), skill_names),
            ),
        )
        for row in data.tasks
    ]

    skills = [
        dataclasses.replace(
            row,
            metadata=extract_metadata(eid, detect_skills(row.skill_name, skill_names)),
        )
        for row in data.skills
    ]

    return dataclasses.replace(
        data,
        cv=cv,
        experiences=experiences,
        employment_histories=employment_histories,
        trainings=trainings,
        tasks=tasks,
        skills=skills,
    )


def _join_texts(*texts: str | None) -> str:
    return " ".join(t for t in texts if t)

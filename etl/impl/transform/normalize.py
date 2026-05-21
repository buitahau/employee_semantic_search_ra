import re
from html import unescape

from common.types import (
    Cv,
    EmployeeData,
    EmploymentHistory,
    Experience,
    Task,
    Training,
    UserSkill,
)

SENTINELS = {"null", "undefined", "None"}

PUNCT_MAP = str.maketrans({
    "‘": "'", "’": "'",
    "“": '"', "”": '"',
    "–": "-", "—": "-",
    "…": "...",
})


def normalize_text(text: str | None) -> str | None:
    if text is None:
        return None
    stripped = text.strip()
    if stripped == "" or stripped in SENTINELS:
        return None
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = text.translate(PUNCT_MAP)
    text = re.sub(r"[\s​‌‍﻿]+", " ", text).strip()
    return text if text else None


def normalize(raw: EmployeeData) -> EmployeeData:
    return EmployeeData(
        employee_id=raw.employee_id,
        user_detail=raw.user_detail,
        cv=_normalize_cv(raw.cv),
        experiences=[_normalize_experience(e) for e in raw.experiences],
        employment_histories=[_normalize_employment_history(h) for h in raw.employment_histories],
        trainings=[_normalize_training(t) for t in raw.trainings],
        tasks=[_normalize_task(t) for t in raw.tasks],
        skills=[_normalize_user_skill(s) for s in raw.skills],
    )


def _normalize_cv(row: Cv | None) -> Cv | None:
    if row is None:
        return None
    return Cv(
        cv=normalize_text(row.cv),
        custom_position=normalize_text(row.custom_position),
        introduction=normalize_text(row.introduction),
        updated_at=row.updated_at,
        metadata=row.metadata,
    )


def _normalize_experience(row: Experience) -> Experience:
    return Experience(
        project_name=normalize_text(row.project_name),
        domain=normalize_text(row.domain),
        description=normalize_text(row.description),
        roles_and_responsibilities=normalize_text(row.roles_and_responsibilities),
        date_from=row.date_from,
        date_to=row.date_to,
        is_currently_working=row.is_currently_working,
        skills=row.skills,
        updated_at=row.updated_at,
        metadata=row.metadata,
    )


def _normalize_employment_history(row: EmploymentHistory) -> EmploymentHistory:
    return EmploymentHistory(
        company=normalize_text(row.company),
        date_from=row.date_from,
        date_to=row.date_to,
        is_currently_working=row.is_currently_working,
        updated_at=row.updated_at,
        metadata=row.metadata,
    )


def _normalize_training(row: Training) -> Training:
    return Training(
        training_title=normalize_text(row.training_title),
        training_description=normalize_text(row.training_description),
        training_date=row.training_date,
        topic_label=normalize_text(row.topic_label),
        level_label=normalize_text(row.level_label),
        updated_at=row.updated_at,
        metadata=row.metadata,
    )


def _normalize_task(row: Task) -> Task:
    return Task(
        title=normalize_text(row.title),
        details=normalize_text(row.details),
        category_label=normalize_text(row.category_label),
        updated_at=row.updated_at,
        metadata=row.metadata,
    )


def _normalize_user_skill(row: UserSkill) -> UserSkill:
    return UserSkill(
        skill_name=normalize_text(row.skill_name),
        level=row.level,
        updated_at=row.updated_at,
        metadata=row.metadata,
    )

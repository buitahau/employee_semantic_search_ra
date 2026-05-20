from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Cv:
    cv: str | None
    custom_position: str | None
    introduction: str | None
    updated_at: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class Experience:
    project_name: str | None
    domain: str | None
    description: str | None
    roles_and_responsibilities: str | None
    date_from: date
    date_to: date | None
    is_currently_working: bool
    skills: list[str]
    updated_at: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class EmploymentHistory:
    company: str | None
    date_from: date
    date_to: date | None
    is_currently_working: bool
    updated_at: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class Training:
    training_title: str | None
    training_description: str | None
    training_date: date
    topic_label: str | None
    level_label: str | None
    updated_at: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class Task:
    title: str | None
    details: str | None
    category_label: str | None
    updated_at: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class UserSkill:
    skill_name: str | None
    level: int
    updated_at: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class EmployeeData:
    employee_id: int
    cv: Cv | None
    experiences: list[Experience]
    employment_histories: list[EmploymentHistory]
    trainings: list[Training]
    tasks: list[Task]
    skills: list[UserSkill]

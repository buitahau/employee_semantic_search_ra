from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class UserDetail:
    first_name: str | None
    last_name: str | None
    trigram: str | None
    company_email: str
    gender: str                # MALE | FEMALE
    date_of_birth: datetime | None
    university: str | None
    position: str | None       # positions.name
    level: str | None          # user_levels.label (nullable FK)
    contract_type: str         # FULLTIME | PART_TIME | INTERN
    start_date: date
    updated_at: datetime


@dataclass
class ChunkRecord:
    employee_id: int
    field_type: str      # "cv" | "experience" | "employment_history" | "training" | "task" | "user_skill"
    chunk_text: str
    chunk_index: int
    char_start: int
    char_end: int
    token_count: int
    preprocess_version: str
    embedding: list[float] | None = None
    metadata: dict = field(default_factory=dict)


@dataclass
class Cv:
    cv: str | None
    custom_position: str | None
    introduction: str | None
    updated_at: datetime
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


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
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class EmploymentHistory:
    company: str | None
    date_from: date
    date_to: date | None
    is_currently_working: bool
    updated_at: datetime
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class Training:
    training_title: str | None
    training_description: str | None
    training_date: date
    topic_label: str | None
    level_label: str | None
    updated_at: datetime
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class Task:
    title: str | None
    details: str | None
    category_label: str | None
    updated_at: datetime
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class UserSkill:
    skill_name: str | None
    level: int
    updated_at: datetime
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class EmployeeData:
    employee_id: int
    user_detail: UserDetail | None
    cv: Cv | None
    experiences: list[Experience]
    employment_histories: list[EmploymentHistory]
    trainings: list[Training]
    tasks: list[Task]
    skills: list[UserSkill]

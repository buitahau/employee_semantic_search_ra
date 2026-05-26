from dataclasses import dataclass, field

from common.types import ChunkRecord, UserDetail


@dataclass
class CvState:
    text: str | None
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class ExperienceState:
    text: str | None
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class EmploymentHistoryState:
    text: str | None
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class TrainingState:
    text: str | None
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class TaskState:
    text: str | None
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class UserSkillState:
    text: str | None
    chunks: list[ChunkRecord] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    pipeline_state: dict = field(default_factory=dict)


@dataclass
class EtlPipelineState:
    employee_id: int
    user_detail: UserDetail | None = None
    cv: CvState | None = None
    experiences: ExperienceState| None = None 
    employment_histories: EmploymentHistoryState| None = None 
    trainings: TrainingState| None = None 
    task: TaskState | None = None 
    skills: UserSkillState| None = None 

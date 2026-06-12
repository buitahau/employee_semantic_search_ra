from common.states import EtlPipelineState
from common.types import UserDetail

_SECTION_LABEL_BY_ATTR: dict[str, str] = {
    "user_detail": "User Detail",
    "cv": "CV",
    "experiences": "Experience",
    "employment_histories": "Employment History",
    "trainings": "Training",
    "task": "Task",
    "skills": "Skills",
}


def _build_header(user_detail: UserDetail | None, section_label: str) -> str:
    fields: list[str] = []
    if user_detail:
        name = " ".join(p for p in (user_detail.first_name, user_detail.last_name) if p)
        if name and user_detail.trigram:
            fields.append(f"Employee: {name} ({user_detail.trigram})")
        elif name:
            fields.append(f"Employee: {name}")
        elif user_detail.trigram:
            fields.append(f"Employee: ({user_detail.trigram})")

        if user_detail.position:
            fields.append(f"Position: {user_detail.position}")
        if user_detail.level:
            fields.append(f"Level: {user_detail.level}")

    fields.append(f"Section: {section_label}")
    return "[" + " | ".join(fields) + "]"


def prepend_headers(state: EtlPipelineState, user_detail: UserDetail | None) -> EtlPipelineState:
    for attr, section_label in _SECTION_LABEL_BY_ATTR.items():
        entity = getattr(state, attr)
        if entity and entity.text:
            header = _build_header(user_detail, section_label)
            entity.text = f"{header}\n\n{entity.text}"
    return state

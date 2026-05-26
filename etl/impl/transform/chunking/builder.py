from common.constants import PREPROCESS_VERSION
from common.states import EtlPipelineState
from common.types import ChunkRecord

_FIELD_TYPE_BY_ATTR: dict[str, str] = {
    "cv": "cv",
    "experiences": "experience",
    "employment_histories": "employment_history",
    "trainings": "training",
    "task": "task",
    "skills": "user_skill",
}


def _make_chunks(employee_id: int, field_type: str, windows: list, metadata: dict) -> list[ChunkRecord]:
    return [
        ChunkRecord(
            employee_id=employee_id,
            field_type=field_type,
            chunk_text=text,
            chunk_index=i,
            char_start=char_start,
            char_end=char_end,
            token_count=token_count,
            preprocess_version=str(PREPROCESS_VERSION),
            metadata=metadata,
        )
        for i, (text, char_start, char_end, token_count) in enumerate(windows)
    ]


def _fill_chunks(state: EtlPipelineState) -> EtlPipelineState:
    for attr, field_type in _FIELD_TYPE_BY_ATTR.items():
        entity = getattr(state, attr)
        if entity:
            windows = entity.pipeline_state.get("windows", [])
            entity.chunks = _make_chunks(state.employee_id, field_type, windows, entity.metadata)
    return state

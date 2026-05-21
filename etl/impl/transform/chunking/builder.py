from common.constants import PREPROCESS_VERSION
from common.types import ChunkRecord, EmployeeData


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


def _fill_chunks(data: EmployeeData) -> EmployeeData:
    if data.cv:
        windows = data.cv.pipeline_state.get("windows", [])
        data.cv.chunks = _make_chunks(data.employee_id, "cv", windows, data.cv.metadata)

    for exp in data.experiences:
        windows = exp.pipeline_state.get("windows", [])
        exp.chunks = _make_chunks(data.employee_id, "experience", windows, exp.metadata)

    for hist in data.employment_histories:
        windows = hist.pipeline_state.get("windows", [])
        hist.chunks = _make_chunks(data.employee_id, "employment_history", windows, hist.metadata)

    for training in data.trainings:
        windows = training.pipeline_state.get("windows", [])
        training.chunks = _make_chunks(data.employee_id, "training", windows, training.metadata)

    for task in data.tasks:
        windows = task.pipeline_state.get("windows", [])
        task.chunks = _make_chunks(data.employee_id, "task", windows, task.metadata)

    for skill in data.skills:
        windows = skill.pipeline_state.get("windows", [])
        skill.chunks = _make_chunks(data.employee_id, "user_skill", windows, skill.metadata)

    return data

from common.logging import get_logger
from common.states import EtlPipelineState
from common.types import ChunkRecord
from etl.extract import extract_employee
from etl.load import load_employee
from etl.transform import transform

_logger = get_logger(__name__)

_STATE_ATTRS = ("cv", "experiences", "employment_histories", "trainings", "task", "skills")


def _collect_chunks(state: EtlPipelineState) -> list[ChunkRecord]:
    chunks: list[ChunkRecord] = []
    for attr in _STATE_ATTRS:
        entity = getattr(state, attr)
        if entity:
            chunks.extend(entity.chunks)
    for i, chunk in enumerate(chunks):
        chunk.chunk_index = i
    return chunks


def run_employee_pipeline(employee_id: int) -> int:
    raw = extract_employee(employee_id)
    state = transform(raw)
    chunks = _collect_chunks(state)
    _logger.info("employee_id=%d collected %d chunks", employee_id, len(chunks))
    for chunk in chunks:
        _logger.info(
            "employee_id=%d chunk_index=%d field_type=%s token_count=%d char_start=%d char_end=%d",
            employee_id,
            chunk.chunk_index,
            chunk.field_type,
            chunk.token_count,
            chunk.char_start,
            chunk.char_end,
        )
    load_employee(employee_id, chunks)
    return len(chunks)

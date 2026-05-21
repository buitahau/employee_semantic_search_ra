from common.constants import PREPROCESS_VERSION
from common.types import ChunkRecord


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

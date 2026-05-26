from common.states import EtlPipelineState
from etl.impl.transform.chunking.embedding.encoder import embed

_STATE_ATTRS = ("cv", "experiences", "employment_histories", "trainings", "task", "skills")


def embed_chunks(state: EtlPipelineState) -> EtlPipelineState:
    for attr in _STATE_ATTRS:
        entity = getattr(state, attr)
        if entity:
            for chunk in entity.chunks:
                chunk.embedding = embed(chunk.chunk_text)
    return state

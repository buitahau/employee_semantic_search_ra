from common.states import EtlPipelineState
from etl.impl.transform.chunking.tokenizer import _fill_token_counts
from etl.impl.transform.chunking.splitter import _fill_sentences
from etl.impl.transform.chunking.accumulator import _fill_windows
from etl.impl.transform.chunking.builder import _fill_chunks
from etl.impl.transform.chunking.embedding import embed_chunks


def chunking(state: EtlPipelineState) -> EtlPipelineState:
    state = _fill_token_counts(state)
    state = _fill_sentences(state)
    state = _fill_windows(state)
    state = _fill_chunks(state)
    state = embed_chunks(state)
    return state

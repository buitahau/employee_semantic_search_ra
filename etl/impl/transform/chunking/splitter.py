import re

from common.states import EtlPipelineState

_SENT_BOUNDARY = re.compile(r'(?<=[.!?])\s+')

_STATE_ATTRS = ("cv", "experiences", "employment_histories", "trainings", "task", "skills")


def _split_sentences(text: str) -> list[tuple[str, int, int]]:
    """Returns [(sentence_text, char_start, char_end), ...]."""
    if not text or not text.strip():
        return []
    sentences = []
    pos = 0
    for m in _SENT_BOUNDARY.finditer(text):
        span = text[pos : m.start() + 1].strip()
        if span:
            sentences.append((span, pos, m.start() + 1))
        pos = m.end()
    tail = text[pos:].strip()
    if tail:
        sentences.append((tail, pos, len(text)))
    return sentences


def _fill_sentences(state: EtlPipelineState) -> EtlPipelineState:
    for attr in _STATE_ATTRS:
        entity = getattr(state, attr)
        if entity and entity.text:
            entity.pipeline_state["sentences"] = _split_sentences(entity.text)
    return state

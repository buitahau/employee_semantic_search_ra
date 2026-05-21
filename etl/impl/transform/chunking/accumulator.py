from typing import Callable
from .tokenizer import _count_tokens as _default_count_tokens, _get_tokenizer
from common.types import EmployeeData

TOKENS_MAX = 250
OVERLAP_MIN = 40

_TOKENS_MAX_BY_SOURCE: dict[str, int] = {
    "cv": TOKENS_MAX,
    "experience": TOKENS_MAX,
    "employment_history": 200,
    "training": 200,
    "task": 200,
    "user_skill": 200,
}

_PREFIX_BY_SOURCE: dict[str, str] = {
    "cv": "CV: ",
    "experience": "Experience: ",
    "employment_history": "Employment: ",
    "training": "Training: ",
    "task": "Task: ",
    "user_skill": "Skill: ",
}


def _token_window_split(
    text: str,
    char_offset: int = 0,
    max_tokens: int = TOKENS_MAX,
    overlap_tokens: int = OVERLAP_MIN,
) -> list[tuple[str, int, int]]:
    enc = _get_tokenizer().encode(text)
    ids = enc.ids
    offsets = enc.offsets
    step = max_tokens - overlap_tokens
    windows = []
    i = 0
    while i < len(ids):
        end = min(i + max_tokens, len(ids))
        t_start = offsets[i][0]
        t_end = offsets[end - 1][1]
        windows.append((text[t_start:t_end], char_offset + t_start, char_offset + t_end))
        if end == len(ids):
            break
        i += step
    return windows


def _build_overlap(
    current: list[tuple[str, int, int]],
    fn: Callable[[str], int],
) -> list[tuple[str, int, int]]:
    overlap: list[tuple[str, int, int]] = []
    total = 0
    for s in reversed(current):
        overlap.insert(0, s)
        total += fn(s[0])
        if total >= OVERLAP_MIN:
            break
    return overlap


def _accumulate_windows(
    sentences: list[tuple[str, int, int]],
    prefix: str,
    tokens_max: int = TOKENS_MAX,
    count_fn: Callable[[str], int] | None = None,
) -> list[tuple[str, int, int, int]]:
    """
    Returns [(window_text, char_start, char_end, token_count), ...].

    tokens_max: per-source-type budget passed from chunk_text().
    count_fn defaults to None. When None, _default_count_tokens is used at call
    time so that unittest.mock.patch on the tokenizer module takes effect.
    """
    fn = count_fn if count_fn is not None else _default_count_tokens
    current: list[tuple[str, int, int]] = []
    windows: list[tuple[str, int, int, int]] = []

    def emit_window(sentences: list[tuple[str, int, int]]) -> None:
        window_text = " ".join(t for t, _, _ in sentences)
        char_start = sentences[0][1]
        char_end = sentences[-1][2]
        windows.append((window_text, char_start, char_end, fn(window_text)))

    for s in sentences:
        s_text, s_start, s_end = s

        if fn(s_text) > tokens_max:
            if current:
                emit_window(current)
                current = []
            for sub in _token_window_split(s_text, char_offset=s_start, max_tokens=tokens_max):
                emit_window([sub])
            continue

        candidate = prefix + " ".join(t for t, _, _ in current + [s])
        if fn(candidate) > tokens_max and current:
            emit_window(current)
            current = _build_overlap(current, fn)

        current.append(s)

    if current:
        emit_window(current)

    return windows


def _fill_windows(data: EmployeeData) -> EmployeeData:
    if data.cv:
        sentences = data.cv.pipeline_state.get("sentences", [])
        if sentences:
            data.cv.pipeline_state["windows"] = _accumulate_windows(
                sentences,
                prefix=_PREFIX_BY_SOURCE["cv"],
                tokens_max=_TOKENS_MAX_BY_SOURCE["cv"],
            )

    for exp in data.experiences:
        sentences = exp.pipeline_state.get("sentences", [])
        if sentences:
            exp.pipeline_state["windows"] = _accumulate_windows(
                sentences,
                prefix=_PREFIX_BY_SOURCE["experience"],
                tokens_max=_TOKENS_MAX_BY_SOURCE["experience"],
            )

    for hist in data.employment_histories:
        sentences = hist.pipeline_state.get("sentences", [])
        if sentences:
            hist.pipeline_state["windows"] = _accumulate_windows(
                sentences,
                prefix=_PREFIX_BY_SOURCE["employment_history"],
                tokens_max=_TOKENS_MAX_BY_SOURCE["employment_history"],
            )

    for training in data.trainings:
        sentences = training.pipeline_state.get("sentences", [])
        if sentences:
            training.pipeline_state["windows"] = _accumulate_windows(
                sentences,
                prefix=_PREFIX_BY_SOURCE["training"],
                tokens_max=_TOKENS_MAX_BY_SOURCE["training"],
            )

    for task in data.tasks:
        sentences = task.pipeline_state.get("sentences", [])
        if sentences:
            task.pipeline_state["windows"] = _accumulate_windows(
                sentences,
                prefix=_PREFIX_BY_SOURCE["task"],
                tokens_max=_TOKENS_MAX_BY_SOURCE["task"],
            )

    for skill in data.skills:
        sentences = skill.pipeline_state.get("sentences", [])
        if sentences:
            skill.pipeline_state["windows"] = _accumulate_windows(
                sentences,
                prefix=_PREFIX_BY_SOURCE["user_skill"],
                tokens_max=_TOKENS_MAX_BY_SOURCE["user_skill"],
            )

    return data

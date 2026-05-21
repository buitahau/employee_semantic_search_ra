import re
from common.types import EmployeeData

_SENT_BOUNDARY = re.compile(r'(?<=[.!?])\s+')


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


def _join(*values: str | None) -> str:
    return " ".join(v for v in values if v)


def _fill_sentences(data: EmployeeData) -> EmployeeData:
    if data.cv:
        text = _join(data.cv.cv, data.cv.custom_position, data.cv.introduction)
        if text:
            data.cv.pipeline_state["sentences"] = _split_sentences(text)

    for exp in data.experiences:
        text = _join(exp.project_name, exp.domain, exp.description, exp.roles_and_responsibilities)
        if text:
            exp.pipeline_state["sentences"] = _split_sentences(text)

    for hist in data.employment_histories:
        text = _join(hist.company)
        if text:
            hist.pipeline_state["sentences"] = _split_sentences(text)

    for training in data.trainings:
        text = _join(training.training_title, training.training_description, training.topic_label, training.level_label)
        if text:
            training.pipeline_state["sentences"] = _split_sentences(text)

    for task in data.tasks:
        text = _join(task.title, task.details, task.category_label)
        if text:
            task.pipeline_state["sentences"] = _split_sentences(text)

    for skill in data.skills:
        text = _join(skill.skill_name)
        if text:
            skill.pipeline_state["sentences"] = _split_sentences(text)

    return data

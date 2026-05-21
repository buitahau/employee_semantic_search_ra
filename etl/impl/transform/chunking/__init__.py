from common.types import EmployeeData
from etl.impl.transform.chunking.tokenizer import _count_tokens
from etl.impl.transform.chunking.splitter import _split_sentences
from etl.impl.transform.chunking.accumulator import _accumulate_windows, TOKENS_MAX


def _join(*values: str | None) -> str:
    return " ".join(v for v in values if v)


def _fill_token_counts(data: EmployeeData) -> EmployeeData:
    if data.cv:
        text = _join(data.cv.cv, data.cv.custom_position, data.cv.introduction)
        data.cv.pipeline_state["token_count"] = _count_tokens(text) if text else 0

    for exp in data.experiences:
        text = _join(exp.project_name, exp.domain, exp.description, exp.roles_and_responsibilities)
        exp.pipeline_state["token_count"] = _count_tokens(text) if text else 0

    for hist in data.employment_histories:
        text = _join(hist.company)
        hist.pipeline_state["token_count"] = _count_tokens(text) if text else 0

    for training in data.trainings:
        text = _join(training.training_title, training.training_description, training.topic_label, training.level_label)
        training.pipeline_state["token_count"] = _count_tokens(text) if text else 0

    for task in data.tasks:
        text = _join(task.title, task.details, task.category_label)
        task.pipeline_state["token_count"] = _count_tokens(text) if text else 0

    for skill in data.skills:
        text = _join(skill.skill_name)
        skill.pipeline_state["token_count"] = _count_tokens(text) if text else 0

    return data


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


def chunking(data: EmployeeData) -> EmployeeData:
    data = _fill_token_counts(data)
    data = _fill_sentences(data)
    data = _fill_windows(data)
    return data

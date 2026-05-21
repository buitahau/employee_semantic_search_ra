from common.types import EmployeeData
from etl.impl.transform.chunking.tokenizer import _count_tokens


def _join(*values: str | None) -> str:
    return " ".join(v for v in values if v)


def _fill_token_counts(data: EmployeeData) -> EmployeeData:
    if data.cv:
        text = _join(data.cv.cv, data.cv.custom_position, data.cv.introduction)
        data.cv.metadata["token_count"] = _count_tokens(text) if text else 0

    for exp in data.experiences:
        text = _join(exp.project_name, exp.domain, exp.description, exp.roles_and_responsibilities)
        exp.metadata["token_count"] = _count_tokens(text) if text else 0

    for hist in data.employment_histories:
        text = _join(hist.company)
        hist.metadata["token_count"] = _count_tokens(text) if text else 0

    for training in data.trainings:
        text = _join(training.training_title, training.training_description, training.topic_label, training.level_label)
        training.metadata["token_count"] = _count_tokens(text) if text else 0

    for task in data.tasks:
        text = _join(task.title, task.details, task.category_label)
        task.metadata["token_count"] = _count_tokens(text) if text else 0

    for skill in data.skills:
        text = _join(skill.skill_name)
        skill.metadata["token_count"] = _count_tokens(text) if text else 0

    return data


def chunking(data: EmployeeData) -> EmployeeData:
    data = _fill_token_counts(data)
    return data

from pathlib import Path
from tokenizers import Tokenizer
from common.config import settings
from common.types import EmployeeData

_tokenizer: Tokenizer | None = None


def _get_tokenizer() -> Tokenizer:
    global _tokenizer
    if _tokenizer is None:
        model_dir = Path(settings.embedding_model_path).parent
        _tokenizer = Tokenizer.from_file(str(model_dir / "tokenizer.json"))
        _tokenizer.no_padding()
        _tokenizer.no_truncation()
    return _tokenizer


def _count_tokens(text: str) -> int:
    return len(_get_tokenizer().encode(text).ids)


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

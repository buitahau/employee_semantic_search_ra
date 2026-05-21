from datetime import date, datetime
from unittest.mock import patch

from common.types import (
    Cv,
    EmployeeData,
    EmploymentHistory,
    Experience,
    Task,
    Training,
    UserDetail,
    UserSkill,
)
from etl.impl.transform.chunking import chunking


def _make_employee(**overrides) -> EmployeeData:
    defaults = dict(
        employee_id=1,
        user_detail=None,
        cv=None,
        experiences=[],
        employment_histories=[],
        trainings=[],
        tasks=[],
        skills=[],
    )
    defaults.update(overrides)
    return EmployeeData(**defaults)


# Patch _count_tokens so tests don't need the ONNX model on disk.
# The patch returns the number of words as a stand-in for real token counts.
def _fake_count(text: str) -> int:
    return len(text.split())


@patch("etl.impl.transform.chunking.tokenizer._get_tokenizer")
def _noop(mock_get):
    pass  # only used to silence import; real patching is per-test via decorator


# --- Cv ---

def test_cv_token_count_populated():
    cv = Cv(cv="hello world", custom_position="engineer", introduction="I am great", updated_at=datetime.now())
    data = _make_employee(cv=cv)
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count):
        result = chunking(data)
    # "hello world engineer I am great" → 6 words
    assert result.cv.metadata["token_count"] == 6


def test_cv_token_count_none_fields():
    cv = Cv(cv=None, custom_position=None, introduction=None, updated_at=datetime.now())
    data = _make_employee(cv=cv)
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count):
        result = chunking(data)
    assert result.cv.metadata["token_count"] == 0


def test_no_cv_skipped():
    data = _make_employee(cv=None)
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count) as mock:
        chunking(data)
    mock.assert_not_called()


# --- Experience ---

def test_experience_token_count():
    exp = Experience(
        project_name="Project X",
        domain="Finance",
        description="built a system",
        roles_and_responsibilities="lead dev",
        date_from=date.today(),
        date_to=None,
        is_currently_working=True,
        skills=[],
        updated_at=datetime.now(),
    )
    data = _make_employee(experiences=[exp])
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count):
        result = chunking(data)
    # "Project X Finance built a system lead dev" → 8 words
    assert result.experiences[0].metadata["token_count"] == 8


# --- EmploymentHistory ---

def test_employment_history_token_count():
    hist = EmploymentHistory(
        company="Acme Corp",
        date_from=date.today(),
        date_to=None,
        is_currently_working=True,
        updated_at=datetime.now(),
    )
    data = _make_employee(employment_histories=[hist])
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count):
        result = chunking(data)
    assert result.employment_histories[0].metadata["token_count"] == 2


# --- Training ---

def test_training_token_count():
    training = Training(
        training_title="Python basics",
        training_description="intro course",
        training_date=date.today(),
        topic_label="programming",
        level_label="beginner",
        updated_at=datetime.now(),
    )
    data = _make_employee(trainings=[training])
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count):
        result = chunking(data)
    # "Python basics intro course programming beginner" → 6 words
    assert result.trainings[0].metadata["token_count"] == 6


# --- Task ---

def test_task_token_count():
    task = Task(
        title="Fix bug",
        details="resolve null pointer",
        category_label="engineering",
        updated_at=datetime.now(),
    )
    data = _make_employee(tasks=[task])
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count):
        result = chunking(data)
    # "Fix bug resolve null pointer engineering" → 6 words
    assert result.tasks[0].metadata["token_count"] == 6


# --- UserSkill ---

def test_skill_token_count():
    skill = UserSkill(skill_name="machine learning", level=3, updated_at=datetime.now())
    data = _make_employee(skills=[skill])
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count):
        result = chunking(data)
    assert result.skills[0].metadata["token_count"] == 2


def test_skill_none_name():
    skill = UserSkill(skill_name=None, level=1, updated_at=datetime.now())
    data = _make_employee(skills=[skill])
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count):
        result = chunking(data)
    assert result.skills[0].metadata["token_count"] == 0


# --- multiple items ---

def test_multiple_experiences_each_get_token_count():
    exps = [
        Experience(project_name="A", domain=None, description=None, roles_and_responsibilities=None,
                   date_from=date.today(), date_to=None, is_currently_working=False, skills=[], updated_at=datetime.now()),
        Experience(project_name="B C", domain=None, description=None, roles_and_responsibilities=None,
                   date_from=date.today(), date_to=None, is_currently_working=False, skills=[], updated_at=datetime.now()),
    ]
    data = _make_employee(experiences=exps)
    with patch("etl.impl.transform.chunking._count_tokens", side_effect=_fake_count):
        result = chunking(data)
    assert result.experiences[0].metadata["token_count"] == 1
    assert result.experiences[1].metadata["token_count"] == 2

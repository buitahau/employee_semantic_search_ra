from datetime import date, datetime
from unittest.mock import MagicMock, patch

import pytest

from etl.extract import (
    _get_cv,
    _get_employment_histories,
    _get_experiences,
    _get_tasks,
    _get_trainings,
    _get_user_skills,
    extract_employee,
)
from common.types import (
    Cv,
    EmployeeData,
    EmploymentHistory,
    Experience,
    Task,
    Training,
    UserSkill,
)

_NOW = datetime(2024, 1, 15, 10, 0, 0)
_TODAY = date(2024, 1, 15)


def _mock_cur():
    return MagicMock()


# --- get_cv ---

def test_get_cv_returns_cv():
    cur = _mock_cur()
    cur.fetchone.return_value = {
        "cv": "my cv text",
        "custom_position": "Senior Dev",
        "introduction": "intro",
        "updated_at": _NOW,
    }
    result = _get_cv(cur, employee_id=1)
    assert isinstance(result, Cv)
    assert result.cv == "my cv text"
    assert result.custom_position == "Senior Dev"
    assert result.introduction == "intro"
    assert result.updated_at == _NOW


def test_get_cv_returns_none_when_no_row():
    cur = _mock_cur()
    cur.fetchone.return_value = None
    result = _get_cv(cur, employee_id=999)
    assert result is None


def test_get_cv_nullable_fields():
    cur = _mock_cur()
    cur.fetchone.return_value = {
        "cv": None,
        "custom_position": None,
        "introduction": None,
        "updated_at": _NOW,
    }
    result = _get_cv(cur, employee_id=1)
    assert result.cv is None
    assert result.custom_position is None


# --- get_experiences ---

def test_get_experiences_resolves_skills():
    cur = _mock_cur()
    cur.fetchall.return_value = [
        {
            "project_name": "Project A",
            "domain": "Finance",
            "description": "desc",
            "roles_and_responsibilities": "dev",
            "date_from": _TODAY,
            "date_to": None,
            "is_currently_working": True,
            "skills": ["Python", "SQL"],
            "updated_at": _NOW,
        }
    ]
    result = _get_experiences(cur, employee_id=1)
    assert len(result) == 1
    exp = result[0]
    assert isinstance(exp, Experience)
    assert exp.skills == ["Python", "SQL"]
    assert exp.is_currently_working is True
    assert exp.date_to is None


def test_get_experiences_empty_skills():
    cur = _mock_cur()
    cur.fetchall.return_value = [
        {
            "project_name": "Solo",
            "domain": None,
            "description": None,
            "roles_and_responsibilities": None,
            "date_from": _TODAY,
            "date_to": _TODAY,
            "is_currently_working": False,
            "skills": [],
            "updated_at": _NOW,
        }
    ]
    result = _get_experiences(cur, employee_id=1)
    assert result[0].skills == []


def test_get_experiences_returns_empty_list():
    cur = _mock_cur()
    cur.fetchall.return_value = []
    assert _get_experiences(cur, employee_id=999) == []


# --- get_employment_histories ---

def test_get_employment_histories_happy_path():
    cur = _mock_cur()
    cur.fetchall.return_value = [
        {
            "company": "Acme",
            "date_from": _TODAY,
            "date_to": None,
            "is_currently_working": True,
            "updated_at": _NOW,
        }
    ]
    result = _get_employment_histories(cur, employee_id=1)
    assert len(result) == 1
    assert isinstance(result[0], EmploymentHistory)
    assert result[0].company == "Acme"


def test_get_employment_histories_returns_empty_list():
    cur = _mock_cur()
    cur.fetchall.return_value = []
    assert _get_employment_histories(cur, employee_id=999) == []


# --- get_trainings ---

def test_get_trainings_happy_path():
    cur = _mock_cur()
    cur.fetchall.return_value = [
        {
            "training_title": "Python 101",
            "training_description": "basics",
            "training_date": _TODAY,
            "topic_label": "Engineering",
            "level_label": "Beginner",
            "updated_at": _NOW,
        }
    ]
    result = _get_trainings(cur, employee_id=1)
    assert len(result) == 1
    t = result[0]
    assert isinstance(t, Training)
    assert t.topic_label == "Engineering"
    assert t.level_label == "Beginner"


def test_get_trainings_returns_empty_list():
    cur = _mock_cur()
    cur.fetchall.return_value = []
    assert _get_trainings(cur, employee_id=999) == []


# --- get_tasks ---

def test_get_tasks_happy_path():
    cur = _mock_cur()
    cur.fetchall.return_value = [
        {
            "title": "Fix bug",
            "details": "details here",
            "category_label": "Backend",
            "updated_at": _NOW,
        }
    ]
    result = _get_tasks(cur, employee_id=1)
    assert len(result) == 1
    assert isinstance(result[0], Task)
    assert result[0].category_label == "Backend"


def test_get_tasks_returns_empty_list():
    cur = _mock_cur()
    cur.fetchall.return_value = []
    assert _get_tasks(cur, employee_id=999) == []


# --- get_user_skills ---

def test_get_user_skills_happy_path():
    cur = _mock_cur()
    cur.fetchall.return_value = [
        {"skill_name": "Python", "level": 4, "updated_at": _NOW},
        {"skill_name": "Docker", "level": 3, "updated_at": _NOW},
    ]
    result = _get_user_skills(cur, employee_id=1)
    assert len(result) == 2
    assert isinstance(result[0], UserSkill)
    assert result[0].skill_name == "Python"
    assert result[0].level == 4


def test_get_user_skills_returns_empty_list():
    cur = _mock_cur()
    cur.fetchall.return_value = []
    assert _get_user_skills(cur, employee_id=999) == []


# --- extract_employee ---

def test_extract_employee_unknown_employee():
    with patch("etl.extract._connect") as mock_connect:
        cur = _mock_cur()
        cur.fetchone.return_value = None
        cur.fetchall.return_value = []
        mock_connect.return_value.__enter__ = lambda _: cur
        mock_connect.return_value.__exit__ = MagicMock(return_value=False)

        data = extract_employee(employee_id=999999)

    assert isinstance(data, EmployeeData)
    assert data.employee_id == 999999
    assert data.cv is None
    assert data.experiences == []
    assert data.employment_histories == []
    assert data.trainings == []
    assert data.tasks == []
    assert data.skills == []


def test_extract_employee_assembles_all_fields():
    cv_row = {
        "cv": "cv text",
        "custom_position": "Dev",
        "introduction": "hi",
        "updated_at": _NOW,
    }
    skill_rows = [{"skill_name": "Go", "level": 5, "updated_at": _NOW}]

    with patch("etl.extract._connect") as mock_connect:
        cur = _mock_cur()
        cur.fetchone.return_value = cv_row
        cur.fetchall.return_value = skill_rows
        mock_connect.return_value.__enter__ = lambda _: cur
        mock_connect.return_value.__exit__ = MagicMock(return_value=False)

        data = extract_employee(employee_id=1)

    assert data.employee_id == 1
    assert data.cv is not None
    assert data.cv.cv == "cv text"

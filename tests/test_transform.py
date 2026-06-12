from datetime import date, datetime
from unittest.mock import patch

from common.types import (
    Cv,
    EmployeeData,
    Experience,
    UserDetail,
)
from etl.transform import transform


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


def _fake_count(text: str) -> int:
    return len(text.split())


def _fake_embed(text: str) -> list[float]:
    return [0.0]


@patch("etl.impl.transform.chunking.embedding.embed", side_effect=_fake_embed)
@patch("etl.impl.transform.chunking.tokenizer._count_tokens", side_effect=_fake_count)
def test_transform_prepends_header_to_chunks(_mock_count, _mock_embed):
    user_detail = UserDetail(
        first_name="Jane",
        last_name="Doe",
        trigram="JDO",
        company_email="jane.doe@owt.swiss",
        gender="FEMALE",
        date_of_birth=None,
        university=None,
        position="Software Engineer",
        level="Senior",
        contract_type="FULLTIME",
        start_date=date(2020, 1, 1),
        updated_at=datetime(2026, 1, 1),
    )
    cv = Cv(cv="Experienced backend engineer.", custom_position=None, introduction=None, updated_at=datetime.now())
    exp = Experience(
        project_name="Search Project",
        domain=None,
        description="Worked on the search project.",
        roles_and_responsibilities=None,
        date_from=date.today(),
        date_to=None,
        is_currently_working=True,
        skills=[],
        updated_at=datetime.now(),
    )
    data = _make_employee(user_detail=user_detail, cv=cv, experiences=[exp])

    state = transform(data)

    assert state.cv.chunks, "expected at least one CV chunk"
    cv_header = "[Employee: Jane Doe (JDO) | Position: Software Engineer | Level: Senior | Section: CV]"
    assert state.cv.chunks[0].chunk_text.startswith(cv_header)
    assert "Experienced backend engineer." in state.cv.chunks[0].chunk_text

    assert state.experiences.chunks, "expected at least one experience chunk"
    exp_header = "[Employee: Jane Doe (JDO) | Position: Software Engineer | Level: Senior | Section: Experience]"
    assert state.experiences.chunks[0].chunk_text.startswith(exp_header)
    assert "Worked on the search project." in state.experiences.chunks[0].chunk_text


@patch("etl.impl.transform.chunking.embedding.embed", side_effect=_fake_embed)
@patch("etl.impl.transform.chunking.tokenizer._count_tokens", side_effect=_fake_count)
def test_transform_no_user_detail_uses_section_only_header(_mock_count, _mock_embed):
    cv = Cv(cv="Experienced backend engineer.", custom_position=None, introduction=None, updated_at=datetime.now())
    data = _make_employee(user_detail=None, cv=cv)

    state = transform(data)

    assert state.cv.chunks[0].chunk_text.startswith("[Section: CV]")

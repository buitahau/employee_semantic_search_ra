from datetime import date, datetime

from common.states import CvState, EtlPipelineState, ExperienceState, UserDetailState
from common.types import UserDetail
from etl.impl.transform.header import _build_header, prepend_headers


def _make_user_detail(**overrides) -> UserDetail:
    defaults = dict(
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
    defaults.update(overrides)
    return UserDetail(**defaults)


def test_build_header_full_identity():
    header = _build_header(_make_user_detail(), "Experience")
    assert header == "[Employee: Jane Doe (JDO) | Position: Software Engineer | Level: Senior | Section: Experience]"


def test_build_header_missing_level():
    header = _build_header(_make_user_detail(level=None), "Training")
    assert header == "[Employee: Jane Doe (JDO) | Position: Software Engineer | Section: Training]"


def test_build_header_missing_position_and_level():
    header = _build_header(_make_user_detail(position=None, level=None), "CV")
    assert header == "[Employee: Jane Doe (JDO) | Section: CV]"


def test_build_header_no_user_detail():
    header = _build_header(None, "CV")
    assert header == "[Section: CV]"


def test_prepend_headers_adds_header_before_text():
    state = EtlPipelineState(
        employee_id=1,
        user_detail=UserDetailState(text="Jane Doe JDO jane.doe@owt.swiss FEMALE FULLTIME"),
        cv=CvState(text="Experienced backend engineer."),
        experiences=ExperienceState(text="Worked on the search project."),
    )

    state = prepend_headers(state, _make_user_detail())

    assert state.user_detail.text == (
        "[Employee: Jane Doe (JDO) | Position: Software Engineer | Level: Senior | Section: User Detail]"
        "\n\nJane Doe JDO jane.doe@owt.swiss FEMALE FULLTIME"
    )
    assert state.cv.text == (
        "[Employee: Jane Doe (JDO) | Position: Software Engineer | Level: Senior | Section: CV]"
        "\n\nExperienced backend engineer."
    )
    assert state.experiences.text == (
        "[Employee: Jane Doe (JDO) | Position: Software Engineer | Level: Senior | Section: Experience]"
        "\n\nWorked on the search project."
    )


def test_prepend_headers_skips_empty_text():
    state = EtlPipelineState(
        employee_id=1,
        cv=CvState(text=None),
        experiences=None,
    )

    state = prepend_headers(state, _make_user_detail())

    assert state.cv.text is None
    assert state.experiences is None

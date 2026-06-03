from psycopg2.extras import RealDictCursor

from common.db import _connect
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


def _get_user_detail(cur: RealDictCursor, employee_id: int) -> UserDetail | None:
    cur.execute(
        """
        SELECT
            u.first_name,
            u.last_name,
            u.trigram,
            u.company_email,
            u.gender,
            u.date_of_birth,
            u.university,
            u.contract_type,
            u.start_date,
            p.name   AS position,
            ul.label AS level,
            u.updated_at
        FROM users u
        LEFT JOIN positions   p  ON p.id  = u.position_id
        LEFT JOIN user_levels ul ON ul.id = u.level_id
        WHERE u.id = %(employee_id)s;
        """,
        {"employee_id": employee_id},
    )
    row = cur.fetchone()
    if row is None:
        return None
    return UserDetail(
        first_name=row["first_name"],
        last_name=row["last_name"],
        trigram=row["trigram"],
        company_email=row["company_email"],
        gender=row["gender"],
        date_of_birth=row["date_of_birth"],
        university=row["university"],
        position=row["position"],
        level=row["level"],
        contract_type=row["contract_type"],
        start_date=row["start_date"],
        updated_at=row["updated_at"],
    )


def _get_cv(cur: RealDictCursor, employee_id: int) -> Cv | None:
    cur.execute(
        """
        SELECT
            uc.cv,
            co.custom_position,
            co.introduction,
            GREATEST(uc.updated_at, co.updated_at) AS updated_at
        FROM user_cvs uc
        LEFT JOIN cv_overview co ON co.user_id = uc.user_id
        WHERE uc.user_id = %(employee_id)s
        ORDER BY uc.updated_at DESC
        LIMIT 1;
        """,
        {"employee_id": employee_id},
    )
    row = cur.fetchone()
    if row is None:
        return None
    return Cv(
        cv=row["cv"],
        custom_position=row["custom_position"],
        introduction=row["introduction"],
        updated_at=row["updated_at"],
    )


def _get_experiences(cur: RealDictCursor, employee_id: int) -> list[Experience]:
    cur.execute(
        """
        SELECT
            e.project_name,
            e.domain,
            e.description,
            e.roles_and_responsibilities,
            e.date_from,
            e.date_to,
            e.is_currently_working,
            e.updated_at,
            COALESCE(
                array_agg(s.name) FILTER (WHERE s.name IS NOT NULL),
                '{}'
            ) AS skills
        FROM experiences e
        LEFT JOIN experience_skills es ON es.experience_id = e.id
        LEFT JOIN skills s ON s.id = es.skill_id
        WHERE e.user_id = %(employee_id)s
        GROUP BY e.id;
        """,
        {"employee_id": employee_id},
    )
    return [
        Experience(
            project_name=row["project_name"],
            domain=row["domain"],
            description=row["description"],
            roles_and_responsibilities=row["roles_and_responsibilities"],
            date_from=row["date_from"],
            date_to=row["date_to"],
            is_currently_working=row["is_currently_working"],
            skills=list(row["skills"]),
            updated_at=row["updated_at"],
        )
        for row in cur.fetchall()
    ]


def _get_employment_histories(cur: RealDictCursor, employee_id: int) -> list[EmploymentHistory]:
    cur.execute(
        """
        SELECT
            company,
            date_from,
            date_to,
            is_currently_working,
            updated_at
        FROM employment_histories
        WHERE user_id = %(employee_id)s;
        """,
        {"employee_id": employee_id},
    )
    return [
        EmploymentHistory(
            company=row["company"],
            date_from=row["date_from"],
            date_to=row["date_to"],
            is_currently_working=row["is_currently_working"],
            updated_at=row["updated_at"],
        )
        for row in cur.fetchall()
    ]


def _get_trainings(cur: RealDictCursor, employee_id: int) -> list[Training]:
    cur.execute(
        """
        SELECT
            t.training_title,
            t.training_description,
            t.training_date,
            tt.label  AS topic_label,
            tl.label  AS level_label,
            t.updated_at
        FROM trainings t
        LEFT JOIN training_topics tt ON tt.id = t.topic_id
        LEFT JOIN training_levels tl ON tl.id = t.level_id
        WHERE t.user_id = %(employee_id)s;
        """,
        {"employee_id": employee_id},
    )
    return [
        Training(
            training_title=row["training_title"],
            training_description=row["training_description"],
            training_date=row["training_date"],
            topic_label=row["topic_label"],
            level_label=row["level_label"],
            updated_at=row["updated_at"],
        )
        for row in cur.fetchall()
    ]


def _get_tasks(cur: RealDictCursor, employee_id: int) -> list[Task]:
    cur.execute(
        """
        SELECT
            ta.title,
            ta.details,
            tac.label AS category_label,
            ta.updated_at
        FROM task_assignments ta
        JOIN task_assignments_assignees taa ON taa.task_assignment_id = ta.id
        LEFT JOIN task_assignments_categories tac ON tac.id = ta.category_id
        WHERE taa.user_id = %(employee_id)s;
        """,
        {"employee_id": employee_id},
    )
    return [
        Task(
            title=row["title"],
            details=row["details"],
            category_label=row["category_label"],
            updated_at=row["updated_at"],
        )
        for row in cur.fetchall()
    ]


def _get_user_skills(cur: RealDictCursor, employee_id: int) -> list[UserSkill]:
    cur.execute(
        """
        SELECT
            s.name  AS skill_name,
            us.level,
            us.updated_at
        FROM user_skills us
        JOIN skills s ON s.id = us.skill_id
        WHERE us.user_id = %(employee_id)s
          AND us.is_selected = true;
        """,
        {"employee_id": employee_id},
    )
    return [
        UserSkill(
            skill_name=row["skill_name"],
            level=row["level"],
            updated_at=row["updated_at"],
        )
        for row in cur.fetchall()
    ]


def get_cv(employee_id: int) -> Cv | None:
    with _connect() as cur:
        return _get_cv(cur, employee_id)


def get_experiences(employee_id: int) -> list[Experience]:
    with _connect() as cur:
        return _get_experiences(cur, employee_id)


def get_employment_histories(employee_id: int) -> list[EmploymentHistory]:
    with _connect() as cur:
        return _get_employment_histories(cur, employee_id)


def get_trainings(employee_id: int) -> list[Training]:
    with _connect() as cur:
        return _get_trainings(cur, employee_id)


def get_tasks(employee_id: int) -> list[Task]:
    with _connect() as cur:
        return _get_tasks(cur, employee_id)


def get_user_skills(employee_id: int) -> list[UserSkill]:
    with _connect() as cur:
        return _get_user_skills(cur, employee_id)


def get_all_employee_ids() -> list[int]:
    with _connect() as cur:
        cur.execute("SELECT id FROM users ORDER BY id;")
        return [row["id"] for row in cur.fetchall()]


def extract_employee(employee_id: int) -> EmployeeData:
    with _connect() as cur:
        return EmployeeData(
            employee_id=employee_id,
            user_detail=_get_user_detail(cur, employee_id),
            cv=_get_cv(cur, employee_id),
            experiences=_get_experiences(cur, employee_id),
            employment_histories=_get_employment_histories(cur, employee_id),
            trainings=_get_trainings(cur, employee_id),
            tasks=_get_tasks(cur, employee_id),
            skills=_get_user_skills(cur, employee_id),
        )

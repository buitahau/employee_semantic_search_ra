from dataclasses import dataclass

from common.db import _connect
from query.types import ExactFilterResult, QueryAnalysis


_SUPPORTED_FILTER_KEYS = {"employee_id", "full_name", "company_email", "gender", "contract_type", "position", "level", "skills"}


def search_exact(analysis: QueryAnalysis) -> ExactFilterResult:
    filters = {k: v for k, v in analysis.filter.items() if k in _SUPPORTED_FILTER_KEYS}
    if not filters:
        return ExactFilterResult(employee_ids=[], matched_count=0)

    conditions: list[str] = []
    params: dict = {}

    if "employee_id" in filters:
        conditions.append("u.id = %(employee_id)s")
        params["employee_id"] = filters["employee_id"]

    if "full_name" in filters:
        conditions.append("LOWER(CONCAT(u.first_name, ' ', u.last_name)) = LOWER(%(full_name)s)")
        params["full_name"] = filters["full_name"]

    if "company_email" in filters:
        conditions.append("LOWER(u.company_email) = LOWER(%(company_email)s)")
        params["company_email"] = filters["company_email"]

    if "gender" in filters:
        conditions.append("LOWER(u.gender) = LOWER(%(gender)s)")
        params["gender"] = filters["gender"]

    if "contract_type" in filters:
        conditions.append(
            "LOWER(REPLACE(u.contract_type::text, '_', '')) = LOWER(REPLACE(%(contract_type)s, ' ', ''))"
        )
        params["contract_type"] = filters["contract_type"]

    if "position" in filters:
        conditions.append("LOWER(p.name) = LOWER(%(position)s)")
        params["position"] = filters["position"]

    if "level" in filters:
        conditions.append("LOWER(ul.label) = LOWER(%(level)s)")
        params["level"] = filters["level"]

    skills_list: list[str] = filters.get("skills", [])
    if skills_list:
        conditions.append(
            "u.id IN ("
            "  SELECT us2.user_id"
            "  FROM user_skills us2"
            "  JOIN skills s2 ON s2.id = us2.skill_id"
            "  WHERE LOWER(s2.name) = ANY(%(skills_lower)s)"
            "    AND us2.is_selected = true"
            "  GROUP BY us2.user_id"
            "  HAVING COUNT(DISTINCT LOWER(s2.name)) = %(skills_count)s"
            ")"
        )
        params["skills_lower"] = [s.lower() for s in skills_list]
        params["skills_count"] = len(skills_list)

    where_clause = "WHERE " + " AND ".join(conditions)

    sql = f"""
        SELECT u.id AS employee_id
        FROM users u
        LEFT JOIN positions   p  ON p.id  = u.position_id
        LEFT JOIN user_levels ul ON ul.id = u.level_id
        {where_clause}
    """

    with _connect() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    employee_ids = [row["employee_id"] for row in rows]
    return ExactFilterResult(employee_ids=employee_ids, matched_count=len(employee_ids))

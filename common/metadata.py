from common.db import _connect


def get_all_skill_names() -> list[str]:
    with _connect() as cur:
        cur.execute("SELECT name FROM skills ORDER BY name")
        return [row["name"] for row in cur.fetchall()]


def detect_skills(text: str | None, skill_names: list[str]) -> list[str]:
    if not text:
        return []
    text_lower = text.lower()
    return [name for name in skill_names if name.lower() in text_lower]

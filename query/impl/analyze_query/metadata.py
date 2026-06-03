from common.metadata import detect_skills, get_all_skill_names


def build_filter(normalized: str) -> dict:
    skill_names = get_all_skill_names()
    matched = detect_skills(normalized, skill_names)
    if matched:
        return {"skills": matched}
    return {}

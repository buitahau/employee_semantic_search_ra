import re

from common.normalize import PUNCT_MAP

_SENTINELS = {"null", "undefined", "none"}


def normalize_query(query: str | None) -> str:
    if query is None:
        raise ValueError("query must not be None")
    text = query.strip()
    if not text or text.lower() in _SENTINELS:
        raise ValueError(f"invalid query: {query!r}")
    text = text.lower()
    text = text.translate(PUNCT_MAP)
    text = re.sub(r"\s+", " ", text).strip()
    return text

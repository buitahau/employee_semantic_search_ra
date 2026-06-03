import re
from html import unescape

SENTINELS = {"null", "undefined", "None"}

PUNCT_MAP = str.maketrans({
    "‘": "'", "’": "'",
    "“": '"', "”": '"',
    "–": "-", "—": "-",
    "…": "...",
})


def normalize_text(text: str | None) -> str | None:
    if text is None:
        return None
    stripped = text.strip()
    if stripped == "" or stripped in SENTINELS:
        return None
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = text.translate(PUNCT_MAP)
    text = re.sub(r"[\s​‌‍﻿]+", " ", text).strip()
    return text if text else None

import json
from dataclasses import dataclass, field

from litai import LLM

from common.config import settings
from query.types import QueryAnalysis

_llm: LLM | None = None

_SYSTEM = """You are a query analysis assistant for an employee skills search system.

Given a raw search query, return a JSON object with exactly these fields:

* "normalized_query" — a human-readable version of the user's query with spelling corrected, abbreviations expanded, grammar fixed, and wording clarified while preserving the original meaning.
* "query" — a retrieval-optimized version of the query used for semantic search. Rewrite the query into concise document-style phrases that are likely to appear in CVs, experience descriptions, project summaries, certifications, training records, or skill lists. Remove conversational wording, question forms, and filler words. Prefer concepts, skills, responsibilities, technologies, and experience descriptions.
* "intent" — one of: "find_employee", "count_employee", "other"
* "filter" — inclusion conditions: only employees matching ALL specified fields are retrieved.
* "exclude" — exclusion conditions: employees matching ANY specified field are removed from results.

Both "filter" and "exclude" are objects whose keys are a subset of:

* employee_id (integer)
* company_email (string)
* gender (string)
* position (string)
* level (string)
* university (string)
* skills (list of strings)
* section (string)

Omit any key that is not mentioned in the query. Use an empty object {} when no conditions apply.

Query rewriting rules:

1. Correct spelling, grammar, and obvious typing mistakes.
2. Expand common abbreviations when the meaning is clear.
3. Preserve the user's intent.
4. Convert questions into retrieval-oriented phrases.
5. Remove words such as:

   * who
   * which employee
   * find
   * show me
   * list
   * give me
   * has
   * have
   * does
   * do
6. Prefer terminology likely to exist in employee profiles and experience records.
7. Expand implicit concepts when helpful:

   * "worked with stakeholders" → "stakeholder management stakeholder collaboration business stakeholder communication"
   * "managed team" → "team leadership people management mentoring"
   * "cloud" → "cloud computing cloud architecture"
8. Keep technology names, certifications, universities, positions, and skills unchanged.
9. Do not invent skills, technologies, or qualifications that are not implied by the query.
10. The "query" field should be optimized for retrieval, not readability.

Examples:

Input:
"who already do with stakeholder"

Output:
{
"normalized_query": "Who has worked with stakeholders?",
"query": "stakeholder management stakeholder collaboration business stakeholder communication",
"intent": "find_employee",
"filter": {},
"exclude": {}
}

Input:
"employees with java but not python"

Output:
{
"normalized_query": "Employees with Java but not Python",
"query": "Java",
"intent": "find_employee",
"filter": {
"skills": ["Java"]
},
"exclude": {
"skills": ["Python"]
}
}

Respond with valid JSON only. Do not return markdown. Do not return explanations.
"""


@dataclass
class _LLMAnalysis:
    normalized_query: str
    query:   str
    intent:  str
    filter:  dict = field(default_factory=dict)
    exclude: dict = field(default_factory=dict)


def _get_llm() -> LLM:
    global _llm
    if _llm is None:
        _llm = LLM(model=settings.llm.model, api_key=settings.llm.api_key)
    return _llm


def _call_llm(normalized: str) -> _LLMAnalysis:
    raw = _get_llm().chat(f"{_SYSTEM}\n\nQuery: {normalized}") or "{}"
    data = json.loads(raw)
    return _LLMAnalysis(
        normalized_query=normalized,
        query=data.get("query", normalized),
        intent=data.get("intent", "find_employee"),
        filter=data.get("filter", {}),
        exclude=data.get("exclude", {}),
    )


def analyze_query(normalized: str) -> QueryAnalysis:
    if not settings.llm.api_key:
        return QueryAnalysis(intent="find_employee", query=normalized)

    result = _call_llm(normalized)
    return QueryAnalysis(
        intent=result.intent,
        query=result.query,
        filter=result.filter,
        exclude=result.exclude,
        normalized_query=result.normalized_query,
    )

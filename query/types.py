from dataclasses import dataclass, field

from common.types import EmployeeData


@dataclass
class QueryRequest:
    query: str


@dataclass
class QueryAnalysis:
    intent:  str
    query:   str
    normalized_query: str
    filter:  dict = field(default_factory=dict)
    exclude: dict = field(default_factory=dict)


@dataclass
class ChunkHit:
    employee_id: int
    field_type:  str
    chunk_text:  str
    metadata:    dict
    score:       float


@dataclass
class ExactFilterResult:
    employee_ids: list[int]
    matched_count: int


@dataclass
class SemanticSearchResult:
    hits: list[ChunkHit]
    matched_count: int

@dataclass
class SearchResult:
    query: str
    total_matches: int
    results: list[EmployeeData]

from dataclasses import dataclass, field


@dataclass
class QueryRequest:
    query: str


@dataclass
class QueryAnalysis:
    intent:    str
    query:     str
    heuristic: str
    filter:    dict = field(default_factory=dict)


@dataclass
class ChunkHit:
    employee_id: int
    field_type:  str
    chunk_text:  str
    metadata:    dict
    score:       float

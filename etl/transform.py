from etl.impl.transform.metadata import enrich_with_metadata
from etl.impl.transform.normalize import normalize
from etl.impl.transform.chunking import chunking
from common.types import EmployeeData


def transform(raw: EmployeeData) -> EmployeeData:
    data = normalize(raw)           # T3.1 — text normalization
    # data = ai_cleanup(data)       # T3.2 — AI cleanup (not yet implemented)
    data = enrich_with_metadata(data)  # T3.3 — metadata extraction
    data = chunking(data)               # T3.4 — chunking
    # data = embed(data)            # T3.5 — embedding (not yet implemented)
    return data

from common.types import EmployeeData
from etl.transforms.metadata import enrich_with_metadata
from etl.transforms.normalize import normalize


def transform(raw: EmployeeData) -> EmployeeData:
    data = normalize(raw)           # T3.1 — text normalization
    # data = ai_cleanup(data)       # T3.2 — AI cleanup (not yet implemented)
    data = enrich_with_metadata(data)  # T3.3 — metadata extraction
    # data = chunk(data)            # T3.4 — chunking (not yet implemented)
    # data = embed(data)            # T3.5 — embedding (not yet implemented)
    return data

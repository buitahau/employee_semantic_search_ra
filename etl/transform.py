from common.states import EtlPipelineState
from common.types import EmployeeData
from etl.impl.transform.chunking import chunking
from etl.impl.transform.metadata import enrich_with_metadata
from etl.impl.transform.normalize import normalize
from etl.impl.transform.state_builder import to_pipeline_state


def transform(raw: EmployeeData) -> EtlPipelineState:
    data = normalize(raw)               # T3.1 — text normalization
    # data = ai_cleanup(data)           # T3.2 — AI cleanup (not yet implemented)
    state = to_pipeline_state(data)     # combine fields → text per entity
    state = enrich_with_metadata(state) # T3.3 — metadata extraction
    state = chunking(state)             # T3.4 + T3.5 — chunking and embedding
    return state

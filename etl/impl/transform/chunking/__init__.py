from common.types import EmployeeData
from etl.impl.transform.chunking.tokenizer import _fill_token_counts
from etl.impl.transform.chunking.splitter import _fill_sentences
from etl.impl.transform.chunking.accumulator import _fill_windows
from etl.impl.transform.chunking.builder import _fill_chunks


def chunking(data: EmployeeData) -> EmployeeData:
    data = _fill_token_counts(data)
    data = _fill_sentences(data)
    data = _fill_windows(data)
    data = _fill_chunks(data)
    return data

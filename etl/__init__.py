from common.types import ChunkRecord, EmployeeData
from etl.extract import extract_employee
from etl.load import load_employee
from etl.transform import transform


def _collect_chunks(data: EmployeeData) -> list[ChunkRecord]:
    chunks: list[ChunkRecord] = []
    if data.cv:
        chunks.extend(data.cv.chunks)
    for exp in data.experiences:
        chunks.extend(exp.chunks)
    for eh in data.employment_histories:
        chunks.extend(eh.chunks)
    for t in data.trainings:
        chunks.extend(t.chunks)
    for task in data.tasks:
        chunks.extend(task.chunks)
    for skill in data.skills:
        chunks.extend(skill.chunks)
    return chunks


def run_employee_pipeline(employee_id: int) -> int:
    raw = extract_employee(employee_id)
    data = transform(raw)
    chunks = _collect_chunks(data)
    load_employee(employee_id, chunks)
    return len(chunks)

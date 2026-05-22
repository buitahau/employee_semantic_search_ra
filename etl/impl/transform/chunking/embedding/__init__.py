from common.types import EmployeeData
from etl.impl.transform.chunking.embedding.encoder import embed


def embed_chunks(data: EmployeeData) -> EmployeeData:
    if data.cv is not None:
        for chunk in data.cv.chunks:
            chunk.embedding = embed(chunk.chunk_text)

    for entity_list in (
        data.experiences,
        data.employment_histories,
        data.trainings,
        data.tasks,
        data.skills,
    ):
        for entity in entity_list:
            for chunk in entity.chunks:
                chunk.embedding = embed(chunk.chunk_text)

    return data

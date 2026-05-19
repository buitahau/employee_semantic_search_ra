-- Verify pgvector is available
SELECT '[1,2,3]'::vector(3);

CREATE TABLE IF NOT EXISTS skills_search_index (
    id               BIGSERIAL PRIMARY KEY,
    employee_id      INTEGER       NOT NULL,
    chunk_index      INTEGER       NOT NULL,
    field_type       TEXT          NOT NULL,  -- 'cv', 'training_log', 'task'
    chunk_text       TEXT          NOT NULL,
    embedding        VECTOR(384)   NOT NULL,
    metadata         JSONB         NOT NULL DEFAULT '{}',
    indexed_at       TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_skills_search_index_employee_chunk
        UNIQUE (employee_id, field_type, chunk_index)
);

-- GIN index for fast JSONB filtering (skills, source_type, date ranges, etc.)
CREATE INDEX IF NOT EXISTS idx_skills_search_index_metadata
    ON skills_search_index USING GIN (metadata);

-- HNSW index for ANN vector search (pgvector >= 0.5.0)
CREATE INDEX IF NOT EXISTS idx_skills_search_index_embedding
    ON skills_search_index USING hnsw (embedding vector_cosine_ops);

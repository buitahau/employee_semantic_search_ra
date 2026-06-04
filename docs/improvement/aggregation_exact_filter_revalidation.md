## Aggregation with Exact Filter Revalidation

**Status:** Open

Currently, the input for the aggregation step comes only from the semantic search results returned by pgvector.

### Why this matters

Relying solely on semantic results can miss relevant candidates that match the user's explicit filters (e.g., exact skill names, location, seniority) but scored slightly lower in the vector search. This reduces precision and can exclude strong matches [web:1][web:3].

### Approach

1. **Execute exact filters from the semantic search query**  
   - Parse the user's original query and the filters extracted during semantic search (skills, location, role, etc.).  
   - Run a separate SQL/pgvector query that applies these filters exactly, without relying on vector similarity scoring.

2. **Run three parallel retrieval pipelines**  
   - **Set A**: Semantic results from pgvector (vector similarity–based).  
   - **Set B**: Exact-filter results from the structured query (deterministic match).  
   - **Set C**: BM25 keyword search results (term-frequency–based relevance score).

3. **Incorporate BM25 score into aggregation**  
   - Execute a BM25 search over the same candidate corpus (e.g., using PostgreSQL full-text search with `tsvector`/`tsquery` or an external engine like Elasticsearch).  
   - Retrieve a BM25 relevance score `s_bm25` for each candidate in Set C.  
   - Normalize `s_bm25` to the same scale as the vector similarity score (e.g., 0–1) using min-max scaling or sigmoid normalization.

4. **Merge and prioritize exact matches**  
   - Merge Sets A, B, and C, deduplicate by candidate ID.  
   - **Prioritize Set B (exact-filter results)**:
     - Assign a higher base score to candidates from Set B.  
     - Within Set B, rank by exact-match quality (e.g., number of required skills matched, exact role match).  
   - For candidates in A and/or C, combine vector and BM25 scores.

### Benefit
By incorporating BM25 keyword scores into the aggregation step, prioritizing exact-filter results, and using a well-defined metadata schema, the final ranking is:
- More faithful to the user's explicit constraints (thanks to exact matches + mandatory fields).
- More robust to spelling variations and keyword mismatches (BM25 captures exact term matches that embeddings may miss).
- More nuanced and accurate when optional metadata is used for reranking.
- More robust and scalable, as the schema enforces consistency across all candidates [web:1][web:3].

This hybrid approach leverages:
- **Vector similarity** for semantic understanding.
- **BM25** for precise keyword matching (e.g., exact skill names, certifications).
- **Exact filters** for deterministic constraint satisfaction.
# Checklist

## Core Features

- [x] Complete the basic semantic search flow (ETL and search).

## Indexing Quality

- [ ] Add contextual data to chunk headers (document type, candidate name/ID, section, role, skills, etc.) to make each chunk self-contained and improve embedding and reranking quality.

- [] Review and provide a detailed mapping table showing exactly which fields from each source table will be ingested into pgvector.

## Result Generation

- [ ] Define structure and generate the client response based on the intent.

## Search Quality Validation

Goal: verify that the search pipeline returns relevant, correctly ranked results across realistic employee data.

- [ ] Prepare seed data that is more complex and realistic, with additional test cases and data variations.
- [ ] Create a list of prompts and their expected results based on the seed data.
- [ ] Implement the tests, collect the actual results, and generate a comparison report against the expected results.

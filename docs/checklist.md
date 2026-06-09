# Checklist

## Core Features

- [x] Complete the basic semantic search flow (ETL and search).

## Indexing Quality

- [ ] [Prepend contextual headers to content before chunking](implementation_plan/tasks/Contextual-headers.md) (document type, candidate name/ID, section, role, skills, etc.) so every resulting chunk is self-contained and improves embedding and reranking quality.

- [ ] [Review and provide a detailed mapping table showing exactly which fields from each source table will be ingested into pgvector.](implementation_plan/tasks/Field-mapping-table.md)

## Result Generation

- [ ] [Define structure and generate the client response based on the intent.](implementation_plan/tasks/Client-respond.md)

## Search Quality Validation

Goal: verify that the search pipeline returns relevant, correctly ranked results across realistic employee data.

- [ ] [Prepare seed data that is more complex and realistic, with additional test cases and data variations.](implementation_plan/tasks/SQV1-seed-data.md)
- [ ] [Create a list of prompts and their expected results based on the seed data.](implementation_plan/tasks/SQV2-test-prompts.md)
- [ ] [Implement the tests, collect the actual results, and generate a comparison report against the expected results.](implementation_plan/tasks/SQV3-search-report.md)

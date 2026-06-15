# Checklist

## Core Features

- ✅ Complete the basic semantic search flow (ETL and search). 

## Indexing Quality

- 🛠️ [IQ1](implementation_plan/tasks/IQ1-Contextual-headers.md) - Prepend contextual headers to content before chunking (document type, candidate name/ID, section, role, skills, etc.) so every resulting chunk is self-contained and improves embedding and reranking quality.

- 🛠️ [IQ2](implementation_plan/tasks/IQ2-Field-mapping-table.md) - Review and provide a detailed mapping table showing exactly which fields from each source table will be ingested into pgvector.

- ✅ [IQ3](implementation_plan/tasks/IQ3-Metadata-structure.md) - Define the canonical metadata structure for each section type stored in pgvector (e.g., experience, skills, education), specifying required/optional fields and types to enable consistent filtering and contextual header generation.

## Result Generation

- ❌ ~~[RG1](implementation_plan/tasks/RG1-Client-respond.md) - Define structure and generate the client response based on the intent.~~

## Improvement

### Query Preprocessing

[Refer](implementation_plan/improvement/ai_powered_query_preprocessing.md)

- ✅ [QP1](implementation_plan/tasks/QP1-AI-query-preprocessing.md) - AI-powered query preprocessing: rewrite noisy input and detect others data before embedding

### Aggregation with Exact Filter Revalidation

[Refer](implementation_plan/improvement/aggregation_exact_filter_revalidation.md)

- ⏳ [AGG1](implementation_plan/tasks/AGG1-BM25-search.md) - Implement BM25 search
- ⏳ [AGG2](implementation_plan/tasks/AGG2-Aggregate-BM25-and-semantic.md) - Aggregate BM25 results and Semantic results from pgvector
- 🛠️ [AGG3](implementation_plan/tasks/AGG3-Exact-filter.md) - Implement exact filter
- ⏳ [AGG4](implementation_plan/tasks/AGG4-Aggregate-Exact-filter-and-semantic.md) - Aggregate exact-match retrieval results and semantic results

## Negation and Complex Condition Handling

[Refer](implementation_plan/improvement/negation_and_complex_condition_handling.md)

- 🔍 [NCC1](implementation_plan/tasks/NCC1-Negation-handling.md) - Handle negation in the exact filter (NOT, exclusion)
- 🔍 [NCC2](implementation_plan/tasks/NCC2-Complex-condition-handling.md) - Handle complex conditions in the exact filter (OR, AND/OR grouping)

## Search Quality Validation

Goal: verify that the search pipeline returns relevant, correctly ranked results across realistic employee data.

- 🛠️ [SQV1](implementation_plan/tasks/SQV1-seed-data.md) - Prepare seed data that is more complex and realistic, with additional test cases and data variations.
- 🛠️ [SQV2](implementation_plan/tasks/SQV2-test-prompts.md) - Create a list of prompts and their expected results based on the seed data.
- 🛠️ [SQV3](implementation_plan/tasks/SQV3-search-report.md) - Implement the tests, collect the actual results, and generate a comparison report against the expected results.

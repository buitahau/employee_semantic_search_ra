## AI-Powered Query Preprocessing

**Status:** Open

Before passing the user's search prompt to the embedding/retrieval pipeline, route it through an AI model to improve query quality. 

### Why this matters

Raw user input is noisy. A misspelled skill name or an ambiguous phrase ("someone who knows cloud") produces a poor embedding, which hurts recall. A preprocessing step normalizes the query before it ever reaches pgvector, improving result quality without changing the retrieval architecture.

### What the AI should do

- **Correct mistakes** — fix typos, grammatical errors, and ambiguous phrasing so the embedding model receives clean input.
- **Detect intent** — classify the prompt into one of: `find_employee`, `count_employee`, or other relevant query types.
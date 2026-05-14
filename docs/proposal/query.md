# Query — Detail Specification

The query layer handles incoming search requests from the admin. It accepts a natural language query and/or structured filter parameters, converts the query text into a vector embedding, and retrieves ranked employee matches from the database. Structured filters narrow the candidate pool via SQL before vector similarity scoring is applied, ensuring results are both semantically relevant and structurally correct.

---

## Description


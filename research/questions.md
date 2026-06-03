# RAG Research Questions

A running list of questions to investigate one by one.

---

## Q1: Which embedding model and embedding dimension are most suitable for each domain?

- [ ] Research pending

---

## Q2: How can we improve completeness accuracy?

- [ ] Research pending

---

## Q3: What is faithfulness? How can we ensure it, and which techniques are most effective for achieving it?

- [ ] Research pending

---

## Q4: How should a RAG system handle negation and exclusion queries?

Examples:
- "Show documents that do NOT mention Kubernetes."
- "What features are unsupported?"
- "Which customers have never used feature X?"
- "Summarize the policy except for security requirements."

Research topics:
- Why vector search struggles with negation
- Query rewriting approaches
- Hybrid retrieval (keyword + vector)
- Metadata filtering
- Reranking for negation awareness
- LLM-based query understanding
- Evaluation benchmarks for negation handling

- [ ] Research pending

---

## Q5: What indexing strategies are available, and when should each be used in a RAG system?

Examples:
- HNSW
- IVF
- IVF-PQ
- IVF-SQ
- Flat (Brute Force)
- DiskANN
- ScaNN
- Graph-based indexes
- Hybrid sparse + dense indexes

Research topics:
- Accuracy vs latency tradeoffs
- Memory consumption
- Scalability to billions of vectors
- Update frequency considerations
- Filtering support
- Distributed deployment
- Impact on retrieval quality

Apply findings to this project:
- Dataset size
- Expected query volume
- Update frequency
- Latency requirements
- Infrastructure constraints

- [ ] Research pending
# RAG Aspects and Fields

## Core RAG Aspects (Evaluation Dimensions)

| Aspect | What It Measures | Why It Matters |
|--------|-----------------|----------------|
| Completeness | Does the answer cover all relevant info from retrieved context? | Prevents partial answers even when factually correct |
| Faithfulness | Is the answer derived only from retrieved context (no hallucinations)? | Ensures factual grounding and avoids LLM fabrication |
| Relevance | Are retrieved documents actually relevant to the query? | Poor retrieval → poor generation quality |
| Context Adherence | Is output consistent with the provided context? | Measures precision of information extraction |
| Answer Correctness | Is the answer factually accurate (ground truth match)? | Traditional accuracy metric |
| Recall | What % of relevant information was retrieved? | Directly ties to completeness |
| Precision | What % of retrieved info is actually relevant? | Affects context window efficiency |

---

## Technical Architecture Aspects

| Aspect | Key Components |
|--------|---------------|
| Retrieval Mechanisms | Dense retrieval (embeddings), sparse retrieval (BM25), hybrid search, multi-vector retrieval |
| Indexing Strategies | Chunking (fixed, semantic, recursive), advanced indexing (parent-child, small-to-big), graph-based indexing |
| Context Management | Token optimization, context window balancing, multi-stage retrieval, adaptive context breadth |
| Reranking | Cross-encoder rerankers, re-ranking retrieved results before generation |
| Query Processing | Query rewriting, query expansion, multi-hop query decomposition, HyDE (hypothetical document) |

---

## Advanced RAG Variants (Fields)

| RAG Type | Distinguishing Feature |
|----------|----------------------|
| Naive RAG | Basic retrieve → generate pipeline |
| Advanced RAG | Adds preprocessing, retrieval optimization, post-processing |
| Modular RAG | Modular components (iterative retrieval, routing, memory) |
| Multi-hop RAG | Iterative retrieval for complex queries requiring multiple documents |
| Graph RAG | Uses knowledge graphs for structured retrieval and reasoning |
| Self-RAG | Model self-critiques retrieval need and quality |
| Corrective RAG (CRAG) | Self-corrects retrieval errors using web search |
| Fusion RAG | Combines dense + sparse retrieval (hybrid search) |
| Agentic RAG | LLM agent plans and executes retrieval steps dynamically |
| Multi-modal RAG | Retrieves from images, audio, video, not just text |
| Long-context RAG | Leverages million-token windows for broader coverage |

---

## Application Domains (Fields)

| Domain | Use Cases |
|--------|----------|
| Question Answering | Knowledge-intensive QA, specialized chatbots |
| Content Generation | Summarization, content creation, market analysis |
| Conversational AI | Chatbots, virtual assistants, customer support |
| Research & Knowledge Engines | Academic research, internal knowledge bases |
| Domain-Specific RAG | Healthcare, legal, finance, technical documentation |

---

## Challenges & Research Fields

| Challenge Area | Key Issues |
|---------------|-----------|
| Scalability | Large corpora, high query volume, latency |
| Bias & Ethics | Retrieval bias, hallucination, ethical deployment concerns |
| Robustness | Handling conflicting evidence, noisy data, adversarial queries |
| Evaluation | Measuring completeness, semantic test coverage, recall in production |
| Data Quality | Unstructured data, inconsistent terminology, multi-format documents |
| Cost Optimization | Token costs, context window trade-offs, efficiency vs. comprehensiveness |

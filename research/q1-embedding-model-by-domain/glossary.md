# Glossary — Key Terms

**Research Question**: Which embedding model and dimension are most suitable for each domain?

**Date**: 2026-06-09

---

## Total Parameters

The total count of numeric values stored in the model file.

AI models do not understand words — they represent meaning as numbers. Total Parameters is how many of those numbers exist in the model. More parameters means a larger file, which requires proportionally more RAM (or VRAM) to load. If the machine has less memory than the file size, the process crashes immediately at startup.

> **Analogy**: The thickness of an encyclopedia. A thicker book holds more knowledge but needs a bigger shelf and more time to open.

**Hardware implication**: Total Parameters is a one-time cost paid at model load time — not per query.

---

## Active Parameters

The number of parameters that actually participate in computation for a single inference call (one search query).

- **Dense models** (traditional): every parameter runs on every query. Active = Total.
- **MoE models** (Mixture of Experts, modern): the model is split into specialized sub-networks called "experts." For any given input, only the relevant experts are activated. Active << Total.

Active Parameters is what drives per-query latency and memory cost. Total Parameters drives file size and startup cost.

> **Analogy**: Total Parameters is how many pages are in the book. Active Parameters is how many pages you actually flip open to answer one question.

---

## Embedding Dimension

The length of the vector (array of numbers) produced by the model for a given input text.

Higher dimension allows the vector to encode finer-grained semantic detail — nuance, synonyms, metaphor, implicit context. Lower dimension means faster similarity search and smaller storage.

**Common ranges:**

| Range | Typical models | Characteristics |
|-------|---------------|-----------------|
| 384 | all-MiniLM-L6-v2, multilingual-e5-small | Very lightweight, fast search, best for short text |
| 768–1024 | bge-base, gte-large, multilingual-e5-base/large | Industry sweet spot — balances accuracy and cost for most enterprise projects |
| 3072+ | text-embedding-3-large, e5-mistral-7b-instruct | High accuracy, but high storage and compute cost |

**Impact on vector database**: Storing millions of documents at higher dimension means proportionally more disk space and RAM. Each similarity search (cosine distance) runs over longer arrays, increasing query latency.

---

## Max Tokens

The maximum input length (in tokens) the model can process in a single call.

Text longer than Max Tokens is silently truncated — the tail is dropped without warning. To avoid data loss, long documents must be split into shorter pieces before embedding. This process is called **chunking**.

**Why long inputs are expensive — self-attention complexity**

Inside a transformer, every token must compare itself against every other token to build context. For an input of N tokens, this creates an N×N comparison matrix:

- 500 tokens → 500 × 500 = 250,000 comparisons
- 1,000 tokens → 1,000 × 1,000 = 1,000,000 comparisons

Complexity is **O(n²)** — doubling the sequence length quadruples the compute cost. This is why larger Max Tokens models consume significantly more compute per call, even if the model itself has fewer parameters.

> Reference: [Attention Mechanism Complexity Analysis](https://medium.com/@mridulrao674385/attention-mechanism-complexity-analysis-7314063459b1)

**Chunking trade-offs:**

| Max Tokens size | Effect |
|----------------|--------|
| Small (256–512) | Many small chunks → slower indexing, more rows in vector database, risk of context loss at boundaries |
| Large (8192+) | Fewer chunks → context preserved per chunk, but each embedding call is more compute-intensive |

**Context loss example** — a document split mid-thought:

- Chunk 1: *"Company A signed a $10M contract."*
- Chunk 2: *"They will deploy the project in Vietnam next month."*

Query: *"Where is Company A's project?"*

Chunk 1's vector contains "Company A" but no location. Chunk 2's vector contains "Vietnam" but "They" has no referent — the model cannot resolve it. The similarity search fails because the relevant information was split across two vectors.

**Indexing cost when chunking:**

When one document is split into N chunks, the embedding model must be called N times. If one call takes 10ms, 10 chunks takes ~100ms. The vector database also stores N rows instead of one, increasing both storage size and the number of rows the similarity search must scan.

---

## Mean (Task)

The model's average score across all individual tasks in the MTEB benchmark, computed as a simple arithmetic mean.

Only computed when the model has run on **all** tasks in the benchmark. If any task result is missing, the score is null.

> Source: [`mteb/leaderboard/text_segments.py`](https://github.com/embeddings-benchmark/mteb/blob/9e29c442/mteb/leaderboard/text_segments.py#L4-L5) — [`_get_model_score`](https://github.com/embeddings-benchmark/mteb/blob/9e29c442/mteb/benchmarks/benchmark.py#L336-L349)

---

## Mean (TaskType)

The model's average score weighted by task type rather than by individual task count.

Computed by first averaging scores within each task type (Retrieval, STS, Clustering, etc.), then averaging those per-type results. This prevents task types that contain more tasks from dominating the overall score.

**Difference from Mean (Task):**

Suppose the benchmark has 30 Retrieval tasks and 5 STS tasks. A model that is excellent at Retrieval and poor at STS will score high on Mean (Task) simply due to task count. Mean (TaskType) gives equal weight to each task type regardless of how many tasks it contains, providing a more balanced view of the model's capabilities.

---

## Retrieval

A MTEB task type where the model retrieves the most relevant documents from a corpus given a query.

**Data structure**: a corpus of documents, a set of queries, and relevance annotations mapping each query to its relevant documents.

**Primary metric**: `ndcg@10` — Normalized Discounted Cumulative Gain at rank 10. Rewards models that rank the most relevant documents near the top of the result list. Range: 0–1 (reported as 0–100 in MTEB).

**Score aggregation**: simple average of `ndcg@10` scores across all Retrieval tasks the model has been evaluated on.

**Example tasks**: ArguAna, NQ, SCIDOCS, StackOverflowQA.

Retrieval score is the most direct proxy for real-world semantic search performance.

---

## STS (Semantic Textual Similarity)

A MTEB task type where the model assigns a similarity score to pairs of sentences, reflecting how close they are in meaning.

**Data structure**: sentence pairs, each with a human-annotated similarity score (typically 0–5).

**Primary metric**: `cosine_spearman` — Spearman rank correlation between the model's cosine similarity scores and the human annotations. Range: −1 to 1 (higher is better; reported as 0–100 after scaling in MTEB).

**Score aggregation**: simple average of `cosine_spearman` scores across all STS tasks the model has been evaluated on.

**Example tasks**: STS12, STS13, STS14, STS15, STSBenchmark, SICK-R.

STS is a direct measure of how faithfully the model's embedding space encodes meaning. A low STS score means the model cannot reliably distinguish similar from dissimilar text — which degrades retrieval, clustering, and all other downstream tasks.

---

## Hugging Face Filter Options

All filter options available on Hugging Face Model Hub when searching for embedding models. See [references.md](./references.md) for which filters were selected and why.

---

### Tasks (Pipeline)

Pipeline is the label that classifies a model by the task it performs.

**Multimodal**

| Task | Description |
|------|-------------|
| Multimodal | Handles multiple input types simultaneously (text, image, audio) |

**Computer Vision**

| Task | Description |
|------|-------------|
| Image Classification | Classifies what an image contains (cat, dog, car...) |
| Object Detection | Detects multiple objects in an image and draws bounding boxes |
| Image Segmentation | Segments an image by pixel region (e.g., separating a person from the background) |
| Depth Estimation | Estimates which objects are near or far in a 2D image |
| Image-to-Image | Transforms an image (super-resolution, denoising, style transfer...) |
| Keypoint Detection | Identifies key body landmarks (hands, knees, head...) |
| Zero-Shot Image Classification | Classifies images without task-specific training |

**Natural Language Processing (NLP)**

| Task | Description |
|------|-------------|
| Feature Extraction | Generates embeddings/vectors for semantic search and RAG |
| Sentence Similarity | Measures semantic equivalence between sentence pairs; uses the same encoder architecture as Feature Extraction |
| Text Generation | Generates text (chatbots, LLMs) |
| Text Classification | Classifies text into categories (spam, sentiment, topic...) |
| Token Classification | Labels individual tokens (NER: person names, organizations...) |
| Question Answering | Answers questions given a context passage |
| Summarization | Condenses text into a shorter form |
| Translation | Translates between languages |
| Fill-Mask | Predicts missing words in a sentence |
| Zero-Shot Classification | Classifies text without task-specific training |
| Conversational | Dialogue and chat |
| Table Question Answering | Answers questions over tabular data |
| Text Ranking | Ranks documents by relevance to a query |
| Document Question Answering | Answers questions over PDFs and documents |
| Grammar Correction | Corrects grammatical errors in text |
| Sentiment Analysis | Classifies sentiment (positive / negative / neutral) |

**Audio**

| Task | Description |
|------|-------------|
| Audio | Speech recognition, audio classification, and related audio tasks |

---

### Libraries

The framework or library used to run the model.

| Library | Description |
|---------|-------------|
| sentence-transformers | Embedding, semantic search, RAG — unified API for all embedding models |
| transformers | Hugging Face's primary library for NLP and LLMs |
| pytorch | Deep learning framework |
| tensorflow | Deep learning framework |
| jax | Google's deep learning framework |
| peft | LoRA, QLoRA — parameter-efficient fine-tuning |
| diffusers | Image generation (Stable Diffusion, Flux...) |
| timm | Computer vision models |
| spacy | Traditional NLP, NER |
| onnx | Inference optimization |
| gguf | Local inference via Ollama, llama.cpp |
| vllm | High-throughput LLM serving |
| keras | High-level API for TensorFlow |

---

### Other (Misc Tags)

Tags describing additional model properties or capabilities.

| Tag | Description |
|-----|-------------|
| eval-results | Model has publicly attached benchmark results in the standard MTEB format |
| eval-results (legacy) | Benchmark results in the old format; not compatible with current MTEB |
| inference-endpoints | Model can be deployed directly via Hugging Face's hosted inference service |
| text-generation-inference (TGI) | Compatible with Hugging Face's TGI server — designed for high-throughput LLM serving |
| text-embeddings-inference (TEI) | Compatible with Hugging Face's TEI server — designed for embedding model serving |
| 4-bit precision | Model has been quantized to 4-bit, reducing RAM/VRAM requirements |
| 8-bit precision | Model has been quantized to 8-bit |
| custom_code | Running the model requires trusting and loading the author's custom code |
| merge | Model was created by merging multiple models |
| mixture-of-experts | MoE architecture — only a subset of parameters is activated per inference call |
| carbon-emissions | Model card includes CO₂ emissions data from training |

---

**Last Updated**: 2026-06-10

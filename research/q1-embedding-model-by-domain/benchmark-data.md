# Benchmark Data — Embedding Models

**Date**: 2026-06-10
**Source**: [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
**Models**: 15

Weight allocation and normalization formulas are defined in [references.md](./references.md).

---

## Use Cases

Three scoring scenarios, each reflecting a different deployment priority. Choose based on your infrastructure constraints and accuracy requirements.

---

### Quality First

**File**: [benchmark-data-quality.md](./benchmark-data-quality.md)

**Search Quality 80% / Operational Cost 20%**

Prioritizes domain-specific retrieval accuracy. Choose when infrastructure is not the bottleneck and accuracy is the primary KPI. Tolerates larger, slower models.

---

### Cost First

**File**: [benchmark-data-cost.md](./benchmark-data-cost.md)

**Search Quality 45% / Operational Cost 55%**

Prioritizes deployability in constrained CPU-only environments with limited RAM and high query volume. Maintains a minimum quality floor — a semantically meaningless model is never selected. Choose when latency or memory is a hard constraint.

---

### Balanced

**File**: [benchmark-data-balanced.md](./benchmark-data-balanced.md)

**Search Quality 55% / Operational Cost 45%**

A deliberate 55/45 split adjusted for CPU-only ONNX deployment, where operational cost is a real constraint. Suitable as a default when neither accuracy nor compute has a hard requirement.

---

**Last Updated**: 2026-06-10

from pathlib import Path

import numpy as np
from tokenizers import Tokenizer

from common.config import settings
from etl.impl.transform.chunking.embedding.model import _get_session

_tokenizer: Tokenizer | None = None


def _get_enc_tokenizer() -> Tokenizer:
    # Separate singleton from chunking's _get_tokenizer(): chunking configures
    # no_truncation(), but inference requires truncation at 512 (BERT limit).
    global _tokenizer
    if _tokenizer is None:
        model_dir = Path(settings.embedding_model_path).parent
        _tokenizer = Tokenizer.from_file(str(model_dir / "tokenizer.json"))
        _tokenizer.enable_truncation(max_length=512)
        _tokenizer.no_padding()
    return _tokenizer


def _tokenize(text: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    encoding = _get_enc_tokenizer().encode(text)
    ids = np.array(encoding.ids, dtype=np.int64).reshape(1, -1)
    seq_len = ids.shape[1]
    attention_mask = np.ones((1, seq_len), dtype=np.int64)
    token_type_ids = np.zeros((1, seq_len), dtype=np.int64)
    return ids, attention_mask, token_type_ids


def _mean_pool(token_embeddings: np.ndarray, attention_mask: np.ndarray) -> np.ndarray:
    mask = attention_mask[:, :, np.newaxis]               # (1, seq_len, 1)
    masked_sum = (token_embeddings * mask).sum(axis=1)    # (1, 384)
    token_count = max(attention_mask.sum(), 1)
    return masked_sum / token_count                        # (1, 384)


def _l2_normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0.0:
        return vector
    return vector / norm


def embed(text: str) -> list[float]:
    input_ids, attention_mask, token_type_ids = _tokenize(text)
    outputs = _get_session().run(
        ["last_hidden_state"],
        {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids,
        },
    )
    token_embeddings = outputs[0]                         # (1, seq_len, 384)
    pooled = _mean_pool(token_embeddings, attention_mask) # (1, 384)
    normalized = _l2_normalize(pooled)                    # (1, 384)
    return normalized[0].tolist()

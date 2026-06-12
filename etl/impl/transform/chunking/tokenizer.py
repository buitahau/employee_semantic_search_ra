from pathlib import Path

from tokenizers import Tokenizer

from common.config import settings
from common.states import EtlPipelineState

_tokenizer: Tokenizer | None = None

_STATE_ATTRS = ("user_detail", "cv", "experiences", "employment_histories", "trainings", "task", "skills")


def _get_tokenizer() -> Tokenizer:
    global _tokenizer
    if _tokenizer is None:
        model_dir = Path(settings.embedding_model_path).parent
        _tokenizer = Tokenizer.from_file(str(model_dir / "tokenizer.json"))
        _tokenizer.no_padding()
        _tokenizer.no_truncation()
    return _tokenizer


def _count_tokens(text: str) -> int:
    return len(_get_tokenizer().encode(text).ids)


def _fill_token_counts(state: EtlPipelineState) -> EtlPipelineState:
    for attr in _STATE_ATTRS:
        entity = getattr(state, attr)
        if entity:
            entity.pipeline_state["token_count"] = _count_tokens(entity.text) if entity.text else 0
    return state

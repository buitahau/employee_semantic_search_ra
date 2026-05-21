from pathlib import Path
from tokenizers import Tokenizer
from common.config import settings

_tokenizer: Tokenizer | None = None


def _get_tokenizer() -> Tokenizer:
    global _tokenizer
    if _tokenizer is None:
        model_dir = Path(settings.embedding_model_path).parent
        _tokenizer = Tokenizer.from_file(str(model_dir / "tokenizer.json"))
    return _tokenizer


def _count_tokens(text: str) -> int:
    return len(_get_tokenizer().encode(text).ids)

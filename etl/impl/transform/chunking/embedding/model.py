import onnxruntime as ort

from common.config import settings

_session: ort.InferenceSession | None = None


def _get_session() -> ort.InferenceSession:
    global _session
    if _session is None:
        _session = ort.InferenceSession(
            settings.embedding_model_path,
            providers=["CPUExecutionProvider"],
        )
    return _session

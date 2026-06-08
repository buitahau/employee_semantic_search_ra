"""Download multilingual-e5-small ONNX model and tokenizer files into models/<model_name>/."""
import shutil
import sys
from pathlib import Path

REPO = "intfloat/multilingual-e5-small"
MODEL_NAME = "multilingual-e5-small"
DEST = Path(__file__).parent.parent / "models" / MODEL_NAME

FILES = [
    "tokenizer.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
    # Note: E5 models don't have separate vocab.txt (vocab is embedded in tokenizer.json)
]
ONNX_FILE = "onnx/model.onnx"
ONNX_DEST_NAME = f"{MODEL_NAME}.onnx"


def main() -> None:
    """Download multilingual-e5-small ONNX model and tokenizer files from HuggingFace Hub."""
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("huggingface_hub not found — installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub"])
        from huggingface_hub import hf_hub_download

    DEST.mkdir(parents=True, exist_ok=True)

    for filename in FILES:
        print(f"Downloading {filename}...")
        src = hf_hub_download(repo_id=REPO, filename=filename)
        shutil.copy(src, DEST / filename)

    print(f"Downloading {ONNX_FILE}...")
    src = hf_hub_download(repo_id=REPO, filename=ONNX_FILE)
    shutil.copy(src, DEST / ONNX_DEST_NAME)

    print(f"\nDone. Files in models/{MODEL_NAME}/:")
    for f in sorted(DEST.iterdir()):
        print(f"  {f.name}  ({f.stat().st_size / 1024 / 1024:.1f} MB)")

    print(f"\nSet in .env:")
    print(f"  EMBEDDING_MODEL_PATH=models/{MODEL_NAME}/{ONNX_DEST_NAME}")


if __name__ == "__main__":
    main()

"""
Caché Couture — ComfyUI model downloader (Path B / ratified 2026-05-19).

The active stack is Qwen Image + WAN 2.2; those weights are already installed.
This script fetches only the genuine gaps:
  - 4x-UltraSharp (photoreal upscaler)
  - LTX-Video 2B (fast-draft video tier)
  - MMAudio (foley / atmosphere on video clips)

SUPIR is installed separately via `scripts/install_supir.py` because it needs
a custom-node clone plus multiple weight files.

Run from project root:
    python scripts/download_models.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    sys.exit("huggingface_hub not installed. Run: pip install --user huggingface_hub")

COMFYUI_PATH = Path(r"C:\Users\Yoshii\Documents\ComfyUI")

# (repo_id, filename, subfolder under ComfyUI/models/, friendly label)
MODELS: list[tuple[str, str, str, str]] = [
    # Photoreal upscaler — replaces anime-tuned 4x-AnimeSharp for stills final pass.
    ("Kim2091/UltraSharp", "4x-UltraSharp.pth", "upscale_models",
     "4x-UltraSharp (photoreal upscaler)"),

    # LTX-Video 2B 0.9.8 distilled fp8 — fast-draft video tier.
    ("Lightricks/LTX-Video", "ltxv-2b-0.9.8-distilled-fp8.safetensors", "checkpoints",
     "LTX-Video 2B 0.9.8 distilled fp8"),

    # T5-XXL fp8 text encoder — required by LTX-Video (UMT5 for WAN won't substitute).
    ("comfyanonymous/flux_text_encoders", "t5xxl_fp8_e4m3fn.safetensors", "text_encoders",
     "t5xxl_fp8_e4m3fn (LTX text encoder)"),
]

# MMAudio and SUPIR are managed via dedicated node installers, not this script:
#   - SUPIR  -> scripts/install_supir.py
#   - MMAudio -> scripts/install_mmaudio.py


def download_one(repo_id: str, filename: str, subfolder: str, label: str) -> None:
    dest_dir = COMFYUI_PATH / "models" / subfolder
    dest_dir.mkdir(parents=True, exist_ok=True)

    # huggingface_hub preserves nested paths from `filename` inside dest_dir.
    target = dest_dir / Path(filename).name
    nested_target = dest_dir / filename
    if target.exists() or nested_target.exists():
        size_mb = (target if target.exists() else nested_target).stat().st_size / 1e6
        print(f"  [skip] {label} — already present ({size_mb:,.0f} MB)")
        return

    print(f"  [pull] {label}")
    print(f"         repo={repo_id} file={filename}")
    try:
        path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=str(dest_dir),
        )
        size_mb = os.path.getsize(path) / 1e6
        print(f"  [ ok ] {label} — {size_mb:,.0f} MB -> {path}")
    except Exception as e:
        print(f"  [fail] {label}: {e}")


def main() -> int:
    if not COMFYUI_PATH.exists():
        sys.exit(f"ComfyUI path not found: {COMFYUI_PATH}")

    print(f"Caché Couture model downloader")
    print(f"  target: {COMFYUI_PATH / 'models'}")
    print(f"  items : {len(MODELS)}")
    print()

    for entry in MODELS:
        download_one(*entry)

    print()
    print("Done. Run `python scripts/install_supir.py` next to add SUPIR.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

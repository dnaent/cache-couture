"""
Caché Couture — MMAudio installer.

Adds the Kijai/ComfyUI-MMAudio custom node and its fp16 weights:
  - mmaudio_large_44k_v2_fp16.safetensors        (2.06 GB)
  - apple_DFN5B-CLIP-ViT-H-14-384_fp16.safetensors (1.97 GB)
  - mmaudio_synchformer_fp16.safetensors          (475 MB)
  - mmaudio_vae_44k_fp16.safetensors              (611 MB)

bigvgan_v2 is auto-downloaded by the node on first 44k inference.

Run after ComfyUI is closed (or accept that the node will only register on restart).

Usage:
    python scripts/install_mmaudio.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    sys.exit("huggingface_hub not installed. Run: pip install --user huggingface_hub")

COMFYUI_PATH = Path(r"C:\Users\Yoshii\Documents\ComfyUI")
NODE_REPO = "https://github.com/kijai/ComfyUI-MMAudio"
NODE_DIR_NAME = "ComfyUI-MMAudio"

WEIGHTS = [
    ("Kijai/MMAudio_safetensors", "mmaudio_large_44k_v2_fp16.safetensors", "mmaudio",
     "MMAudio large 44k v2 fp16"),
    ("Kijai/MMAudio_safetensors", "apple_DFN5B-CLIP-ViT-H-14-384_fp16.safetensors", "mmaudio",
     "Apple DFN5B CLIP ViT-H/14 fp16"),
    ("Kijai/MMAudio_safetensors", "mmaudio_synchformer_fp16.safetensors", "mmaudio",
     "MMAudio synchformer fp16"),
    ("Kijai/MMAudio_safetensors", "mmaudio_vae_44k_fp16.safetensors", "mmaudio",
     "MMAudio VAE 44k fp16"),
]


def clone_node() -> None:
    target = COMFYUI_PATH / "custom_nodes" / NODE_DIR_NAME
    if target.exists():
        print(f"  [skip] custom node already cloned at {target}")
        return
    print(f"  [clone] {NODE_REPO} -> {target}")
    subprocess.run(["git", "clone", NODE_REPO, str(target)], check=True)


def download_weight(repo_id: str, filename: str, subfolder: str, label: str) -> None:
    dest = COMFYUI_PATH / "models" / subfolder
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / filename
    if target.exists():
        print(f"  [skip] {label} — already present ({target.stat().st_size/1e6:,.0f} MB)")
        return
    print(f"  [pull] {label}")
    print(f"         repo={repo_id} file={filename}")
    try:
        path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir=str(dest))
        size_mb = Path(path).stat().st_size / 1e6
        print(f"  [ ok ] {label} — {size_mb:,.0f} MB")
    except Exception as e:
        print(f"  [fail] {label}: {e}")


def main() -> int:
    if not COMFYUI_PATH.exists():
        sys.exit(f"ComfyUI path not found: {COMFYUI_PATH}")

    print("Caché Couture — MMAudio installer")
    print(f"  ComfyUI: {COMFYUI_PATH}")
    print()
    print("Cloning custom node...")
    clone_node()
    print()
    print("Downloading weights...")
    for entry in WEIGHTS:
        download_weight(*entry)

    print()
    print("MMAudio install complete. Restart ComfyUI; bigvgan_v2 will auto-download")
    print("on first 44k inference.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
Caché Couture — SUPIR installer.

Adds the Kijai/ComfyUI-SUPIR custom node and the weights it needs:
  - SUPIR-v0Q_fp16.safetensors  (2.66 GB) — pruned, default high-generalisation variant
  - sd_xl_base_1.0.safetensors  (6.94 GB) — required SDXL backbone
  - Optional: SUPIR-v0F_fp16.safetensors (2.66 GB) — light-degradation variant

Run after ComfyUI is closed (or accept that the node will only register on restart).
After install, restart ComfyUI; ComfyUI-Manager will offer to install the node's
Python deps automatically on first use, or run pip install -r requirements.txt
inside the ComfyUI-bundled Python.

Usage:
    python scripts/install_supir.py          # node + v0Q + SDXL backbone
    python scripts/install_supir.py --with-v0F   # also fetch v0F variant
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    sys.exit("huggingface_hub not installed. Run: pip install --user huggingface_hub")

COMFYUI_PATH = Path(r"C:\Users\Yoshii\Documents\ComfyUI")
NODE_REPO = "https://github.com/kijai/ComfyUI-SUPIR"
NODE_DIR_NAME = "ComfyUI-SUPIR"

# (repo_id, filename, subfolder under ComfyUI/models/, label)
CORE_WEIGHTS = [
    ("Kijai/SUPIR_pruned", "SUPIR-v0Q_fp16.safetensors", "checkpoints",
     "SUPIR v0Q fp16 (default)"),
    ("stabilityai/stable-diffusion-xl-base-1.0", "sd_xl_base_1.0.safetensors", "checkpoints",
     "SDXL base 1.0 (SUPIR backbone)"),
]

OPTIONAL_V0F = (
    "Kijai/SUPIR_pruned", "SUPIR-v0F_fp16.safetensors", "checkpoints",
    "SUPIR v0F fp16 (light degradation)",
)


def clone_node() -> None:
    nodes_dir = COMFYUI_PATH / "custom_nodes"
    target = nodes_dir / NODE_DIR_NAME
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-v0F", action="store_true",
                        help="Also fetch the v0F low-degradation variant")
    args = parser.parse_args()

    if not COMFYUI_PATH.exists():
        sys.exit(f"ComfyUI path not found: {COMFYUI_PATH}")

    print("Caché Couture — SUPIR installer")
    print(f"  ComfyUI: {COMFYUI_PATH}")
    print()
    print("Cloning custom node...")
    clone_node()
    print()
    print("Downloading weights...")
    for entry in CORE_WEIGHTS:
        download_weight(*entry)
    if args.with_v0F:
        download_weight(*OPTIONAL_V0F)

    print()
    print("SUPIR install complete. Restart ComfyUI; if the node fails to register,")
    print("install its Python deps inside ComfyUI's environment:")
    print(f"  cd {COMFYUI_PATH / 'custom_nodes' / NODE_DIR_NAME}")
    print(f"  <comfy python> -m pip install -r requirements.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

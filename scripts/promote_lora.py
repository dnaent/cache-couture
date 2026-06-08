"""Promote trained Caché LoRAs into the ComfyUI registry.

ai-toolkit writes to `outputs/loras/{faces,garments,utility}/<name>/<name>.safetensors`
(plus intermediate checkpoints). This script picks the highest-step .safetensors
per LoRA name and copies it to the canonical ComfyUI path:

  cache_face_m##   → ComfyUI/models/loras/cache/c1_faces/cache_face_m##.safetensors
  cache_garment_<col> → ComfyUI/models/loras/cache/c{2,3,4}_<col>/cache_garment_<col>.safetensors
  cache_chip       → ComfyUI/models/loras/cache/utility/cache_chip.safetensors

Per ComfyUI/models/loras/cache/README.md and CLAUDE.md §11.3.

USAGE
  python scripts/promote_lora.py                  # promote every cache_* LoRA
  python scripts/promote_lora.py M07              # only the M07 face LoRA
  python scripts/promote_lora.py lightware        # only the Lightware garment LoRA
  python scripts/promote_lora.py --dry-run        # print what would be copied
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LORA_OUT_ROOT = REPO / "outputs" / "loras"
COMFY_LORA_ROOT = Path("C:/Users/Yoshii/Documents/ComfyUI/models/loras/cache")

CLASS_FOR_NAME: dict[re.Pattern, str] = {
    re.compile(r"^cache_face_m\d{2}$"): "c1_faces",
    re.compile(r"^cache_garment_lightware$"): "c2_lightware",
    re.compile(r"^cache_garment_dailyware$"): "c3_dailyware",
    re.compile(r"^cache_garment_darkware$"): "c4_darkware",
    re.compile(r"^cache_chip$"): "utility",
}


def classify(name: str) -> str | None:
    for pat, cls in CLASS_FOR_NAME.items():
        if pat.match(name):
            return cls
    return None


STEP_RE = re.compile(r"_(\d{6,})\.safetensors$")


def latest_safetensors(name_dir: Path) -> Path | None:
    """Return the highest-step .safetensors in a training output dir.

    ai-toolkit names checkpoints like `<name>_000250.safetensors`,
    `<name>_000500.safetensors`, ..., `<name>.safetensors` for the final.
    Prefer the unsuffixed name; fall back to the highest numbered step.
    """
    files = list(name_dir.glob("*.safetensors"))
    if not files:
        return None
    final = name_dir / f"{name_dir.name}.safetensors"
    if final.exists():
        return final
    numbered = [(int(m.group(1)), p) for p in files if (m := STEP_RE.search(p.name))]
    if numbered:
        numbered.sort()
        return numbered[-1][1]
    files.sort(key=lambda p: p.stat().st_mtime)
    return files[-1]


def discover(selectors: list[str]) -> list[tuple[Path, str, str]]:
    """Resolve selectors to (source_safetensors, class_subdir, target_filename)."""
    out: list[tuple[Path, str, str]] = []
    if not LORA_OUT_ROOT.exists():
        return out
    # Two-level: outputs/loras/<subroot>/<name>/<name>.safetensors
    candidates: list[Path] = []
    for subroot in LORA_OUT_ROOT.iterdir():
        if subroot.is_dir():
            for name_dir in subroot.iterdir():
                if name_dir.is_dir():
                    candidates.append(name_dir)

    def matches(name: str) -> bool:
        if not selectors:
            return True
        for sel in selectors:
            if sel.upper().startswith("M") and sel[1:].isdigit():
                if name == f"cache_face_{sel.lower()}":
                    return True
            elif sel in ("lightware", "dailyware", "darkware"):
                if name == f"cache_garment_{sel}":
                    return True
            elif sel == "chip":
                if name == "cache_chip":
                    return True
            elif sel == name:
                return True
        return False

    for name_dir in candidates:
        name = name_dir.name
        if not matches(name):
            continue
        cls = classify(name)
        if not cls:
            print(f"!!! no registry class mapping for {name!r}, skipping")
            continue
        latest = latest_safetensors(name_dir)
        if not latest:
            print(f"!!! no .safetensors in {name_dir}")
            continue
        out.append((latest, cls, f"{name}.safetensors"))
    out.sort(key=lambda t: t[2])
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote trained Caché LoRAs into ComfyUI registry")
    parser.add_argument("selectors", nargs="*")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = discover(args.selectors)
    if not plan:
        print("Nothing to promote.")
        return 1

    print(f"Will promote {len(plan)} LoRA(s):")
    for src, cls, dst_name in plan:
        dst = COMFY_LORA_ROOT / cls / dst_name
        print(f"  {src.name}  ->  {dst}")

    if args.dry_run:
        return 0

    failed = 0
    for src, cls, dst_name in plan:
        dst_dir = COMFY_LORA_ROOT / cls
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / dst_name
        try:
            shutil.copy2(src, dst)
            print(f"  OK  {dst}")
        except OSError as e:
            print(f"  ERR  {dst}: {e}", file=sys.stderr)
            failed += 1
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Caché LoRA training driver.

Walks configs/ai_toolkit/ and runs each `cache_*.yaml` through the local
ai-toolkit at C:/Users/Yoshii/Documents/ai-toolkit/ (Python 3.12 venv,
torch 2.9.1+cu128). Per CLAUDE.md §17.2 and consistency_pipeline.md §6.

Each config trains one LoRA — face or garment — and writes intermediate
checkpoints to its own `training_folder` (typically
`cache_couture/outputs/loras/{faces,garments,utility}/<name>/`).

Promote the final .safetensors into the ComfyUI registry afterwards with
`scripts/promote_lora.py`.

USAGE
  python scripts/train_loras.py                  # train all configs
  python scripts/train_loras.py faces            # only cache_face_*.yaml
  python scripts/train_loras.py garments         # only cache_garment_*.yaml
  python scripts/train_loras.py M01 M02          # specific slot(s)
  python scripts/train_loras.py --dry-run        # print the commands only
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONFIGS_DIR = REPO / "configs" / "ai_toolkit"

AI_TOOLKIT = Path("C:/Users/Yoshii/Documents/ai-toolkit")
AI_TOOLKIT_PY = AI_TOOLKIT / "venv" / "Scripts" / "python.exe"
AI_TOOLKIT_RUN = AI_TOOLKIT / "run.py"


def discover_configs(selectors: list[str]) -> list[Path]:
    """Resolve selectors to a concrete ordered list of config paths.

    Selector grammar:
      - empty       → every cache_*.yaml (template excluded)
      - "faces"     → cache_face_*.yaml (template excluded)
      - "garments"  → cache_garment_*.yaml (template excluded)
      - "M07"       → cache_face_m07_qwen_12gb.yaml
      - "lightware" → cache_garment_lightware_qwen_12gb.yaml
      - explicit filename → that exact file
    """
    all_configs = sorted(
        p for p in CONFIGS_DIR.glob("cache_*.yaml") if "template" not in p.name
    )
    if not selectors:
        return all_configs

    resolved: list[Path] = []
    for sel in selectors:
        if sel == "faces":
            resolved.extend(p for p in all_configs if p.name.startswith("cache_face_"))
        elif sel == "garments":
            resolved.extend(p for p in all_configs if p.name.startswith("cache_garment_"))
        elif sel.upper().startswith("M") and sel[1:].isdigit():
            target = CONFIGS_DIR / f"cache_face_{sel.lower()}_qwen_12gb.yaml"
            if target.exists():
                resolved.append(target)
            else:
                print(f"!!! no config for {sel} at {target}")
        elif sel in ("lightware", "dailyware", "darkware"):
            target = CONFIGS_DIR / f"cache_garment_{sel}_qwen_12gb.yaml"
            if target.exists():
                resolved.append(target)
            else:
                print(f"!!! no config for {sel} at {target}")
        elif sel == "chip":
            target = CONFIGS_DIR / "cache_chip_qwen_12gb.yaml"
            if target.exists():
                resolved.append(target)
            else:
                print(f"!!! no config for chip at {target}")
        else:
            p = CONFIGS_DIR / sel if "/" not in sel else Path(sel)
            if p.exists():
                resolved.append(p)
            else:
                print(f"!!! unknown selector {sel!r}")

    # De-duplicate while preserving order
    seen: set[Path] = set()
    out: list[Path] = []
    for p in resolved:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def train_one(config: Path, dry_run: bool) -> tuple[Path, float, int]:
    cmd = [str(AI_TOOLKIT_PY), str(AI_TOOLKIT_RUN), str(config)]
    print(f"\n=== {config.name} ===")
    print(f"  cmd: {' '.join(cmd)}")
    if dry_run:
        return config, 0.0, 0
    t0 = time.monotonic()
    proc = subprocess.run(cmd, cwd=str(AI_TOOLKIT))
    elapsed = time.monotonic() - t0
    print(f"  -> exit {proc.returncode}  ({elapsed:.1f}s)")
    return config, elapsed, proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ai-toolkit on Caché LoRA configs")
    parser.add_argument("selectors", nargs="*", help="Empty for all; 'faces'/'garments'; slot like M07; collection like lightware; or explicit filename")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not AI_TOOLKIT_PY.exists() or not AI_TOOLKIT_RUN.exists():
        print(f"!!! ai-toolkit not found at {AI_TOOLKIT}", file=sys.stderr)
        return 2

    configs = discover_configs(args.selectors)
    if not configs:
        print("No configs matched.")
        return 1

    print(f"Will train {len(configs)} LoRA(s):")
    for c in configs:
        print(f"  - {c.name}")

    results: list[tuple[Path, float, int]] = []
    for c in configs:
        results.append(train_one(c, args.dry_run))

    print("\n=== summary ===")
    total = 0.0
    failed = 0
    for c, elapsed, rc in results:
        flag = "OK " if rc == 0 else f"ERR{rc}"
        print(f"  {flag}  {c.name}  ({elapsed:.1f}s)")
        total += elapsed
        if rc != 0:
            failed += 1
    print(f"\nTotal: {total/60:.1f} min, {failed} failure(s)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

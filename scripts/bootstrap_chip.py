"""Caché chip-mark bootstrap orchestrator.

Drives workflows/utility/qwen_edit_bootstrap.json against the canonical
microchip symbol (`brand/logos/cache_symbol.png`) to produce a training
set of the chip rendered as tonal embroidery / reflective yarn / woven
label patch / engraved hardware on a variety of garment label surfaces.

Output is the utility LoRA training set at `brand/chip/training_set/`,
consumed by `configs/ai_toolkit/cache_chip_qwen_12gb.yaml`.

Per CLAUDE.md §4 (materiality cues), §11.3 (LoRA registry), §16.4 (stacking
precedence), and consistency_pipeline.md sequencing step 7.

The chip is rendered SMALL, off-centre, never as a large logo — labels are
intentionally subtle. Curate to ~24–30 highest-fidelity images before
training.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

THIS = Path(__file__).resolve()
REPO = THIS.parent.parent
sys.path.insert(0, str(THIS.parent))

import comfy_client as cc  # noqa: E402

WORKFLOW_PATH = REPO / "workflows" / "utility" / "qwen_edit_bootstrap.json"
COMFY_BASE = Path("C:/Users/Yoshii/Documents/ComfyUI")
COMFY_INPUT = COMFY_BASE / "input"

SOURCE_LOGO = REPO / "brand" / "logos" / "cache_symbol.png"
TRAINING_SET = REPO / "brand" / "chip" / "training_set"
TRIGGER = "cache_chip"

# Finish × surface × angle matrix.
#
# Curation pass on 2026-05-20 retired two finishes:
#   - "tonal black-on-black embroidery" (old f1) — rendered with too much
#     contrast (white-on-black instead of tonal); replaced by subtle
#     reflective yarn in even light, which IS the canonical tonal default.
#   - "woven black-on-black label patch" (old f3) — Qwen defaulted to gold
#     yarn; concept dropped entirely. The chip is woven directly into the
#     garment fabric now, not applied as a separate stitched-on label patch.
#
# Active finishes for re-bootstrap (f1, f2). The existing f4 (engraved
# gunmetal hardware) plates remain in brand/chip/training_set/ from the
# prior run and are NOT regenerated.
FINISHES = [
    # f1 — subtle reflective yarn, default register (light diffused, reads grey)
    (
        "small chip mark woven directly into the garment fabric in subtle "
        "reflective yarn, viewed in even diffused natural light so the "
        "embroidery reads as a soft grey or light-grey tonal whisper against "
        "the black weave, no separate label patch, the chip is part of the weave"
    ),
    # f2 — subtle reflective yarn, light catching at angle (occasional flash)
    (
        "small chip mark woven directly into the garment fabric in subtle "
        "reflective yarn, with raking light catching the embroidery at a "
        "glancing angle so the chip momentarily reads as a clean cool silver "
        "flash against the black weave, no separate label patch, the chip is "
        "part of the weave"
    ),
]
SURFACES = [
    "on the back of a black hood, centred just below the hood crown seam",
    "on the back-right pocket of black technical trousers",
    "halfway up the right trouser leg of black technical trousers, outer side",
    "halfway up the left arm of a black technical jacket sleeve, outer side",
]
ANGLES = [
    "macro close-up of the chip mark only, fabric weave visible around it",
    "mid-distance crop showing the chip in context of the garment region, "
    "three-quarter angle",
]

POSITIVE_PREAMBLE = (
    "Caché Couture chip mark — stylised microchip emblem with square silhouette, "
    "pin/lead protrusions on all four sides, internal circuit/maze pattern, "
    "rendered very small, subtle, and off-centre — never a large or showy logo. "
    "The chip is integrated into the matte black technical fabric weave. "
    "Magazine grade, 35mm, ISO 100, f/8, crisp focus"
)
NEGATIVE = (
    "wordmark, text characters, letters, alphabet, large logo, oversized emblem, "
    "centred composition, high contrast white-on-black, stark black-and-white, "
    "gold yarn, gold thread, yellow, brass colour, saturated colours, neon, "
    "bright background, vibrant, visible logo text, watermark, harsh shadows, "
    "low resolution, AI artefacts, cluttered background, props, "
    "separate sewn-on label patch, stitched-on emblem badge"
)


def ensure_logo_in_comfy() -> str:
    if not SOURCE_LOGO.exists():
        raise FileNotFoundError(f"No chip logo at {SOURCE_LOGO}")
    dst_dir = COMFY_INPUT / "cache" / "logos"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / "cache_symbol.png"
    shutil.copy2(SOURCE_LOGO, dst)
    return "cache/logos/cache_symbol.png"


def write_caption(image_path: Path, finish: str, surface: str, angle: str) -> Path:
    caption = f"{TRIGGER}, {finish}, {surface}, {angle}"
    cap_path = image_path.with_suffix(".txt")
    cap_path.write_text(caption, encoding="utf-8")
    return cap_path


def bootstrap(base_seed: int = 3000, dry_run: bool = False) -> None:
    image_rel = ensure_logo_in_comfy()
    print(f"\n=== chip ===")
    print(f"  source: {image_rel}")
    TRAINING_SET.mkdir(parents=True, exist_ok=True)

    workflow = cc.load_workflow(WORKFLOW_PATH)
    total = len(FINISHES) * len(SURFACES) * len(ANGLES)
    i = 0
    for f_idx, finish in enumerate(FINISHES, start=1):
        for s_idx, surface in enumerate(SURFACES, start=1):
            for a_idx, angle in enumerate(ANGLES, start=1):
                i += 1
                seed = base_seed + i
                positive = (
                    f"{POSITIVE_PREAMBLE}, extract the chip emblem from this source "
                    f"and re-render it: {finish} {surface}, {angle}"
                )
                prefix = f"cache/chip_bootstrap/f{f_idx}_s{s_idx}_a{a_idx}"
                patches = {
                    "4": {"image": image_rel},
                    "6": {"prompt": positive},
                    "7": {"prompt": NEGATIVE},
                    "8": {"seed": seed},
                    "10": {"filename_prefix": prefix},
                }
                patched = cc.substitute(workflow, patches)
                print(
                    f"  [{i:02d}/{total}] f{f_idx}-s{s_idx}-a{a_idx}  seed={seed}  "
                    f"{finish[:40]} / {surface[:25]}"
                )
                if dry_run:
                    continue
                t0 = time.monotonic()
                entry = cc.submit_and_wait(patched, poll_interval=2.0, timeout=900.0)
                elapsed = time.monotonic() - t0
                written = cc.fetch_outputs(entry, TRAINING_SET)
                for img_path in written:
                    write_caption(img_path, finish, surface, angle)
                print(f"        -> {len(written)} img + captions in {elapsed:.1f}s -> {TRAINING_SET}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap chip-mark training set via Qwen Image Edit")
    parser.add_argument("--base-seed", type=int, default=3000)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"ComfyUI host: {cc.SERVER_ADDRESS}")
    if not args.dry_run:
        stats = cc.system_stats()
        dev = stats["devices"][0] if stats.get("devices") else {}
        print(f"  device: {dev.get('name', '?')}")
        print(f"  vram free: {dev.get('vram_free', 0) / 1024**3:.2f} GiB")

    bootstrap(base_seed=args.base_seed, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

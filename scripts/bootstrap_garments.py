"""Caché garment-bootstrap orchestrator.

For each collection (lightware / dailyware / darkware), drives
workflows/utility/qwen_edit_bootstrap.json against the corresponding
brand/lookbook/core_<collection>.png plate, prompting Qwen Image Edit
to isolate one garment at a time and re-render it as a floating studio
mockup. Each garment is rendered on BOTH backdrops:

  - #0A0A0A off-black (stealth / reflective macro register)
  - #FAFAF7 warm bone (canonical lookbook register)

Both backdrops feed the same C2/C3/C4 garment LoRA so reflective physics
travel with the garment regardless of downstream lighting. Per
.claude/consistency_pipeline.md sequencing step 4.

Lean schema: 6 representative garments per collection × 2 backdrops × 1
angle = 12 plates per collection. Operator curates to the highest-fidelity
~50% before training, matching the concise approach used for chip.
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

COLLECTIONS = ["lightware", "dailyware", "darkware"]

BACKDROPS = {
    "offblack": "on off-black seamless backdrop, hex #0A0A0A, low-key register, single specular highlight to reveal reflective yarn and gunmetal hardware",
    "bone": "on warm bone seamless backdrop, hex #FAFAF7, soft even diffused front fill, canonical lookbook register",
}

# Per-collection garment lists. Each entry becomes one "extract and re-render"
# variation. 6 garments per collection × 2 backdrops × 1 angle = 12 plates
# per collection. Selected for representative coverage — one outerwear,
# one mid-layer, one bottom, plus collection-defining accessories or cuts.
# Operator can edit this list to bias the bootstrap toward any garment
# under-represented in the resulting LoRA.
GARMENTS = {
    "lightware": [
        "cropped technical hoodie, raglan sleeves",
        "lightweight track jacket, full zip, mock collar",
        "essential tee, dropped shoulder",
        "cut-out crop top, asymmetric hem",
        "tailored sweatpant, tapered ankle",
        "lightweight balaclava, ribbed knit",
    ],
    "dailyware": [
        "heavy slightly oversized tee, dropped shoulder, ribbed crew neck, pure cotton",
        "essential cotton hoodie, slightly oversized, kangaroo pocket, ribbed cuff and hem, pure cotton",
        "lightweight cotton half-zip pullover, mock collar, slim placket, pure cotton",
        "straight-leg essential cotton joggers, no taper, elasticated waist with drawcord, pure cotton",
        "straight-leg cotton cargo pant, daily weight, side-leg cargo pockets, pure cotton",
        "mid-thigh cotton shorts, elasticated waist with drawcord, pure cotton",
    ],
    "darkware": [
        "voluminous hooded puffer jacket, baffled construction, high collar",
        "longline puffer coat, mid-thigh hem, baffled construction",
        "puffer gilet, standing collar, full-zip",
        "heavy outerwear-grade fleece quarter-zip, high collar, thick pile, technical weight",
        "heavy utility straight-leg cargo trouser, technical fabric, padded knee, no taper",
        "ski goggles, mirrored lens",
    ],
}

POSITIVE_PREAMBLE = (
    "isolated single garment, floating studio mockup, no model, no mannequin, "
    "ghost mannequin invisible mannequin effect, Caché Couture stealth black streetwear, "
    "matte technical fabric, subtle reflective yarn, gunmetal hardware, "
    "ultra-detailed weave texture, magazine grade, 35mm, ISO 100, f/8, crisp focus"
)
NEGATIVE = (
    "model wearing garment, person, body, face, hands, mannequin visible, "
    "saturated colours, neon, bright background, visible logo text, watermark, "
    "harsh shadows, low resolution, AI artefacts, cluttered background, props"
)

ANGLE_VARIANTS = ["three-quarter angle from the right"]


def ensure_plate_in_comfy(collection: str) -> str:
    src = REPO / "brand" / "lookbook" / f"core_{collection}.png"
    if not src.exists():
        raise FileNotFoundError(f"No lookbook plate for {collection} at {src}")
    dst_dir = COMFY_INPUT / "cache" / "lookbook"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / f"core_{collection}.png"
    shutil.copy2(src, dst)
    return f"cache/lookbook/core_{collection}.png"


def write_caption(image_path: Path, trigger: str, garment: str, backdrop_key: str, angle: str) -> Path:
    """Write a `.txt` caption next to an image (ai-toolkit reads by stem)."""
    backdrop_phrase = "off-black seamless backdrop" if backdrop_key == "offblack" else "warm bone seamless backdrop"
    caption = f"{trigger}, {garment}, {angle}, on {backdrop_phrase}"
    cap_path = image_path.with_suffix(".txt")
    cap_path.write_text(caption, encoding="utf-8")
    return cap_path


def bootstrap_collection(
    collection: str, base_seed: int = 2000, dry_run: bool = False
) -> None:
    print(f"\n=== {collection} ===")
    image_rel = ensure_plate_in_comfy(collection)
    print(f"  plate: {image_rel}")

    workflow = cc.load_workflow(WORKFLOW_PATH)
    garments = GARMENTS[collection]
    total = len(garments) * len(BACKDROPS) * len(ANGLE_VARIANTS)
    trigger = f"{collection}_set"
    i = 0

    for backdrop_key, backdrop_text in BACKDROPS.items():
        dest = REPO / "brand" / "garments" / collection / "training_set" / backdrop_key
        dest.mkdir(parents=True, exist_ok=True)
        for g_idx, garment in enumerate(garments, start=1):
            for a_idx, angle in enumerate(ANGLE_VARIANTS, start=1):
                i += 1
                # Resume: skip if a plate with this (garment, angle) already exists.
                existing = list(dest.glob(f"g{g_idx:02d}_a{a_idx}_*.png"))
                if existing:
                    print(
                        f"  [{i:02d}/{total}] {backdrop_key:8s} g{g_idx:02d}-a{a_idx}  "
                        f"SKIP (already have {existing[0].name})"
                    )
                    continue
                seed = base_seed + i
                positive = (
                    f"{POSITIVE_PREAMBLE}, extract from this lookbook plate and re-render: "
                    f"the {garment}, {angle}, {backdrop_text}"
                )
                prefix = (
                    f"cache/garment_bootstrap/{collection}/{backdrop_key}/"
                    f"g{g_idx:02d}_a{a_idx}"
                )
                patches = {
                    "4": {"image": image_rel},
                    "6": {"prompt": positive},
                    "7": {"prompt": NEGATIVE},
                    "8": {"seed": seed},
                    "10": {"filename_prefix": prefix},
                }
                patched = cc.substitute(workflow, patches)
                print(
                    f"  [{i:02d}/{total}] {backdrop_key:8s} g{g_idx:02d}-a{a_idx}  "
                    f"seed={seed}  {garment[:55]}"
                )
                if dry_run:
                    continue
                t0 = time.monotonic()
                entry = cc.submit_and_wait(patched, poll_interval=2.0, timeout=900.0)
                elapsed = time.monotonic() - t0
                written = cc.fetch_outputs(entry, dest)
                for img_path in written:
                    write_caption(img_path, trigger, garment, backdrop_key, angle)
                print(f"        -> {len(written)} img + captions in {elapsed:.1f}s -> {dest}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap garment training sets via Qwen Image Edit")
    parser.add_argument(
        "collections",
        nargs="*",
        default=COLLECTIONS,
        help=f"Collections to process (default: all: {' '.join(COLLECTIONS)})",
    )
    parser.add_argument("--base-seed", type=int, default=2000)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"ComfyUI host: {cc.SERVER_ADDRESS}")
    if not args.dry_run:
        stats = cc.system_stats()
        dev = stats["devices"][0] if stats.get("devices") else {}
        print(f"  device: {dev.get('name', '?')}")
        print(f"  vram free: {dev.get('vram_free', 0) / 1024**3:.2f} GiB")

    for collection in args.collections:
        if collection not in COLLECTIONS:
            print(f"!!! {collection} not in {COLLECTIONS}, skipping")
            continue
        bootstrap_collection(collection, base_seed=args.base_seed, dry_run=args.dry_run)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

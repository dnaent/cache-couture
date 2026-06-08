"""One-shot: generate candidate source portraits for the new M03 identity.

M03 was reassigned on 2026-05-21 from the retired East Asian woman slot to a
new identity: Mixed Race (Black/White) woman, natural curves (soft hourglass),
natural curly hair (medium-volume coils). The slot is blocked on a source
portrait. This script renders four candidates via Qwen Image t2i so the
operator can pick the best one; the chosen file then becomes
`brand/models/M03/source/portrait.jpg`.

Output directory: `outputs/m03_candidates/` (project repo)
Then ComfyUI copies them back from `ComfyUI/output/cache/portraits/m03_*/`.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

THIS = Path(__file__).resolve()
REPO = THIS.parent.parent
sys.path.insert(0, str(THIS.parent))

import comfy_client as cc  # noqa: E402

WORKFLOW_PATH = REPO / "workflows" / "utility" / "qwen_t2i_portrait.json"
DEST = REPO / "outputs" / "m03_candidates"

# Brand-voice prompt matching the canonical lookbook register
# (CLAUDE.md §2.5, §11.1, plus M03 profile descriptor).
POSITIVE = (
    "editorial fashion photography, Caché Couture, "
    "Mixed Race (Black/White) woman in her late twenties, "
    "warm light brown skin, naturally curly hair with medium-volume coils framing the face, "
    "soft hourglass build with natural curves, full-figured but athletic, "
    "wearing a fitted black cropped technical hoodie with raglan sleeves "
    "and tailored black sweatpants with tapered ankle (Caché Lightware), "
    "matte technical fabric, subtle reflective yarn highlights, "
    "warm off-white seamless studio backdrop, soft even diffused front fill, "
    "full body frontal stance, hands relaxed at sides, neutral expression, "
    "frame from head to feet, monochromatic palette, no logos visible, "
    "ultra-detailed weave texture, magazine grade, "
    "35mm, shot on Phase One, ISO 100, f/8, crisp focus"
)

NEGATIVE = (
    "saturated colours, neon, bright background, vibrant, sunset lighting, "
    "visible logo text, watermark, harsh shadows, low resolution, plastic skin, "
    "AI artefacts, extra fingers, distorted face, warped hands, cluttered background, "
    "props, motion blur, sepia, vintage filter, "
    "straight hair, bald, very short hair, "
    "thin frame, skinny, athletic-thin, masculine build"
)

SEEDS = [4101, 4102, 4103, 4104]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate M03 source-portrait candidates")
    parser.add_argument("--seeds", type=int, nargs="*", default=SEEDS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"ComfyUI host: {cc.SERVER_ADDRESS}")
    if not args.dry_run:
        stats = cc.system_stats()
        dev = stats["devices"][0] if stats.get("devices") else {}
        print(f"  device: {dev.get('name', '?')}")
        print(f"  vram free: {dev.get('vram_free', 0) / 1024**3:.2f} GiB")

    DEST.mkdir(parents=True, exist_ok=True)
    workflow = cc.load_workflow(WORKFLOW_PATH)

    for i, seed in enumerate(args.seeds, start=1):
        prefix = f"cache/portraits/m03_cand_{i:02d}"
        patches = {
            "6": {"text": POSITIVE},
            "7": {"text": NEGATIVE},
            "8": {"seed": seed},
            "10": {"filename_prefix": prefix},
        }
        patched = cc.substitute(workflow, patches)
        print(f"  [{i:02d}/{len(args.seeds)}] seed={seed}")
        if args.dry_run:
            continue
        t0 = time.monotonic()
        entry = cc.submit_and_wait(patched, poll_interval=2.0, timeout=600.0)
        elapsed = time.monotonic() - t0
        written = cc.fetch_outputs(entry, DEST)
        print(f"        -> {len(written)} img in {elapsed:.1f}s -> {DEST}")

    print(f"\nCandidates in: {DEST}")
    print("Pick the best one and copy it to brand/models/M03/source/portrait.jpg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Caché face-bootstrap orchestrator.

For each active cast slot (M01, M02, M04..M10), copies the source portrait
into ComfyUI/input/cache/M##/ and drives workflows/utility/qwen_edit_bootstrap.json
through a fixed 12-variation set that varies pose, framing, angle, expression,
and lighting while preserving identity via Qwen Image Edit's image-conditioning.

The variation set is split 6/6:
  - 6 full-body framings (frontal stance, walk, contrapposto, profile, seated,
    leaning) so the LoRA learns the model's BUILD and silhouette.
  - 6 head/expression crops so face fidelity stays sharp.

Each caption is built from the model's profile.md (ethnicity / build / hair)
so the trigger token learns face + physique together — at inference time
`m02_face` alone will recover the lean tall build, not just the face.

Outputs land in ComfyUI/output/cache/face_bootstrap/M##/ then get pulled back
into brand/models/M##/training_set/ with a sibling caption .txt per image.

Per .claude/consistency_pipeline.md §Tier 2 step 1. Some identity drift is
expected — the operator curates to the highest-fidelity ~50% before training.
"""

from __future__ import annotations

import argparse
import re
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
COMFY_OUTPUT = COMFY_BASE / "output"

ACTIVE_SLOTS = ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10"]

# 12 variations, split 6 full-body + 6 head/expression.
#
# Each entry: (framing_key, prompt_fragment). The framing_key controls
# whether the prompt requests a full-body crop ("full") or chest-up
# crop ("head") — this is appended automatically so we don't have to
# repeat it in every line.
VARIATIONS = [
    # ---- 6 full-body framings (build / silhouette / posture) ----
    ("full", "frontal stance, hands relaxed at sides, weight evenly on both feet"),
    ("full", "three-quarter walk pose, mid-step, one foot forward, arms swinging naturally"),
    ("full", "contrapposto, weight shifted to one leg, opposite hip raised"),
    ("full", "side-on profile view, arms at sides"),
    ("full", "seated on a backless studio stool, knees together, hands resting on thighs"),
    ("full", "leaning one shoulder against an unseen wall, arms folded"),
    # ---- 6 head / expression / lighting variations (face fidelity) ----
    ("head", "frontal gaze directly at camera, neutral mouth"),
    ("head", "head turned slightly left, three-quarter angle"),
    ("head", "head turned slightly right, three-quarter angle"),
    ("head", "subtle smile, mouth closed"),
    ("head", "low-key rim lighting from behind, single specular highlight, off-black backdrop"),
    ("head", "warm bone backdrop, soft frontal fill, even diffused light"),
]

FRAMING_PROMPTS = {
    "full": "full body framing head to feet, model's complete silhouette visible, build and proportions legible",
    "head": "close crop from chest up, face dominates the frame",
}

POSITIVE_PREAMBLE = (
    "same person, identity preserved, same face structure, same body type, "
    "Caché Couture stealth black streetwear, matte technical fabrics, "
    "warm off-white seamless studio backdrop unless otherwise specified, "
    "soft even diffused front fill, neutral expression unless otherwise specified, "
    "magazine grade, 35mm, ISO 100, f/8, crisp focus"
)
NEGATIVE = (
    "different person, identity drift, body type drift, build change, "
    "warped face, distorted hands, extra fingers, "
    "saturated colours, neon, bright background, visible logo text, watermark, "
    "harsh shadows, low resolution, plastic skin, AI artefacts, cluttered background"
)


# ---------------------------------------------------------------------------
# profile.md parsing
# ---------------------------------------------------------------------------

_PROFILE_FIELDS = ("Pronouns", "Apparent ethnicity", "Hair (in source)", "Build")


def parse_profile(slot: str) -> dict[str, str]:
    """Extract the markdown-table rows from brand/models/M##/profile.md.

    Returns a dict with at minimum: pronouns, ethnicity, hair, build.
    Each value is the right-hand cell, stripped of whitespace and trailing
    parentheticals like '(operator to confirm)'.
    """
    path = REPO / "brand" / "models" / slot / "profile.md"
    if not path.exists():
        raise FileNotFoundError(f"No profile.md for {slot} at {path}")
    text = path.read_text(encoding="utf-8")

    fields: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", line)
        if not m:
            continue
        key, value = m.group(1).strip(), m.group(2).strip()
        if key in _PROFILE_FIELDS:
            # Strip trailing parentheticals like "(operator to confirm)"
            value = re.sub(r"\s*\([^)]*\)\s*$", "", value).strip()
            fields[key] = value

    return {
        "pronouns": fields.get("Pronouns", "they/them"),
        "ethnicity": fields.get("Apparent ethnicity", ""),
        "hair": fields.get("Hair (in source)", ""),
        "build": fields.get("Build", "average build"),
    }


def physique_phrase(profile: dict[str, str]) -> str:
    """Compose a brand-voice descriptor for caption / prompt injection.

    Example output: "Black man, lean tall build, very short close cut hair"
    """
    pronouns = profile.get("pronouns", "they/them").lower()
    if "she" in pronouns:
        gender = "woman"
    elif "he" in pronouns:
        gender = "man"
    else:
        gender = "person"

    ethnicity = profile.get("ethnicity", "").strip()
    build = profile.get("build", "").strip().rstrip(".").lower()
    hair = profile.get("hair", "").strip().rstrip(".").lower()

    parts = []
    if ethnicity:
        parts.append(f"{ethnicity} {gender}")
    else:
        parts.append(gender)
    if build:
        parts.append(f"{build} build" if "build" not in build else build)
    if hair:
        parts.append(f"{hair} hair" if "hair" not in hair else hair)
    return ", ".join(parts)


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

def ensure_source_in_comfy(slot: str) -> str | None:
    """Copy the slot's source portrait into ComfyUI/input. Returns the
    relative path LoadImage expects, or None if the source is missing
    (slot is awaiting an operator drop — caller should skip it)."""
    src = REPO / "brand" / "models" / slot / "source" / "portrait.jpg"
    if not src.exists():
        return None
    dst_dir = COMFY_INPUT / "cache" / slot
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / "portrait.jpg"
    shutil.copy2(src, dst)
    return f"cache/{slot}/portrait.jpg"


def write_caption(
    image_path: Path, trigger: str, physique: str, framing_key: str, variation: str
) -> Path:
    framing_phrase = FRAMING_PROMPTS[framing_key]
    caption = f"{trigger}, {physique}, {framing_phrase}, {variation}"
    cap_path = image_path.with_suffix(".txt")
    cap_path.write_text(caption, encoding="utf-8")
    return cap_path


def bootstrap_slot(slot: str, base_seed: int = 1000, dry_run: bool = False) -> None:
    print(f"\n=== {slot} ===")
    image_rel = ensure_source_in_comfy(slot)
    if image_rel is None:
        print(f"  !!! no source portrait for {slot} — slot awaits operator drop, skipping")
        return
    profile = parse_profile(slot)
    physique = physique_phrase(profile)
    print(f"  physique: {physique}")
    print(f"  source:   {image_rel}")

    workflow = cc.load_workflow(WORKFLOW_PATH)
    dest = REPO / "brand" / "models" / slot / "training_set"
    dest.mkdir(parents=True, exist_ok=True)
    trigger = f"{slot.lower()}_face"

    for i, (framing_key, variation) in enumerate(VARIATIONS, start=1):
        # Resume: skip if a plate with this variation index already exists.
        existing = list(dest.glob(f"v{i:02d}_{framing_key}_*.png"))
        if existing:
            print(f"  [{i:02d}/{len(VARIATIONS)}] {framing_key:4s}  SKIP (already have {existing[0].name})")
            continue
        framing_phrase = FRAMING_PROMPTS[framing_key]
        positive = (
            f"{POSITIVE_PREAMBLE}, {physique}, {framing_phrase}, {variation}"
        )
        seed = base_seed + i
        prefix = f"cache/face_bootstrap/{slot}/v{i:02d}_{framing_key}"
        patches = {
            "4": {"image": image_rel},
            "6": {"prompt": positive},
            "7": {"prompt": NEGATIVE},
            "8": {"seed": seed},
            "10": {"filename_prefix": prefix},
        }
        patched = cc.substitute(workflow, patches)
        print(
            f"  [{i:02d}/{len(VARIATIONS)}] {framing_key:4s}  seed={seed}  "
            f"{variation[:60]}"
        )
        if dry_run:
            continue
        t0 = time.monotonic()
        entry = cc.submit_and_wait(patched, poll_interval=2.0, timeout=900.0)
        elapsed = time.monotonic() - t0
        written = cc.fetch_outputs(entry, dest)
        for img_path in written:
            write_caption(img_path, trigger, physique, framing_key, variation)
        print(f"        -> {len(written)} img + captions in {elapsed:.1f}s -> {dest}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap face training sets via Qwen Image Edit")
    parser.add_argument(
        "slots",
        nargs="*",
        default=ACTIVE_SLOTS,
        help=f"Slots to process (default: all active: {' '.join(ACTIVE_SLOTS)})",
    )
    parser.add_argument("--base-seed", type=int, default=1000)
    parser.add_argument("--dry-run", action="store_true", help="Skip submission, just print")
    args = parser.parse_args()

    print(f"ComfyUI host: {cc.SERVER_ADDRESS}")
    if not args.dry_run:
        stats = cc.system_stats()
        dev = stats["devices"][0] if stats.get("devices") else {}
        print(f"  device: {dev.get('name', '?')}")
        print(f"  vram free: {dev.get('vram_free', 0) / 1024**3:.2f} GiB")

    for slot in args.slots:
        if slot not in ACTIVE_SLOTS:
            print(f"!!! {slot} is not in active roster, skipping")
            continue
        bootstrap_slot(slot, base_seed=args.base_seed, dry_run=args.dry_run)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

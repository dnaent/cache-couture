# Caché utility workflows

Utility workflows are **bootstrap / curation** graphs that produce the inputs
for LoRA training. They are not part of the eight production workflows gated
in CLAUDE.md §17.3 (`workflows/{stills,video}/01..08`).

## qwen_edit_bootstrap.json

Single Qwen Image Edit graph that both bootstrap orchestrators drive:

```
LoadImage ─┬─→ VAEEncode ───────────────┐
           ├─→ TextEncodeQwenImageEdit ─┤  (positive, image-conditioned)
           └─→ TextEncodeQwenImageEdit ─┤  (negative, image-conditioned)
                                        ├─→ KSampler → VAEDecode → SaveImage
UNETLoader  (qwen_image_edit_fp8) ──────┘
CLIPLoader  (qwen_2.5_vl_7b_fp8, type=qwen_image)
VAELoader   (qwen_image_vae)
```

Defaults: euler / simple, 20 steps, cfg 2.5, denoise 1.0. Suitable starting
point for a 12 GB card; tune from the orchestrator if needed.

### Orchestrators

- `scripts/bootstrap_faces.py` — per cast slot M##, 20 variations
  (pose/angle/expression/lighting) per source portrait. Outputs to
  `brand/models/M##/training_set/`.
- `scripts/bootstrap_garments.py` — per collection, 8 garments × 2 backdrops
  × 2 angles = 32 plates per collection. Outputs to
  `brand/garments/<collection>/training_set/{offblack,bone}/`.
- `scripts/bootstrap_chip.py` — chip mark × 4 finishes × 4 surfaces × 2
  angles = 32 plates. Outputs to `brand/chip/training_set/`. Source asset
  is `brand/logos/cache_symbol.png`.

Both orchestrators:

1. Copy the source asset into `ComfyUI/input/cache/...` so `LoadImage` resolves it.
2. Submit the workflow once per variation via `comfy_client.submit_and_wait`.
3. Fetch outputs from `ComfyUI/output/...` back to the repo training-set folder.

### Smoke test

```powershell
$env:COMFYUI_HOST = "127.0.0.1:8000"
python scripts\bootstrap_faces.py M01 --dry-run        # prints the plan, no GPU
python scripts\bootstrap_faces.py M01                  # runs 20 generations for M01 only
python scripts\bootstrap_garments.py lightware --dry-run
```

### Notes

- Identity drift is expected; curate to ~15–20 (faces) / 20–30 (garments)
  before training. See `.claude/consistency_pipeline.md` §Tier 2.
- A Lightning 4-step LoRA + lower step count can be wired in for faster
  drafts later; keep the canonical workflow at full 20 steps for quality.
- ControlNet-Union (pose channel) is intentionally **not** stacked in v1
  of this workflow — Qwen Image Edit's image-conditioning resists pose
  changes regardless. If pose-locked results need overriding, add a second
  variant (`qwen_edit_bootstrap_pose.json`) that drops Edit for vanilla
  Qwen Image + InstantX ControlNet-Union pose.

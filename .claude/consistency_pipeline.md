# Caché — Model Consistency Pipeline

> How we keep the same human models legible across every garment, collection, and
> campaign. Sits on top of the ratified Qwen Image + WAN 2.2 stack (CLAUDE.md §8).

---

## Problem

We have a fixed cast of human models (the source portraits in `consistent_models/`).
Every drop will swap their clothes, location, accessories, pose, lighting condition,
and motion. Their **face and body identity must not drift** between outputs.

Out-of-the-box prompt-only generation does not solve this — even with detailed
descriptions, faces shift run-to-run. We need an identity-locking strategy.

---

## Three-tier approach

The pipeline runs in tiers. Each tier costs more upfront effort but unlocks more
creative freedom downstream. Most production assets will use Tier 1; Tier 2 unlocks
campaigns that need novel poses; Tier 3 is for the lookbook lineup plates.

### Tier 1 — Qwen Image Edit garment swap (zero training)

**Use when:** swapping garments on an existing source portrait. Same pose, same
backdrop, same model.

**How:**
1. Load the source portrait from `brand/models/<slug>/source/portrait.jpg` into
   `qwen_image_edit_fp8_e4m3fn.safetensors`.
2. Mask out the existing clothing (auto-segment via SAM or manual).
3. Prompt the new garment in brand-voice technical language (CLAUDE.md §6 + §11).
4. Render at native resolution; upscale with 4x-UltraSharp → SUPIR (tiled) for
   print-ready output.

**Pros:** Identity is preserved at 100% fidelity — it's literally the same
photograph, only the garment region is regenerated. Fast (single inference pass).

**Cons:** Pose, framing, and lighting are locked to the source portrait. You
cannot ask the model to turn their head, walk, or stand in a different scene.

**Workflow file:** `workflows/stills/03_garment_inpaint_qwen_edit.json` (TBD).

### Tier 2 — Per-model character LoRA (modest training)

**Use when:** you need the same model in a *new* pose, scene, expression, or
crop that the source portrait cannot provide.

**How:**
1. **Bootstrap a training set from the single source portrait** using Tier 1:
   - Generate 12 variations of the same model — 6 full-body framings (frontal,
     walk, contrapposto, profile, seated, leaning) so the LoRA learns the
     model's BUILD as well as their face, plus 6 head/expression crops so
     face fidelity stays sharp.
   - Each variation preserves identity but changes stance/framing/lighting.
   - Captions embed the per-slot physique descriptor pulled from `profile.md`
     (ethnicity / build / hair), so the trigger token learns face + physique.
   - Curate aggressively to the highest-fidelity ~6–8 images per model
     (lean schema; matches the chip-set discipline).
2. **Caption** is written inline by the bootstrap orchestrator as a sibling
   `.txt` to each generated image. The trigger token is `m##_face` (e.g.
   `m01_face`). ai-toolkit reads captions by stem from `training_set/`; the
   sibling `captions/` folder is retained for hand-edited overrides only.
3. **Train a Qwen Image LoRA** (rank 16–32, 1500–2500 steps) using
   ai-toolkit by Ostris or a comparable trainer. Output goes to
   `ComfyUI/models/loras/cache/c1_faces/<slug>.safetensors`.
4. **Inference:** stack the per-model face LoRA at 0.85–1.0 with the matching
   collection garment LoRA (`cache_garment_<lightware|dailyware|darkware>`) at
   0.6–0.85. No `cache_brand` — brand DNA travels with the face + garment LoRAs.

**Pros:** Full creative freedom — any pose, any scene, any lighting, identity
locked.

**Cons:** Training time (~45 min per model on the RTX 3080 Ti). Bootstrap step
introduces some identity drift; we curate aggressively to keep the LoRA tight.

**LoRA naming:** `cache_face_m01.safetensors` … `cache_face_m10.safetensors` per
`brand/models/INDEX.md`.

### Tier 3 — Garment-LoRA stacking + manual lineup composite (campaign-level)

**Use when:** generating the brand-signature "lineup plate" — multiple models
side-by-side as a single horizontal composition (CLAUDE.md §2.5, §12.1).

**How:**
1. For each figure, render in Qwen Image stacking the Tier-2 face LoRA
   (`cache_face_m##` at 0.85–1.0) with the matching collection garment LoRA
   (`cache_garment_<collection>` at 0.6–0.85, where `<collection>` is one of
   `lightware`, `dailyware`, `darkware`).
2. Lock backdrop + lighting via a shared prompt fragment (`on warm bone seamless
   backdrop` for canonical lookbook, `on off-black seamless backdrop` for
   stealth/macro) and offset seeds (`seed`, `seed+1`, …) per figure.
3. Composite side-by-side manually at 1920 × 1080 (or 2560 × 1440 for hero) —
   the lineup is a compositing step, not a learned behaviour.

**Strength stacking:** `cache_face_m01` at 0.9 + `cache_garment_darkware` at
0.75. No global brand LoRA — brand DNA is encoded into both LoRAs via their
training-set bias.

**Note:** The earlier plan to train a `cache_core_<collection>` "lineup
composition LoRA" was dropped. With C1+C2/C3/C4 stacking, lineup framing is
purely a compositing concern; a learned lineup behaviour would just duplicate
what manual side-by-side already produces.

---

## Why not IP-Adapter / PuLID / InstantID alone?

Reference-image identity adapters (IP-Adapter, PuLID, InstantID) lock the **face**
well from a single reference but routinely lose body shape, hand structure, and
subtle facial features under heavy prompt rewrites. They are useful as an
*augment* to Tier 1 (e.g., enforcing face fidelity inside a Qwen Edit pass) but
should not be the primary identity mechanism for a brand whose stealth-wealth
positioning depends on quiet, exact consistency.

A PuLID-Qwen integration may land in the next ComfyUI update — when it does,
re-evaluate as a Tier 1.5 option.

---

## Directory map

```
cache_couture/
├── consistent_models/                # raw source portraits (input)
└── brand/
    ├── models/                       # C1 face-LoRA inputs
    │   ├── INDEX.md                  # cast catalogue
    │   ├── M01/
    │   │   ├── profile.md            # name, descriptors, LoRA status
    │   │   ├── source/portrait.jpg   # the canonical source shot
    │   │   ├── training_set/         # bootstrapped variations (Tier 2 input)
    │   │   └── captions/             # per-image .txt for training
    │   └── M02..M10/
    └── garments/                     # C2/C3/C4 garment-LoRA inputs
        ├── lightware/{training_set/{offblack,bone},captions}/
        ├── dailyware/{training_set/{offblack,bone},captions}/
        └── darkware/{training_set/{offblack,bone},captions}/

ComfyUI/
└── models/
    └── loras/
        └── cache/
            ├── c1_faces/             # cache_face_m##.safetensors (9 active)
            ├── c2_lightware/         # cache_garment_lightware.safetensors
            ├── c3_dailyware/         # cache_garment_dailyware.safetensors
            ├── c4_darkware/          # cache_garment_darkware.safetensors
            └── utility/              # cache_chip.safetensors
```

---

## Sequencing for the first drop

1. ~~**Scaffold `brand/`, populate `brand/models/M01..M10/source/`, draft per-model `profile.md`**~~ — done 2026-05-19. See CLAUDE.md §17.2.
2. ~~**Install ai-toolkit**~~ — done 2026-05-19 at `C:\Users\Yoshii\Documents\ai-toolkit\` with Python 3.12.11 venv (matches ComfyUI's uv-managed Python). torch 2.9.1+cu128, CUDA enabled. Per-slot training configs rendered to `configs/ai_toolkit/cache_face_m##_qwen_12gb.yaml`.
3. **Workflow — Tier 2 face bootstrap (next):** build a Qwen Image Edit + InstantX-ControlNet-pose pipeline that generates 20–30 variations per model from the single source portrait. Save to `brand/models/M##/training_set/`. This is a *utility* workflow, not one of the eight production workflows gated in CLAUDE.md §17.3 — design first, then JSON.
4. **Workflow — garment bootstrap (C2/C3/C4 training data):** extract individual garments from `brand/lookbook/core_*.png` lookbook plates and recompose as floating-garment studio mockups. Render each garment on BOTH backdrops — `#0A0A0A` off-black and `#FAFAF7` bone — so the resulting LoRA carries reflective/stealth physics under either lighting register. Save to `brand/garments/<collection>/training_set/{offblack,bone}/`.
5. **Train face LoRAs:** `python run.py configs/ai_toolkit/cache_face_m##_qwen_12gb.yaml` per active slot. Output safetensors land in `outputs/loras/faces/`, then promote to `ComfyUI/models/loras/cache/c1_faces/cache_face_m##.safetensors`.
6. **Train garment LoRAs:** `python run.py configs/ai_toolkit/cache_garment_<collection>_qwen_12gb.yaml` for each of `lightware`, `dailyware`, `darkware`. Promote to `ComfyUI/models/loras/cache/c2_lightware/`, `c3_dailyware/`, `c4_darkware/` respectively.
7. **Workflow — Tier 1 garment swap:** `03_garment_inpaint_qwen_edit.json`. Produces near-term campaign stills by swapping garments on the source portraits — does not need face or garment LoRAs (uses Qwen Image Edit directly).
8. **Workflow — Tier 2 inference:** standard Qwen Image + face-LoRA + garment-LoRA workflow for novel scenes (`01_hero_still_qwen.json`, `02_lookbook_lineup_qwen.json`).
9. **Workflow — Tier 3 lineup plate:** stack face + garment LoRAs per figure, then composite. No `cache_core_*` LoRA — lineup framing is a compositing concern, not a learned behaviour.

---

## Current cast (post-2026-05-21 resolution)

Active roster — **10 identities**. Visual review on 2026-05-19 reconciled the
original flagged duplicates: M01/M03 confirmed same East Asian woman in two
fits (original M03 slot retired, merged into M01); M02/M05 confirmed distinct.
On 2026-05-21 the M03 slot was reactivated with a new, independent identity
(Mixed Race woman, natural curves, natural curly hair) so the slot is no
longer a permanent hole.

| Slot | Visual descriptor | Garment in source |
|---|---|---|
| M01 | East Asian woman, long straight black hair | cropped hoodie + sweatpants (Lightware) — secondary angle (`source/portrait_b.jpg`, former M03 portrait): puffer vest + crewneck + cargo + boots (Darkware-lite) |
| M02 | Black man, lean build, sharp jaw, very short hair | oversized tee + cargo + slip-ons (Dailyware) |
| M03 | **Mixed Race (Black/White) woman**, natural curves, natural curly hair | *tbd — assigned on portrait intake* |
| M04 | White man, medium wavy brown hair | oversized hoodie + sweatpants (Dailyware) |
| M05 | Black man, athletic build, rounder face, close crop | full puffer parka + cargo + sneakers (Darkware) |
| M06 | White woman, brown chin-length bob, centre-parted | oversized tee + wide cargo + sneakers (Dailyware) |
| M07 | Black woman, natural afro | track jacket + tank + wide sweatpants (Lightware) |
| M08 | White woman, long brown hair, ski goggles on forehead | cropped sweatshirt + wide sweatpants (Darkware accessory) |
| M09 | White man, buzzed blond, sharp jaw | puffer vest + hoodie + jogger + trainers (Darkware-lite) |
| M10 | Mixed / Latino man, short curly black hair | hoodie + cargo + slip-ons (Dailyware) |

Slot numbering is **append-only by default**. The 2026-05-21 M03 reactivation
is an explicit exception, permitted because no LoRA had been trained against
the original retired identity. Once a `cache_face_m##.safetensors` has been
promoted, the slot is locked — future cast additions go to M11+. M03 is
blocked on a fresh source portrait (Mixed Race woman) from the operator
before bootstrap + LoRA training can run for that slot. Codename assignment
per slot (`OPERATOR_A`, `CACHE_07`, etc.) is non-blocking for LoRA training.

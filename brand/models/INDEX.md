# Caché — Cast Index

> Roster of the consistent models that anchor every Caché campaign. Each slot is
> a separate identity to be locked via per-model character LoRA
> (`cache_face_m##.safetensors`). See `.claude/consistency_pipeline.md` for the
> three-tier strategy.

| Slot | Codename | Visual descriptor | Source garment in portrait | LoRA status |
|---|---|---|---|---|
| M01 | _tbd_ | East Asian woman, long straight black hair | Cropped hoodie + black sweatpants (Lightware/Dailyware) | training set ready |
| M02 | _tbd_ | Black man, lean build, sharp jaw, very short hair | Oversized black tee + cargo pants + slip-ons (Dailyware) | training set ready |
| M03 | _tbd_ | Mixed Race (Black/White) woman, natural curves, natural curly hair | _tbd_ — assigned on portrait intake | blocked on source portrait |
| M04 | _tbd_ | White man, medium wavy brown hair | Oversized hoodie + sweatpants (Dailyware) | training set ready |
| M05 | _tbd_ | Black man, athletic build, rounder face, close crop | Full puffer parka + cargo pants + sneakers (Darkware) | training set ready |
| M06 | _tbd_ | White / mixed woman, brown chin-length hair | Oversized tee + cargo pants (Dailyware) | training set ready |
| M07 | _tbd_ | Black woman, afro | Track jacket + tank + wide sweatpants (Lightware) | training set ready |
| M08 | _tbd_ | White woman, long brown hair, ski goggles on head | Cropped sweater + wide sweatpants (Darkware accessory) | training set ready |
| M09 | _tbd_ | White man, buzzed blond, sharp jaw | Puffer vest + hoodie + jogger (Darkware-lite) | training set ready |
| M10 | _tbd_ | Mixed / Latino man, short curly black hair | Hoodie + cargo pants (Dailyware) | training set ready |

## Cast resolution history

- **2026-05-19** — visual review of all 10 source portraits. **M01 ≡ original M03**
  (same East Asian woman). Original M03 slot retired; portrait kept in place as
  a secondary angle for M01.
- **2026-05-21** — **M03 slot reactivated** with a new identity: Mixed Race
  (Black/White) woman, natural curves, natural curly hair. The prior M03
  portrait (East Asian woman, Winter-lite fit) was relocated to
  `brand/models/M01/source/portrait_b.jpg`. M03 awaits a fresh source portrait
  from the operator before bootstrap + LoRA training can run for the slot.
- **M02 ≠ M05** — distinct Black male models. M02 is taller, slimmer build,
  sharper jaw; M05 has athletic build, rounder face, different cheekbone /
  nose structure. Both kept.

## Active roster: 10 identities (M01–M10)

Slot numbering convention: append-only by default. The 2026-05-21 M03
reactivation is an explicit exception, not a precedent — future new cast
members start at M11, never recycling a slot that was retired *after*
LoRAs were promoted. M03 was reusable because no LoRA had been trained
against the retired identity.

## Open questions for the operator

- **M03 source portrait** — drop a full-body or three-quarter portrait into
  `brand/models/M03/source/portrait.jpg` matching the descriptor (Mixed Race
  woman, natural curves, natural curly hair) so the bootstrap can run.
- **Codenames** — assign internal codenames in each `profile.md`. Use neutral
  protocol-style handles (`OPERATOR_A`, `CACHE_07`, etc.) rather than real
  names, in keeping with the stealth-wealth brand voice.

## File layout per model

```
brand/models/M##/
├── profile.md             # name, descriptors, training status
├── source/
│   └── portrait.jpg       # canonical source shot from consistent_models/
│   └── portrait_b.jpg     # optional second angle (M01 only — relocated from M03)
├── training_set/          # populated by scripts/bootstrap_faces.py
│   ├── v01_full_..._00001_.png
│   ├── v01_full_..._00001_.txt   # caption sits next to the image (ai-toolkit reads by stem)
│   ├── v02_full_..._00001_.png
│   ├── v02_full_..._00001_.txt
│   └── ...
└── captions/              # optional: hand-curated override captions (vestigial)
```

ai-toolkit's `caption_ext: "txt"` makes it read `<stem>.txt` from the same
`folder_path` as the images. The bootstrap orchestrator writes the caption
inline at fetch time, so `training_set/` is self-contained. The sibling
`captions/` folder is retained for hand-edited overrides but is not read
by the trainer.

## LoRA output target

Per-model LoRAs land in `ComfyUI/models/loras/cache/c1_faces/cache_face_m##.safetensors`.

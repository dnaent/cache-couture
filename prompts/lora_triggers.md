# Caché LoRA triggers

The LoRA registry is organised into four asset classes plus a utility folder.
See `ComfyUI/models/loras/cache/README.md` for full directory layout and
`CLAUDE.md` §11.3 + §16.4 for stacking precedence.

## C1 — Faces (per-identity)

| Slot | File | Trigger |
|---|---|---|
| M01 | `c1_faces/cache_face_m01.safetensors` | `m01_face` |
| M02 | `c1_faces/cache_face_m02.safetensors` | `m02_face` |
| M04 | `c1_faces/cache_face_m04.safetensors` | `m04_face` |
| M05 | `c1_faces/cache_face_m05.safetensors` | `m05_face` |
| M06 | `c1_faces/cache_face_m06.safetensors` | `m06_face` |
| M07 | `c1_faces/cache_face_m07.safetensors` | `m07_face` |
| M08 | `c1_faces/cache_face_m08.safetensors` | `m08_face` |
| M09 | `c1_faces/cache_face_m09.safetensors` | `m09_face` |
| M10 | `c1_faces/cache_face_m10.safetensors` | `m10_face` |

M03 retired (merged into M01). Strength: **0.85 – 1.0** (never below 0.75).

## C2/C3/C4 — Collection garments

| Class | Collection | File | Trigger |
|---|---|---|---|
| C2 | Lightware | `c2_lightware/cache_garment_lightware.safetensors` | `lightware_set` |
| C3 | Dailyware | `c3_dailyware/cache_garment_dailyware.safetensors` | `dailyware_set` |
| C4 | Darkware | `c4_darkware/cache_garment_darkware.safetensors` | `darkware_set` |

Strength: **0.6 – 0.85**.

## Utility

| File | Trigger | Purpose |
|---|---|---|
| `utility/cache_chip.safetensors` | `cache_chip` | Microchip symbol mark on labels |

Strength: **0.5 – 0.7**, optional — only on assets requiring chip-mark insertion.

## Backdrop — prompt fragment, not LoRA

- Off-black: `on off-black seamless backdrop` (`#0A0A0A`) — stealth / reflective macro
- Bone: `on warm bone seamless backdrop` (`#FAFAF7`) — canonical lookbook register

Garment LoRAs are trained on both backdrops so reflective physics travel with the garment.

## Deprecated — do not use

`cache_brand`, `cache_core_light`, `cache_core_daily`, `cache_core_winter`.
Replaced by the C1+C2/C3/C4 architecture. See `ComfyUI/models/loras/cache/README.md`
for the rationale.

# M03 — Profile

| Field | Value |
|---|---|
| Codename | _tbd_ |
| Real name (internal only) | _tbd_ |
| Pronouns | she/her |
| Apparent ethnicity | Mixed Race (Black / White) |
| Hair (in source) | Natural curls, voluminous medium-length coils, centre-parted |
| Build | Natural curves, soft hourglass |
| Distinguishing features | _tbd_ |
| Source portrait | `source/portrait.jpg` (synthesised via Qwen Image t2i, 2026-05-21, seed 4102 — see `outputs/m03_candidates/m03_cand_02_00001_.png`) |
| Source garment | Cropped black technical hoodie + tailored black sweatpants (Cache Core — Lightware) |
| LoRA file (target) | `ComfyUI/models/loras/cache/c1_faces/cache_face_m03.safetensors` |
| LoRA trigger token | `m03_face` |
| LoRA training status | source ready; bootstrap pending |
| Training-set size (target) | 12 (bootstrap default; curate to ~6–8) |
| Notes | Slot reactivated 2026-05-21 with a new identity. The prior "M03 ≡ M01" portrait has been relocated to `M01/source/portrait_b.jpg` as a secondary angle for the East Asian woman; the M03 slot is now an independent Mixed Race woman, natural curves, natural curly hair. Source portrait was synthesised rather than operator-supplied — Qwen baked a small "Caché" text mark onto the pants (negative-prompt ignored); this will wash out during the bootstrap re-renders. |

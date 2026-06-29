# Canonical brand prompt fragments

## Global style prefix (all editorial / product renders)
```
editorial fashion photography, Caché Couture, stealth black streetwear,
matte premium fabrics, warm off-white seamless studio backdrop,
soft even diffused front fill, full body frontal stance, hands at sides,
neutral expression, frame from head to feet, no logos visible in background,
monochromatic palette, subtle reflective yarn highlights, gunmetal hardware,
ultra-detailed weave texture, 35mm, shot on Phase One, ISO 100, f/8,
crisp focus, magazine grade
```

## Tier material fragments (append the right one per garment; see CLAUDE.md §4)
Match fabric to the `-ware` tier — never render synthetics on a Dailyware cotton piece.

- **Dailyware tee:** `heavyweight 100% cotton single jersey, ~240gsm, garment-dyed deep black, soft matte hand, dense drape`
- **Dailyware tracksuit (hood + joggers):** `heavyweight brushed-back cotton loopback, ~400gsm, dense soft cotton fleece, matte, substantial weight`
- **Lightware tee/crop:** `lightweight cotton-modal jersey, ~190gsm, fluid drape, matte`
- **Lightware track jacket / shorts:** `matte peached nylon-taslan shell, lightweight technical, no sheen` (or `poly-elastane 4-way stretch knit, matte`)
- **Darkware puffer:** `matte recycled-nylon shell, clean baffled synthetic-fill puffer, stealth black, zero sheen, voluminous`
- **Darkware softshell / tech jacket:** `matte softshell bonded to micro-fleece, technical, gunmetal zips`
- **Darkware heavy fleece:** `dense poly polar-fleece / sherpa texture, matte`
- **Darkware utility cargo:** `matte cotton-nylon ripstop twill, utility pockets`
- **Accessory ski mask:** `fine merino wool knit balaclava, soft matte, ribbed`

## Value-signal fragments (reinforce premium feel)
```
gunmetal matte-black hardware, engraved zip pullers, deep non-fading black,
woven tonal chip-mark label small and off-centre, bound seams, ribbed cuffs,
black-out reflective yarn catching light only at glancing angle
```

## Homepage pillar macros (4-up Multicolumn)
Square 1:1, ~1200×1200, **identical framing + lighting on all four** for a cohesive row. Use the
global prefix + value-signal fragments. One macro per brand pillar (§1.3):
- **Stealth:** `extreme close-up, black sherpa balaclava, eyes only, matte, warm off-white seamless`
- **Utility:** `macro detail, matte cotton-nylon cargo pocket, gunmetal YKK zip pull, stealth black`
- **Encryption:** `macro, woven chip-mark embroidery on black weave, subtle reflective grey yarn flashing at a glancing angle`
- **Cachet:** `macro, small woven HIDDEN / APPROVAL label on a black garment, gunmetal tone, soft-focus background`

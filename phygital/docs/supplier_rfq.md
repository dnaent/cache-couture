# Caché Couture — Manufacturer RFQ / Outreach

> Supplier outreach + Request for Quote. Send to candidate OEM cut-and-sew factories.
> Two versions below: a short first-contact message and the full spec to attach once a
> supplier responds. Fill the `«…»` placeholders before sending.

---

## A. First-contact message (short — for Alibaba chat / email intro)

**Subject:** Private-label streetwear — OEM cut & sew, custom branding, small recurring batches

Hello,

We are Caché Couture (DNA Entertainment, UK), a high-end technical streetwear brand. We are
selecting a long-term OEM manufacturing partner for an apparel line built around custom
fabric, woven branding, and embedded NFC labels.

We are **not** looking for catalog/dropship product. We need true cut-and-sew to our spec,
with our own branding and packaging, produced in **small recurring batches** (made-to-
forecast, not bulk warehousing).

Before we share full tech packs, could you confirm whether you can support:

1. Custom cut-and-sew apparel (hoodies, puffer outerwear, joggers, tees) to our patterns.
2. **Woven-into-fabric** logo detail (not a sewn-on patch) and reflective-yarn embroidery.
3. Custom private-label inner labels, hang tags, and branded polybag/box packaging.
4. **NFC tag or QR insertion** into the inner label (or accepting brand-supplied NFC labels
   for you to sew in).
5. **Low MOQ** — target «50–150» units per style/colour, with repeat batches.
6. Per-order or per-batch fulfillment options (see Q&A in the full spec).

If yes to most of the above, we'd like to move to samples. Please also send your factory
profile, certifications, typical lead times, and MOQ tiers.

Thank you,
«Name» — Caché Couture
«email» · «website»

---

## B. Full RFQ spec (attach after first reply)

### B1. About the brand
Caché Couture is technical, stealth-luxury streetwear. Aesthetic: monochrome (stealth
black / off-black), matte technical fabrics, *subtle* reflectivity — never high-vis. The
brand signature is restraint: small, off-centre branding that rewards close inspection.

### B2. What we need (capabilities checklist)
Please answer **Yes / No / Partial** to each:

| # | Requirement | Y/N/Partial | Notes |
|---|---|---|---|
| 1 | Custom cut-and-sew from our patterns/tech packs | | |
| 2 | Fabrics: matte black weaves, sherpa/bouclé fleece, nylon ripstop, softshell | | |
| 3 | Reflective/black-out reflective yarn embroidery | | |
| 4 | **Woven-in** logo (microchip glyph) — woven into fabric, not appliqué patch | | |
| 5 | Gunmetal custom hardware (zip pulls, engraved plates) | | |
| 6 | Tonal/reflective embroidered wordmark labels (small, off-centre) | | |
| 7 | Custom inner labels, hang tags, branded polybag / box | | |
| 8 | NFC chip insertion into inner label **or** sew-in of brand-supplied NFC labels | | |
| 9 | QR-encoded tag alternative if NFC not feasible | | |
| 10 | Low MOQ per style/colour («50–150») with repeat batches | | |
| 11 | Pre-production sampling (paid samples accepted) | | |
| 12 | Per-order fulfillment / blind dropship **or** batch ship to a 3PL | | |

### B3. Initial styles (indicative — full tech packs on request)
- **Lightware:** essential tees, track jackets, tailored sweatpants, lightweight balaclavas.
- **Dailyware:** oversized cotton tees, cotton hoodies, half-zip pullovers, joggers, cargos.
- **Darkware:** hooded puffer jackets, longline puffers, puffer gilets, heavy fleece
  quarter-zips, utility cargo trousers.

### B4. Branding placement (critical — woven chip mark)
The microchip logo is **woven directly into the garment fabric**, small and off-centre, at
four canonical positions:
1. Back of hood, centred below the crown seam.
2. Back-right trouser pocket.
3. Halfway up the right outer trouser leg.
4. Halfway up the left outer sleeve.

Finish: subtle reflective yarn that reads as a soft grey tonal whisper, flashing silver only
at a glancing light angle. **Never** stark white-on-black. A sparing engraved gunmetal plate
is acceptable where hardware reads better than embroidery.

### B5. Phygital / NFC requirement
Every garment carries an embedded **NFC chip or QR-encoded tag** in the inner label, tied to
a unique encrypted SKU. The NFC/QR must survive normal wear and washing. If you cannot embed
NFC, confirm you can sew in **brand-supplied** NFC labels at production.

### B6. Order & fulfillment model
Our model is **low recurring batches held at a fulfillment partner (3PL), shipped per
customer order** from our Shopify store. Please answer:
- **Q1.** Can you ship finished batches to a third-party 3PL/warehouse (UK/EU/US)?
- **Q2.** Do you offer per-order blind dropship (our branding, no factory paperwork)? At what
  unit-cost premium vs batch shipping?
- **Q3.** Do you expose an **order/fulfillment API** (or accept CSV/portal order feeds) so we
  can automate from Shopify? If so, please share the API docs.
- **Q4.** Lead times: first sample, bulk production, repeat batches.
- **Q5.** MOQ tiers and per-unit pricing at «50 / 100 / 250 / 500» units.

### B7. Information requested back
- Factory profile + certifications (e.g. BSCI, WRAP, OEKO-TEX, ISO).
- Sample policy and cost.
- Payment terms (deposit %, balance trigger).
- Standard packaging options + cost for custom packaging.
- References / existing brands served (NDA acceptable).

---

*Internal note:* maps to `phygital/CLAUDE.md` §2/§4 and root `CLAUDE.md` §3/§4/§4.1/§5.
Q3 (API/feed) determines how `app/alibaba.py::forward_order` is wired; Q1–Q2 confirm the
low-batch-stock + 3PL model.

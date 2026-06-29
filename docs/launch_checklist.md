# Caché — Launch Checklist

> Working checklist to get Caché from "storefront built, password on" to live + fulfilling.
> Related: `docs/shopify_migration.md` (store state), `phygital/CLAUDE.md` (fulfilment/sourcing),
> `phygital/docs/supplier_rfq.md` (full RFQ). Last updated 2026-06-29.

## 0. Where you are
Storefront, catalogue, collections, copy, policies (No-Apologies cleaned), and home-page brief are
done; store is **password-protected**. Remaining = sourcing + fulfilment + go-live. Two fulfilment
tracks: **POD** (Core/Gradient/Japan) and **OEM batch + 3PL** (Tag, masks, accessories).

---

## 1. Shopify apps (keep it lean — apps slow the store)
**Install:**
- [ ] **POD provider — pick ONE, prioritise UK fulfilment.** **Printful** (UK facility in Birmingham,
      embroidery, strong branding) or **Inkthreadable** (UK-native, sustainable). Apliiq has great
      streetwear blanks + woven neck labels but ships from the **US** (slower/pricier for UK orders).
      Decision test for any of them: ① heavyweight 100% cotton, ② embroidery, ③ custom neck label,
      ④ **UK fulfilment**. (Same provider can also do no-stock POD **socks**.)
- [ ] **Klaviyo** — email/SMS automation (welcome / abandoned-cart / post-purchase / win-back flows =
      passive revenue). Or start free with **Shopify Email**, upgrade later.
- [ ] **Your 3PL's app** — once a 3PL is chosen (this is the OEM order handoff).
- [ ] **Reviews** — Judge.me or Loox (social proof). Optional but high-value.

**Turn on:** **Shop** (Shop Pay accelerated checkout). **Native, no app:** Shopify Markets
(international), cookie-consent (Settings → Customer privacy), Search & Discovery (filters).

**Add once live (out of password):** **Google & YouTube** (free Google Shopping listings), **Pinterest**.

**Ignore — wrong model (these are dropshipping/arbitrage, not a branded line):** DSers,
Alibaba & AliExpress Dropship, CJdropshipping, Printify (aggregator, weak branding), Shopify
Marketplace Connect (dilutes a stealth-luxury brand).

- Phygital/NFT is **not an app** — it's your own service (`phygital/`), wired later.

---

## 2. POD track — Apliiq setup (Core / Gradient / Japan)
- [ ] Create Apliiq account, install the Shopify app, connect the store.
- [ ] Choose **heavyweight 100% cotton** blanks (tee ~240gsm; hoodie/jogger ~380–420gsm). Order **blank
      samples** to check hand-feel.
- [ ] Set decoration per collection: **embroidery** for the chip-mark/wordmark (tonal = Core; gradient
      thread = Gradient); **DTG** for Japan motifs. Order a **decorated sample**.
- [ ] Set up your **custom neck label** + pack-in slot (the NFT card goes here later).
- [ ] Upload artwork; map Apliiq products onto your existing Shopify products + variants (sizes).
- [ ] **Place a test order** — verify branding, quality, fulfilment, shipping before go-live.
- Apliiq auto-fulfils per order — no custom code on this track.

---

## 3. OEM track — sourcing cut-and-sew on Alibaba (Tag apparel + utility vest)
**How to source:**
- [ ] Search: "custom cut and sew hoodie OEM", "heavyweight cotton streetwear manufacturer", "custom
      tracksuit OEM low MOQ", "utility vest manufacturer".
- [ ] Filter to **Verified Supplier / Trade Assurance**, **Guangdong** (same province as your other
      suppliers), good response rate + years active.
- [ ] Shortlist (already researched, all Dongguan): **Groovecolor, Dongguan Metro, Jiayu, Yecheng, Pindon**.
- [ ] Message each with the opener (§3.2) + the **3 make-or-break questions** (§3.1).
- [ ] Order **paid samples** from the best 2–3. Check: fabric weight/hand, embroidery + print quality,
      label sew-in, fit/sizing.
- [ ] Vet: certifications (BSCI / WRAP / OEKO-TEX), MOQ, price tiers (50 / 100 / 250), lead times,
      payment terms. **Always pay via Trade Assurance** (escrow protection).
- [ ] Lock one. Then send the **Neon reflective label** swatch so they cost sewing it in.

### 3.1 The 3 make-or-break questions (ask EVERY candidate)
1. **Print method vs cotton** — can you embroider and/or **DTG / screen-print on 100% cotton**? We do
   **NOT** want polyester sublimation. (Reject sublimation-only suppliers.)
2. **Reflective woven labels + NFC** — will you sew in our **brand-supplied reflective woven labels**
   (from Dongguan Neon) and **brand-supplied NFC labels**?
3. **Order handoff** — do you offer a **per-order fulfilment API**, accept a **CSV/order feed**, or
   **ship batches to our 3PL**? (This decides how the store auto-links to fulfilment.)

### 3.2 Alibaba chat opener (paste this)
> Hello — we're a UK streetwear brand (Caché) sourcing a long-term cut-and-sew OEM partner for
> heavyweight 100% cotton apparel (hoodies, joggers, tees, utility vests), small recurring batches
> (MOQ ~50/style). Before samples, please confirm: (1) Can you decorate via embroidery and/or
> DTG/screen-print on 100% cotton? We do not want polyester sublimation. (2) Will you sew in our
> brand-supplied reflective woven labels and NFC labels? (3) For fulfilment — do you offer a per-order
> API, accept a CSV/order feed, or ship batches to our 3PL? Please also send your factory profile,
> certifications, MOQ tiers, lead times, and sample policy. Thank you.

Full spec to attach after their first reply: `phygital/docs/supplier_rfq.md`.

---

## 4. Accessories OEM (premium tier — batch + 3PL, all Guangdong)
| Accessory | Supplier type | Status |
|---|---|---|
| 2-in-1 masks, beanies | Knitwear OEM | ✅ Kangduo |
| Reflective woven labels | Trim supplier | ✅ Neon |
| Tag apparel + utility storage vests | Cut-and-sew apparel OEM | 🔍 sourcing (§3) |
| Duffle / messenger bags / pouches | Bag / luggage OEM | ❌ to source |
| Keyrings | Metal / promotional OEM (gunmetal, engraved) | ❌ to source |
| Socks | Sock OEM (or Printful POD) | ❌ to source |
- Source each specialist OEM the same way as §3 (Verified/Trade Assurance, Guangdong, samples, 3 Qs).
- All carry the reflective woven label where it fits → premium signature tier.

---

## 5. 3PL / fulfilment (the OEM order handoff)
- [ ] Choose a **UK/EU 3PL** to hold OEM + accessory batch stock and ship per Shopify order.
- [ ] Confirm it has a **Shopify integration** (auto order sync) — this *is* the order handoff for OEM.
- [ ] Ship OEM/accessory batches to the 3PL; load stock quantities.
- (Ask Claude to research UK 3PLs that handle apparel + small brands.)

---

## 6. Phygital / NFT (post-launch — Claude builds)
- [ ] Decide chain + commission/design the procedural NFT art + claim page.
- [ ] Claude builds the **generic-card claim/mint flow** + wires `forward_order`.
- [ ] Print the **premium NFT cards** (generic "claim" card) as pack-ins (POD provider pack-in + OEM 3PL insert).

---

## 7. Go-live (flip the switch)
- [ ] Confirm final **pricing**.
- [ ] Complete **policies** — fill placeholders (return/business address, VAT); write the real
      **Shipping policy** once a supplier/3PL is known.
- [ ] Switch **inventory to tracked** for OEM/3PL items (POD items stay untracked/auto).
- [ ] Finish the **home page** (hand the brief in `docs` to the Shopify agent) + add the **collection
      covers** (1600×2000) + link the **Phygital Ownership** page in the footer.
- [ ] **Test orders end-to-end** — one POD, one OEM — verify fulfilment + branding + the NFT card.
- [ ] **Remove the storefront password.** 🚀

---

## 8. What Claude does (your dev side)
- Wire **Shopify → OEM** (`phygital/app/alibaba.py::forward_order`) once OEM + 3PL + their handoff
  method are known.
- Build the **phygital NFT card** claim/mint flow when you switch it from "coming soon" to live.
- Research **3PLs** / draft supplier comms / tidy product data on request.

---

## 9. Self-sustaining wheel — steady-state operations
The end-state operating model. Once set up, these loops run with minimal intervention.

### Automated loops (zero-touch)
- **Order → fulfil → ship:**
  - *POD items* (Core / Gradient / Japan): Shopify → POD app (Printful/Inkthreadable) → decorate → ship.
  - *OEM items* (Tag / masks / accessories): Shopify → 3PL app → pick & pack (branded box + NFT card) → ship.
- **Phygital:** `orders/paid` webhook → phygital service mints the tethered NFT + records SKU ↔ token.
- **Marketing:** Klaviyo flows (welcome / abandoned-cart / post-purchase / win-back) fire on their own.
- **Checkout / payments / tax / returns:** Shopify + the POD/3PL handle these per policy.

### Human-in-the-loop (your role — by design, minimal)
- **OEM supplier conversations** — new pieces, quality, pricing, relationships. *Your main involvement.*
- **Batch reorders** — when an OEM/accessory item hits its **par level** at the 3PL, approve a reorder
  PO → OEM produces a batch → ships to the 3PL. POD items never need this (no stock).
- **Creative direction** — generate marketing / lookbook on the **3080 Ti / ComfyUI** (root `CLAUDE.md`
  §4/§8 + `prompts/library.md`); schedule social posts.
- **Light CS** — Shopify Inbox; most is automatable with saved replies + FAQ.

### The trigger that keeps the wheel turning
The **par-level reorder**. Track inventory on OEM items only → set low-stock alerts → a dip below par
pings you → you approve the batch PO. That single recurring action (plus supplier chats) is the whole
of your operational involvement. **Zero-touch:** POD fulfilment, phygital minting, marketing flows,
checkout.

### Cadence
Check the Shopify dashboard ~weekly; act on **reorder alerts** and **supplier threads** as they arrive.
Everything else turns by itself.

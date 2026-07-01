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
- [ ] **POD provider — DECISION: Printful** (chosen 2026-06-29). UK fulfilment (Wolverhampton) +
      international coverage (fits the universal/global positioning); broadest catalogue (apparel + POD
      socks/hats in one account); most reliable automation for a hands-off wheel; embroidery + custom
      neck labels. *Fallback:* **Inkthreadable** (UK-native, cheaper UK-only, eco) — only if going
      UK-only / marketing sustainability. Apliiq dropped (US fulfilment). **Before mapping all products:
      order ONE sample** (heavyweight 100% cotton tee + embroidered wordmark + custom neck label) to
      confirm hand-feel + embroidery quality. Same account also covers POD **socks**.
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

## 2. POD track — Printful setup (Core / Gradient / Japan)
- [ ] Create **Printful** account, install the Shopify app, connect the store.
- [ ] Choose **heavyweight 100% cotton** blanks. Tees are easy; **verify hoodies/joggers are 100% cotton**
      (most POD fleece is an 80/20 cotton-poly blend) — see the open decision below. Order **blank samples**.
- [ ] Set decoration: **embroidery** for the chip-mark/wordmark (tonal = Core); **Gradient wordmark = DTG**
      (embroidery can't do a smooth colour gradient); **DTG** for Japan motifs. Order a **decorated sample**.
- [ ] **Tracksuit = a Printful *bundle*** (hoodie + joggers as one Shopify product) — map as a bundle, not
      a single item, or the customer won't receive both pieces.
- [ ] Set up your **custom neck label** + pack-in slot (the NFT card goes here later).
- [ ] Upload artwork; map Printful products onto your existing Shopify products + variants (sizes).
- [ ] **Place a test order** — verify branding, quality, fulfilment before go-live.
- Printful auto-fulfils per order — no custom code on this track. Same account covers POD **socks**.
- **⚠ Open decision:** if you can't find a 100% cotton heavyweight hoodie/jogger you like → either accept a
  cotton-rich blend for POD tracksuits (soften copy to "heavyweight cotton") **or** move tracksuits to OEM.
  Tell Claude which and the product copy/metafields get updated to match.

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

## 4. Accessories OEM (premium tier — batch + 3PL; mostly Guangdong, socks = Zhejiang)
| Accessory | Supplier type | Status |
|---|---|---|
| 2-in-1 masks, beanies | Knitwear OEM | ✅ Kangduo |
| Reflective woven labels | Trim supplier | ✅ Neon |
| Tag apparel + utility storage vests | Cut-and-sew apparel OEM | 🔍 sourcing (§3) |
| Duffle / messenger bags / pouches | Bag / luggage OEM | 🔍 shortlisted (§4.1) |
| Keyrings | Metal / promotional OEM (gunmetal, engraved) | 🔍 shortlisted (§4.1) |
| Socks | **Printful POD** | ✅ decided |
- Source each specialist OEM the same way as §3 (Verified/Trade Assurance, samples, the 3 questions).
- All carry the reflective woven label where it fits → premium signature tier.

### 4.1 Candidate shortlist (researched 2026-07-01 — starting points to vet on Alibaba, not endorsements)
Verify each on Alibaba (**Verified Supplier / Trade Assurance**), request paid samples, and ask the **3
make-or-break questions (§3.1)** before committing. Pay via Trade Assurance.

**Bags — duffle / messenger / pouches (Guangdong):**
- **Jundong Factory** (Guangdong) — OEM/ODM travel/duffel bags, private-label, low MOQ.
- **Meyzy** — custom travel/duffle, MOQ ~50–300, fast sampling.
- **OSGW Bag** (Guangdong) — custom backpacks/duffels/organisers.
- General Alibaba messenger-bag OEMs run MOQ ~100–500. (Note: the luggage supply chain spans Guangdong + Hebei.)
- Sources: [Jundong](https://jundongfactory.com/custom-travel-bags/) · [Meyzy](https://www.meyzy.com/solutions/travel-bag-manufacturer/) · [OSGW](https://www.osgwbag.com/)

**Keyrings — metal / engraved (Guangdong):**
- **Guangzhou Mingou Metal Products Co., Ltd.** (Guangzhou) — OEM metal keychains.
- **Guangdong Jinyibao Arts & Crafts** (Shenzhen) — 20+ yrs metal keychains.
- **Shenzhen Longzhiyu Crafts Co., Ltd.** — high-capacity metal keychain factory.
- MOQ ~50 for basic **laser-engraving** (your gunmetal engraved keyring fits this band); 500+ only if a
  bespoke mould is needed.
- Sources: [Guangzhou Mingou](https://keychaincn.en.alibaba.com/) · [keychain roundup](https://www.leelinepromotion.com/keychain-manufacturers-in-china/)

**Socks — ✅ DECIDED: Printful POD** (2026-07-01). Kept on Printful (no separate supplier, no stock)
rather than a sock OEM — simplest, and the sock hub is Zhuji/Zhejiang anyway (outside Guangdong).
Revisit a Zhejiang sock OEM (e.g. **Zhuji Niumai**, MOQ ~20 pairs) only if you later want woven-branded
socks. Source if needed: [socks factory roundup](https://www.honouroceanshipping.com/top-20-china-socks-factory-socks-wholesale-manufacturers/)

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

---

## 10. Accounts & infrastructure (reference — set up 2026-06-30)
- **Email:** Google Workspace **user-alias domain** — `hiddencache.co.uk` added as an alias of the
  primary `dnaent.co.uk`. Brand address **`contact@hiddencache.co.uk`** (mirrors `contact@dnaent.co.uk`,
  same inbox; Gmail send-as enabled). Authenticated: **MX (Google 5-record set) + SPF + DKIM** — Gmail active.
- **DNS — all at Squarespace.** Both domains are registered/managed at Squarespace, so **every DNS
  record goes in the Squarespace DNS panel** (`Settings → Domains → hiddencache.co.uk → DNS`): email
  (MX/SPF/DKIM), the Shopify storefront, Shopify email-auth CNAMEs, and Klaviyo CNAMEs. Google Admin
  only *generates* the Google DKIM; it is *added* in Squarespace.
  - **Storefront records (do NOT touch):** `A @ → 23.227.38.65` and `CNAME www → shops.myshopify.com`.
- **Apps installed:** **Klaviyo** (email/SMS) · **Printful** (POD). Apliiq uninstalled.
- **Klaviyo config (2026-07-01):** sender `Caché` / `contact@hiddencache.co.uk`; Shopify integration
  connected. **Using Klaviyo's DEFAULT sending domain — NO branded sending domain** (deliberate: it's a
  volume optimisation, revisit at scale; avoids the NS-delegation complexity). Klaviyo auto-created
  **7 flows** (Welcome email + SMS, Abandoned Checkout, Browse Abandonment, Winback, Thank You,
  Post-Purchase) + **4 editorial campaign drafts** — all on-brand, awaiting customisation. Paste-ready
  flow/email copy in Caché voice: **`docs/klaviyo_flows.md`**. **Priority: build the waitlist signup
  form + Welcome flow now** (pre-launch list-building while password-protected).
- **Shopify transactional email:** authenticated via 6 Shopify CNAMEs (`*._domainkey`, `mailer*`) in
  Squarespace; sender `contact@hiddencache.co.uk`.
- **Policy URLs (branded, live at launch):** `hiddencache.co.uk` + `/policies/privacy-policy`,
  `/policies/terms-of-service`, `/policies/refund-policy`, `/policies/shipping-policy` (⚠ still the
  one-line placeholder — flesh out once dispatch times known), `/policies/contact-information`.
- **DNS rule:** every record (email, Shopify, future Klaviyo) goes in **Squarespace**; never touch the
  storefront `A @ → 23.227.38.65` / `CNAME www → shops.myshopify.com`.

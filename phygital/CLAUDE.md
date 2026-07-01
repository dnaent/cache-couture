# Caché Phygital Service — Context (CLAUDE.md)

> Scoped context for the `phygital/` FastAPI service. The repo-root `CLAUDE.md` is the
> brand source of truth (DNA, palette, materiality, phygital protocol §5). This file
> covers only the order → NFT → fulfillment service and the Shopify ↔ Alibaba/OEM path.
> Update it before changing the fulfillment model, supplier, or webhook contract.

---

## 1. Goal

Connect the Shopify store (**hiddencache.co.uk** / `hiddencache.myshopify.com`) to a
manufacturer so paid orders are produced and shipped on demand with Caché's own branding
and packaging — minimising up-front stock. Each paid order also mints its 1:1 tethered
NFT (CLAUDE.md §5).

Pipeline (implemented in `app/shopify_webhooks.py::handle_order_paid`):

```
Shopify orders/paid webhook
  → verify HMAC (X-Shopify-Hmac-Sha256)
  → for each Caché line item (has SKU): mint tethered NFT → persist Tether
  → forward_order(order)  → OEM supplier / 3PL fulfillment
```

---

## 2. Fulfillment Decision — Custom OEM (ratified 2026-06-27)

The operator chose the **custom OEM supplier** path over the generic Alibaba.com
Dropshipping app.

**Why generic dropship was rejected:** Caché's signature construction — woven chip mark,
reflective yarn, gunmetal hardware, embedded NFC label (root CLAUDE.md §4 / §4.1 / §5) —
cannot be produced by generic POD or catalog dropshipping. It needs real cut-and-sew with
milled fabric.

**Terminology correction:** there is **no "Alibaba official MCP app."** No Alibaba MCP
server is or was configured (active MCP: Shopify, Gmail, Google Calendar, Google Drive).
The integration is plain HTTPS: Shopify webhook → this service → supplier/3PL REST API.

### 2.1 Stock model — Low Batch Stock (ratified 2026-06-27)

True per-unit factory dropshipping of custom-branded garments effectively does not exist —
no factory cut-and-sews and ships one branded unit at a time. The operator has therefore
ratified the **Low Batch Stock** strategy:

```
Small recurring batch cut-and-sew (branded, NFC, custom packaging), made to forecast
  → branded stock held at a 3PL / fulfillment partner (no storefront inventory)
  → per-order pick & ship triggered by Shopify orders/paid
```

"Zero stock" is explicitly **not** the target for signature apparel. The win is **low,
made-to-forecast batch stock at a 3PL, no retail storefront inventory, and automated
per-order fulfillment.** A true zero-stock dropship track remains viable only for low-value
unbranded **accessories** (optional hybrid: generic Alibaba dropship app for those).

Target batch sizes: ~50–150 units per style/colour, repeat batches (see RFQ §B6).

### 2.2 POD / OEM split + sourcing progress (2026-06-29)

The reflective woven label (mirrored `CACHÉ` / `HIDDEN / APPROVAL`, §2.1 device, half black-satin /
half reflective silver) is a **non-negotiable brand signature**. POD providers cannot sew in a
third-party reflective woven label, so any product carrying it must be OEM. Resulting split:

- **POD track (Apliiq / Printful — Shopify-native, per-order, no custom code):** Core, Gradient, and
  **Japan** (motifs as DTG placement prints on heavyweight 100% cotton blanks). Decoration-on-blank;
  accepts printed-not-woven motif as the accessible-tier compromise.
- **OEM track (custom cut-and-sew, low batch + 3PL or order API):** **Tag Collection** + the
  **2-in-1 convertible mask** — these carry the reflective woven tag + (mask) merino + NFC.

**Decoration by tier — Option B, LOCKED 2026-06-29:** reflective embroidery + the reflective woven
label are the **Tag/mask top-tier signature only**. **Core / Gradient / Japan use NON-reflective
decoration** so they stay POD: Core = tonal embroidered chip-mark; Gradient = gradient-thread
embroidered wordmark; Japan = **DTG-printed** motifs + tonal-embroidered CACHÉ branding. (Operator
originally specced screen-print for Japan motifs; defaulted to **DTG** to keep Japan POD — switching
Japan motifs back to screen-print would move Japan to the OEM batch track.)

**Phygital delivery (revised 2026-06-29):** moved from woven-chip / NFC-in-garment to a
**procedurally-generated NFT card** included with every order (POD + OEM alike) — decouples phygital
from manufacturing so every garment carries it. Recommended mechanism: a generic premium "claim"
card (QR) + server-side per-order NFT tethered to the SKU (the service already maps SKU→token);
uniqueness is digital, not per-card. (Woven chip-mark + reflective label become a Tag/mask-tier detail.)

**Sourced suppliers (operator, 2026-06-29):**
- **Dongguan Kangduo Clothing Co., Ltd.** — **knitwear only**: merino brushed 2-in-1 mask (+ knitted
  beanies if added). Cannot do cut-and-sew apparel.
- **Dongguan Neon Garment Accessories Co., Ltd.** — reflective woven labels (Tag/mask tier).
- **Cut-and-sew apparel OEM — STILL TO SOURCE** — makes the Tag hoodie/joggers/tees and sews in
  Neon's labels. Needs: heavyweight 100% cotton, accepts brand-supplied reflective labels, low MOQ.
- Flow: Neon produces labels → ships to each garment maker (Kangduo + apparel OEM) → sewn in.
- **Accessories (premium OEM tier, all Guangdong, batch + 3PL):** keyrings (metal OEM), duffle / messenger
  bags / pouches (bag/luggage OEM), utility storage vests (cut-and-sew apparel OEM). **Socks = Printful POD
  (decided 2026-07-01), not OEM.** Lighters dropped (hazmat shipping). Full table + sourcing steps +
  candidate shortlist: `docs/launch_checklist.md` §4.

**Status of open items:**
1. ✅ Reflective label scope = **Tag/mask premium tier only**; Core/Gradient/Japan use standard
   (non-reflective) neck labels → **POD stays on** for those.
2. ⚠️ **Source a cut-and-sew apparel OEM** for the Tag apparel (Kangduo is knitwear only).
3. ⏳ **Order handoff (RFQ Q3):** does each OEM/3PL expose a per-order API or accept a CSV/feed? That
   answer is what `forward_order` (`app/alibaba.py`) gets wired to. POD track needs no wiring.

---

## 3. Current State (2026-06-27)

| Component | File | Status |
|---|---|---|
| FastAPI entrypoint, `/health`, webhook route, `/tethers/{sku}` | `app/main.py` | Implemented |
| Shopify HMAC verify + orders/paid handler | `app/shopify_webhooks.py` | Implemented (real HMAC) |
| NFT mint | `app/nft.py` | Stub — fill once chain/contract chosen |
| Tether persistence | `app/store.py` | In-memory dev store; Firestore TODO |
| Supplier fulfillment adapter | `app/alibaba.py` | **Generic OEM REST adapter (template)** |
| Config / env | `app/config.py`, `.env.example` | Implemented |

`forward_order` is a **no-op** until `ALIBABA_API_BASE` is set (plumbing-only). When set,
it builds a vendor-neutral payload, signs it (HMAC-SHA256 over `timestamp.body`), and
POSTs to `<base>/orders`. Field names and the signing scheme are placeholders — remap
`_build_payload` and `_sign` to the real supplier/3PL contract once locked.

---

## 4. Outstanding (in order)

1. **Lock a supplier/3PL** (operator-led research, in progress). Custom cut-and-sew
   streetwear factory able to do private-label woven labels, custom polybag/hang-tag
   packaging, and — ideally — NFC label insertion. Confirm how per-order fulfillment is
   triggered: their own order API, a 3PL API, or manual CSV/portal. Outreach RFQ ready at
   `phygital/docs/supplier_rfq.md` — send to candidates; Q3 answer determines API wiring.
2. **Remap `app/alibaba.py`** `_build_payload` / `_sign` / endpoint to the locked API.
3. **Decide NFC sourcing.** If the factory can't embed NFC, source NFC inner labels
   separately and have the 3PL apply at pick-pack, or pre-batch.
4. **Implement NFT mint** (`app/nft.py`) — chain/contract/RPC selection (root §5).
5. **Swap in Firestore** for `app/store.py` (`GCP_PROJECT=cache-couture`,
   `FIRESTORE_COLLECTION=phygital_tethers`).
6. **Deploy + register webhook** — topic `orders/paid`, JSON, URL
   `https://<host>/webhooks/shopify/orders-paid`; set `SHOPIFY_WEBHOOK_SECRET`.
7. **(Optional) Hybrid accessories track** — generic Alibaba.com Dropshipping app in
   Shopify for unbranded low-value items; those line items would carry no Caché SKU and
   are skipped by `forward_order`.

---

## 5. Run / Test (dev)

```bash
cd phygital
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # fill SHOPIFY_WEBHOOK_SECRET (+ supplier creds when ready)
uvicorn app.main:app --reload --port 8090
```

Health: `GET /health`. With `ALIBABA_API_BASE` unset, the pipeline runs end-to-end and
fulfillment cleanly reports `{"forwarded": false, "reason": "supplier_not_configured"}`.

---

## 6. Conventions

- Only line items with a `sku` are treated as Caché items (minted + forwarded). Untracked
  items are skipped — see `handle_order_paid` and `_build_payload`.
- Buyer wallet for the NFT is read from order `note_attributes` (`wallet` /
  `wallet_address`); absent → mint to custody and transfer later.
- Secrets live in `.env` only (gitignored). Never commit real Shopify/supplier/mint keys.
- Brand voice + materiality rules in root `CLAUDE.md` govern any customer-facing copy or
  packaging spec generated here.

---

*End of phygital/CLAUDE.md*

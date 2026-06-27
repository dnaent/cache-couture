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

# Caché Shopify Storefront — Migration Context

> Context for the Shopify store **Caché** (`hiddencache.co.uk` / `no-apologies-5.myshopify.com`,
> Dawn theme, Basic plan, GBP). Records the 2026-06-27 rebrand from the previous **No Apologies**
> brand to Caché. Update this when products, collections, pricing, or go-live state change.
> Related: [phygital/CLAUDE.md](../phygital/CLAUDE.md) (fulfillment), root `CLAUDE.md` (brand DNA).

> **STATUS (2026-06-29): Store admin + design COMPLETE.** Catalogue (13 active products: tees +
> full tracksuits + 2-in-1 convertible masks), collections/tiers/menu, on-brand copy, materials
> spec (100% heavyweight cotton / merino), collection covers, de-branded policies, and the home-page
> brief (`§ home-page build brief` handed to the Shopify agent) are all done. Storefront is
> **password-protected** pending fulfilment. **Remaining = NOT storefront work:** (1) source + lock an
> Alibaba OEM/3PL supplier, (2) wire Shopify orders → supplier via `phygital/app/alibaba.py`
> `forward_order` once that supplier exposes an order API/feed, (3) switch inventory to **tracked** +
> flip off the password to go live. Marketing/LoRA training handed to the ComfyUI (3080 Ti) machine —
> see root `CLAUDE.md` §4/§8 + `prompts/library.md`.

---

## 1. What happened (2026-06-27, autonomous session)

Replaced the previous **No Apologies** catalogue with the Caché range from `/shopify` designs,
keeping the existing theme/layout untouched (text + products only). Store name was already "Caché".

- **Backup:** old store state saved to `docs/shopify_store_backup_2026-06-27.json` before changes.
- **20 Caché products created** (all `vendor: Caché`, status **DRAFT**) — auto-join the smart
  collections by title/tag/type. See §3. (The single "Tag Mask" was later split into two standalone
  products — **Ski Mask Black** and **Ski Mask Blue** — so Accessories reads as two items.)
- **10 No Apologies products ARCHIVED** (reversible; data retained, removed from storefront).

### 1.1 Collection architecture (final 2026-06-27 — CLAUDE.md `-ware` tiers)

All collections are **smart** (auto-populated). The store now follows the **Lightware / Dailyware /
Darkware** tier system from root `CLAUDE.md` §3, alongside design-line and type collections.

**Design-line collections** (these hold the current range; every product in them is **Dailyware**):

| Collection | GID (Collection/…) | Handle | Rule | Count |
|---|---|---|---|---|
| Core Collection | 434617745729 | `definition` | TITLE starts with "Core" | 3 |
| Gradient Collection | 656391635265 | `gradient-collection` | TITLE starts with "Gradient" | 3 |
| Japan Collection | 434619416897 | `graffiti` | TITLE starts with "Japan" | 9 |
| Tag Collection | 434619908417 | `staple` | TITLE starts with "Tag" | 3 |

**Tier collections** (empty placeholders for future tier-specific designs):

| Collection | GID | Handle | Rule | Count |
|---|---|---|---|---|
| Lightware | 656391700801 | `lightware` | TAG = "Lightware" | 0 |
| Darkware | 656391864641 | `darkware` | TAG = "Darkware" | 0 |

**Type / utility collections:**

| Collection | GID | Handle | Rule | Count |
|---|---|---|---|---|
| Tracksuits | 434873598273 | `tracksuits` | TYPE = "Tracksuit" | 11 |
| T-Shirts | 434874057025 | `t-shirts` | TYPE = "T-Shirt" | 8 |
| Accessories | 434879725889 | `accessories` | TAG = "Accessories" | 2 (ski masks) |

**Tier logic (per operator + CLAUDE.md §3):**
- **Dailyware** — the entire current range (Core/Gradient/Japan/Tag). Stated in each product's
  description and carried as a `Dailyware` tag. **No standalone Dailyware collection** — these pieces
  live in their own design-line collections.
- **Lightware** (§3.1, sleek lightweight: track jackets, essential tees, sweatpants, technical
  shorts) and **Darkware** (§3.3, strict heavy outerwear: puffers, gilets, heavy fleece, utility
  cargos) — renamed from the former Summer/Outerwear collections. **Intentionally empty**; populate
  by tagging a product `Lightware` / `Darkware` once those designs exist. Do not back-fill with the
  current Dailyware pieces.
- The former **Winter Collection was deleted.** Gradient was split out of Core (retitled
  `Core Gradient X` → `Gradient X`).

### 1.2 Header navigation menu

Live header is the **"Caché Menu"** (`home-menu`, Menu/212625785153). Final order:
`Home · Collections · Tracksuits · T-Shirts · Darkware · Lightware · Accessories · Search · Contact`.
("Items" → "Darkware"; new "Lightware" item added; both point at the renamed tier collections.)

## 2. KNOWN GAP — product images not attached (environment blocker)

The designs in `/shopify` are **not yet on the products.** Shopify needs public HTTPS image URLs;
the local PNGs must be uploaded to Shopify's CDN first. In this session that was impossible:
- No `upload-image` MCP tool is exposed to this client.
- Staged-upload + `productCreateMedia` works via GraphQL, **but** pushing the bytes needs outbound
  HTTPS to Google Cloud Storage, and this environment's shell has **no internet egress** (all
  hosts time out).

**To finish images,** use `docs/shopify_image_manifest.json` (maps every local file → product →
front/back/variant). Options, easiest first:
1. Enable the Shopify `upload-image` MCP tool in the client, then a Claude session attaches all
   images per the manifest in one pass.
2. Run the staged-upload pipeline from a machine **with** internet (e.g. the Windows box): for each
   file `stagedUploadsCreate` → POST bytes to the returned GCS URL → `productCreateMedia` with the
   `resourceUrl`. (The GraphQL half already works here; only the byte-push was blocked.)
3. Manual: drag-drop each file onto its product in Shopify admin, guided by the manifest.

## 3. Product catalogue (19 products, all DRAFT)

SKU scheme: `CACHE-<LINE>-<TYPE>-<COLOUR>-<SIZE>` (feeds the phygital SKU→NFT pipeline, root §5).
Sizes S/M/L/XL for apparel; masks One Size. Prices are **provisional** (see §4).

| Product | GID (Product/…) | Type | Variants | Price |
|---|---|---|---|---|
| Core Tee | 10295709991233 | T-Shirt | Black, White | £40 |
| Gradient Tee | 10295710089537 | T-Shirt | Blue/Green/Red ± Black | £40 |
| Core Tracksuit | 10295710155073 | Tracksuit | Black, Grey, Navy | £160 |
| Gradient Tracksuit | 10295710253377 | Tracksuit | Black, Blue, Green, Red | £160 |
| Core Bottoms | 10295710187841 | Bottoms | Black, Grey, Navy | £75 |
| Gradient Bottoms | 10295710286145 | Bottoms | Black, Blue, Green, Red | £75 |
| Japan Sun Tee | 10295710318913 | T-Shirt | White, Black | £40 |
| Japan Sun Tracksuit | 10295710384449 | Tracksuit | Black | £160 |
| Japan Sun Bottoms | 10295710449985 | Bottoms | Black | £75 |
| Japan Wave Tracksuit | 10295710482753 | Tracksuit | Blue | £160 |
| Japan Wave Bottoms | 10295710515521 | Bottoms | Blue | £75 |
| Japan Bamboo Tracksuit | 10295710548289 | Tracksuit | Black | £160 |
| Japan Bamboo Bottoms | 10295710581057 | Bottoms | Black | £75 |
| Japan Cherry Tracksuit | 10295710646593 | Tracksuit | Black | £160 |
| Japan Cherry Bottoms | 10295710679361 | Bottoms | Black | £75 |
| Tag Hoodie | 10295710744897 | Hoodie | Black | £90 |
| Tag Bottoms | 10295710810433 | Bottoms | Black | £75 |
| Tag Tee | 10295710843201 | T-Shirt | Black, White | £40 |
| Ski Mask Black | 10295750787393 | Mask | One Size | £30 |
| Ski Mask Blue | 10295750820161 | Mask | One Size | £30 |

## 4. Decisions & assumptions (please confirm)

- **Status = DRAFT, not ACTIVE.** No supplier/fulfillment is locked yet and pricing needs sign-off,
  so nothing is on the live storefront. Going live = flip products to ACTIVE (one bulk action) once
  ready. The storefront is intentionally empty of products until then.
- **Pricing is provisional** — flat by type (Tee £40, Hoodie £90, Bottoms £75, Tracksuit £160,
  Mask £30), loosely mirroring the old store (Tee £35 / Tracksuit £160 / Mask £30). Adjust freely.
- **Taxonomy = CLAUDE.md §3 `-ware` tiers** (see §1.1): current range = **Dailyware** (in
  descriptions + `Dailyware` tag), organised by design line (Core/Gradient/Japan/Tag). **Lightware**
  and **Darkware** are empty tier collections for future designs; **Accessories** holds the ski masks.
- **Gradient SKUs** still carry the `CACHE-CORE-G*` prefix (e.g. `CACHE-CORE-GTEE-BLU-M`) from before
  the line was split out of Core. SKUs are internal + unique, so left as-is; rename to `CACHE-GRAD-*`
  later if you want the prefix to match the line. Titles/tags/collections are all correct.
- **Empty by design:** Lightware + Darkware have **0 products** on purpose — populate by tagging a
  product `Lightware` / `Darkware` when tier-specific designs (shorts/track tops; puffers/jackets/
  fleece) exist. Do not back-fill them with the current Dailyware pieces. **Accessories** = 2 ski
  masks; ready for keyrings, lighters, beanies, duffle / messenger bags, socks (tag each `Accessories`).
- **Colourways as variants** (one product per garment, colour as an option) rather than one product
  per colourway. Cleaner than the old store; theme handles it.
- **Collection handles unchanged** (`definition`/`graffiti`/`staple`) to avoid breaking theme menu
  links — only titles/rules/descriptions changed. URLs are cosmetically stale; rename handles later
  if wanted (will need theme menu links updated to match).
- **Inventory untracked** (0, no tracking) — aligns with Low Batch Stock once a 3PL is set.

## 5. Outstanding

1. **Attach product images** — see §2 + manifest. Highest priority; the store is visually empty
   without them.
2. **Collection cover images** — still the old No Apologies covers (same upload blocker). Replace
   with 9 Caché covers (Core, Gradient, Japan, Tag, Lightware, Darkware, Accessories, Tracksuits,
   T-Shirts). **Dimensions: see §6.** Operator designing these (2026-06-27).
3. **Confirm pricing**, then **flip DRAFT → ACTIVE** to go live.
4. **Theme section text** (homepage hero copy, about, footer, announcement bar) — could not be
   edited via the Shopify MCP (no theme-content tools exposed for the live theme). Any remaining
   "No Apologies" wording in theme sections must be changed in the Shopify theme editor.
5. **Optional:** dedicated Bottoms / Hoodies collections (the range now has many; old store had none).

## 6. Theme & collection cover image spec

**Live theme: Dawn** (`OnlineStoreTheme/139206525249`, role MAIN). Verified from theme files 2026-06-27.

**Where collection covers appear:** ONLY on the `/collections` grid (the "Collections" menu link),
via the `main-list-collections` section. The collection-page **banner is disabled**
(`main-collection-banner` → `disabled: true`, `show_collection_image: false`), so no wide hero/banner
version of the cover is needed.

**Grid behaviour:** `main-list-collections` is set to **`image_ratio: "adapt"`**, 3 columns desktop.
"Adapt" = each card takes its image's **own** aspect ratio with **no cropping**. Consequence: design
**all 9 covers to the same aspect ratio** (or grid rows go uneven), full-bleed (no safe margins needed).

**Recommended dimensions** (pick one ratio, apply to all 9):
- Editorial: **4:5 portrait → 1600 × 2000 px** (recommended).
- Uniform/simple: **1:1 square → 1600 × 1600 px**.

1600 px on the wide edge covers Dawn's max page width (1600) at retina. Format **JPG, sRGB, ≤ ~2 MB**
each (hard limits 4472 × 4472 px / 20 MB / 50 MP). Brand register: stealth black `#0A0A0A` / warm
bone `#FAFAF7` grounds, monochrome, matte. Upload uses the same blocked path as product images (§2).

**Product images (separate):** the product grid (`main-collection-product-grid`) is also `image_ratio:
"adapt"` — so product photos likewise show at their own ratio; keep the `/shopify` product shots a
consistent ratio per the manifest. (Current `/shopify` product files are mostly tall portrait.)

## 7. Launch-prep update (2026-06-29)

- **Product media:** operator manually uploaded all product images over the weekend — every product
  now has at least its front shot. Products are **ACTIVE** (the one stray DRAFT, Core Collection Tee,
  was flipped to ACTIVE).
- **Pricing:** all T-shirts set to **£50** (Core/Gradient/Japan Sun raised from £40; Tag already £50).
  Ski Masks kept at **£120** (premium, operator-confirmed). Tracksuits £160, bottoms £75, hoodie £90.
- **Phygital messaging (V1 launches WITHOUT live NFT):** every product description's old "tethered
  ownership" line was replaced with an **"NFT counterpart — coming soon"** paragraph: the encrypted
  SKU reserves the buyer's 1:1 digital ownership now; the NFT mints once the phygital protocol is live.
- **Collection covers:** the old No Apologies cover images were replaced with representative Caché
  **product shots** (already on the CDN) for Core, Gradient, Japan, Tag, Tracksuits, T-Shirts,
  Accessories. **Lightware + Darkware still have no cover** (empty tier placeholders). These are interim
  — swap in the 9 bespoke covers (1600×2000 / 1:1) when designed, via `scripts/shopify_upload_images.py --covers`.
- **"No Apologies" cleanup:** the **theme is clean** (no references). All remaining references live in
  the **store Policies** (Contact/Privacy/Refund/Terms/Shipping): trade name "No Apologies",
  `sales@noapologiesuk.co.uk` / `.store`, `noapologiesuk.*` URLs. Fix in Settings → Policies
  (→ Caché, `contact@dnaent.co.uk`, `hiddencache.co.uk`). Not API-edited (legal text + monitored email).
- **Automation:** Dev Dashboard app "Caché Automation" (client_credentials) is the token path for
  `scripts/shopify_upload_images.py`; in-chat automation runs via the Shopify MCP.
- **Still open:** ~~password-protect storefront~~ (done 2026-06-29); switch inventory to **tracked**
  once a 3PL/supplier is locked (currently untracked = sellable with no stock/fulfilment).
- **Policies / "No Apologies": DONE (2026-06-29).** Theme was already clean; all refs were in the legal
  Policies. Fixed via `scripts/fix_policies.py --apply` (Contact 2, Privacy 2, Refund 5, Terms 8;
  Shipping clean) → **0 "apolog" references remain**. Replacements applied: "No Apologies"→Caché,
  sales@noapologiesuk.*→contact@dnaent.co.uk, noapologiesuk.store/.co.uk→hiddencache.co.uk. Required
  adding `read_legal_policies`+`write_legal_policies` to the Caché Automation app and **re-installing**
  it (releasing a version does not re-grant scopes; reinstall does). The claude.ai MCP connector still
  lacks these scopes, so policy edits must go through the app token / `scripts/fix_policies.py`.
- **Still TODO on policies (not "No Apologies" — legal completeness):** unfilled template placeholders
  ([INSERT RETURN ADDRESS], business address/phone/VAT in Terms) + the one-line Shipping policy
  (parked until supplier sourced).

## 8. Product restructure — full tracksuits only (2026-06-29)

Operator decision: stop selling bottoms and hoodies separately; sell them only as **full tracksuits**
(hooded top + matching bottoms), still split by their own collections. Tees remain standalone.

- **Deleted** the 7 standalone Bottoms products (Core, Gradient, Japan Sun/Wave/Bamboo/Cherry, Tag).
- **Created** `Tag Collection Tracksuit` (gid 10297330172225, £160, S–XL, SKU `CACHE-TAG-TRK-BLK-*`,
  ACTIVE) — the Tag line had no tracksuit; built from the tag hoodie + tag bottoms images. Verified it
  retained its bottoms image after Tag Bottoms was deleted (Files asset persists).
- **Archived** `Tag Collection Hoodie` (now redundant; reversible).
- Core/Gradient/Japan tracksuits already showed their bottoms photos, so no image enrichment needed.
- **Resulting active catalogue (13):** Core Tee+Tracksuit, Gradient Tee+Tracksuit, Japan Sun Tee +
  Sun/Wave/Bamboo/Cherry Tracksuits, Tag Tee+Tracksuit, and 2 Accessories. Tracksuits collection = 7,
  T-Shirts = 4.
- **2026-06-29:** the two ski-mask products are a **2-in-1 convertible** (ribbed merino beanie that
  unrolls into a balaclava) — retitled "Convertible Beanie / Ski Mask — Black/Blue" (handles unchanged:
  `ski-mask-black` / `ski-mask-blue`). No separate beanie product — it's one item, two modes.
- **Note:** `docs/shopify_image_manifest.json` now contains stale entries for the deleted bottoms /
  archived hoodie (image attachment already complete, so non-blocking).

### 8.1 Materials spec (2026-06-29)

All garments (tees + tracksuits) are **100% heavyweight cotton**; ski masks are **100% merino wool**.
Recorded per product: (a) a "Fabric:" line in the description, and (b) a structured metafield
**`custom.material`**, now promoted to a **pinned, storefront-visible metafield definition** ("Material",
gid 268668371265). NB: the definition is data only — Dawn won't render it on the product page until a
**metafield block is bound in the theme customiser** (Online Store → Customize → Default product → add
a block → dynamic source = Material). The description "Fabric:" line is what's customer-visible today.

The **full brand material strategy** — per-`-ware`-tier fabric map (Lightware/Dailyware/Darkware +
accessories), GSM, and the perceived-value levers (weight, deep-black dye, gunmetal hardware, woven
trims, packaging) — is now codified in root **`CLAUDE.md` §4** and the ComfyUI fragments in
**`prompts/library.md`**. Those are the single source of truth for both product specs and marketing/
image generation. Synthetics (nylon/softshell/recycled-poly fill) are reserved for **Darkware** outerwear
and bags; Dailyware stays 100% cotton.

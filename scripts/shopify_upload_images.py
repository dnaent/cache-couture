#!/usr/bin/env python3
"""Attach local Caché design images to Shopify products (and collection covers).

WHY THIS EXISTS
---------------
The Shopify MCP used in the Claude chat can create/update products but cannot push
raw image *bytes*, and the chat sandbox has no internet. This script runs on a machine
*with* internet (your Mac/Windows) and does the byte upload via the standard Shopify
flow: stagedUploadsCreate -> upload bytes to Shopify's storage -> productCreateMedia.

AUTH (Dev Dashboard app "Caché Automation")
-------------------------------------------
Uses the client_credentials grant. You provide the app's Client ID + Secret; the script
fetches a fresh 24h access token itself, so no token is ever copy-pasted. Docs:
https://shopify.dev/docs/apps/build/dev-dashboard/get-api-access-tokens

SETUP
-----
    pip install requests
    export SHOPIFY_CLIENT_ID=...          # Dev Dashboard -> Caché Automation -> Settings
    export SHOPIFY_CLIENT_SECRET=...      # keep secret; never commit
    # optional overrides:
    # export SHOPIFY_SHOP=no-apologies-5  # store subdomain (default below)
    # export IMAGE_ROOT="/path/to/shopify"  # default = manifest's image_root
    # export SHOPIFY_ACCESS_TOKEN=shpat_... # skip the exchange if you already have a token

RUN
---
    python scripts/shopify_upload_images.py              # products only
    python scripts/shopify_upload_images.py --covers     # + collection covers (see COVERS)
    python scripts/shopify_upload_images.py --force      # re-upload even if media exists

Idempotent: by default a product/collection that already has image(s) is skipped, so the
script is safe to re-run after a partial run.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "docs" / "shopify_image_manifest.json"
API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2026-04")
SHOP = os.environ.get("SHOPIFY_SHOP", "no-apologies-5")

# Collection covers: fill in once the 9 cover images exist, then run with --covers.
# Map collection GID -> image filename (relative to IMAGE_ROOT). Left blank for now.
COVERS: dict[str, str] = {
    # "gid://shopify/Collection/434617745729": "cover_core.jpg",          # Core Collection
    # "gid://shopify/Collection/656391635265": "cover_gradient.jpg",      # Gradient Collection
    # "gid://shopify/Collection/434619416897": "cover_japan.jpg",         # Japan Collection
    # "gid://shopify/Collection/434619908417": "cover_tag.jpg",           # Tag Collection
    # "gid://shopify/Collection/656391700801": "cover_lightware.jpg",     # Lightware
    # "gid://shopify/Collection/656391864641": "cover_darkware.jpg",      # Darkware
    # "gid://shopify/Collection/434879725889": "cover_accessories.jpg",   # Accessories
    # "gid://shopify/Collection/434873598273": "cover_tracksuits.jpg",    # Tracksuits
    # "gid://shopify/Collection/434874057025": "cover_tshirts.jpg",       # T-Shirts
}

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def get_access_token() -> str:
    tok = os.environ.get("SHOPIFY_ACCESS_TOKEN")
    if tok:
        return tok
    cid = os.environ.get("SHOPIFY_CLIENT_ID")
    secret = os.environ.get("SHOPIFY_CLIENT_SECRET")
    if not (cid and secret):
        sys.exit("Set SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET (or SHOPIFY_ACCESS_TOKEN).")
    resp = requests.post(
        f"https://{SHOP}.myshopify.com/admin/oauth/access_token",
        data={"grant_type": "client_credentials", "client_id": cid, "client_secret": secret},
        timeout=30,
    )
    if resp.status_code != 200:
        sys.exit(f"Token request failed ({resp.status_code}): {resp.text[:300]}")
    return resp.json()["access_token"]


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    resp = requests.post(
        f"https://{SHOP}.myshopify.com/admin/api/{API_VERSION}/graphql.json",
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        json={"query": query, "variables": variables or {}},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"])[:500])
    return data["data"]


def staged_upload(token: str, path: Path) -> str:
    """Upload one file's bytes to Shopify staging; return its resourceUrl."""
    mime = MIME.get(path.suffix.lower(), "image/png")
    data = gql(
        token,
        """mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){
            stagedTargets{url resourceUrl parameters{name value}} userErrors{message}}}""",
        {"input": [{"filename": path.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]},
    )
    res = data["stagedUploadsCreate"]
    if res["userErrors"]:
        raise RuntimeError(res["userErrors"])
    target = res["stagedTargets"][0]
    form = {p["name"]: p["value"] for p in target["parameters"]}
    with path.open("rb") as fh:
        up = requests.post(target["url"], data=form, files={"file": (path.name, fh, mime)}, timeout=120)
    if up.status_code not in (200, 201, 204):
        raise RuntimeError(f"byte upload failed ({up.status_code}): {up.text[:200]}")
    return target["resourceUrl"]


def product_has_media(token: str, pid: str) -> bool:
    data = gql(token, "query($id:ID!){product(id:$id){media(first:1){nodes{id}}}}", {"id": pid})
    return bool(data["product"]["media"]["nodes"])


def attach_product_media(token: str, pid: str, sources: list[tuple[str, str]]):
    media = [{"originalSource": url, "alt": alt, "mediaContentType": "IMAGE"} for url, alt in sources]
    data = gql(
        token,
        """mutation($id:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$id,media:$media){
            media{...on MediaImage{id}} mediaUserErrors{field message}}}""",
        {"id": pid, "media": media},
    )
    errs = data["productCreateMedia"]["mediaUserErrors"]
    if errs:
        raise RuntimeError(errs)


def set_collection_cover(token: str, cid: str, resource_url: str):
    data = gql(
        token,
        """mutation($input:CollectionInput!){collectionUpdate(input:$input){
            collection{id} userErrors{field message}}}""",
        {"input": {"id": cid, "image": {"src": resource_url}}},
    )
    errs = data["collectionUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(errs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--covers", action="store_true", help="also upload collection covers (see COVERS map)")
    ap.add_argument("--force", action="store_true", help="upload even if media already exists")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    image_root = Path(os.environ.get("IMAGE_ROOT", manifest["image_root"]))
    token = get_access_token()
    print(f"Authenticated to {SHOP}.myshopify.com (API {API_VERSION}); image root: {image_root}")

    done = skipped = failed = 0
    for prod in manifest["products"]:
        pid, title = prod["productId"], prod["title"]
        try:
            if not args.force and product_has_media(token, pid):
                print(f"  skip (has media): {title}")
                skipped += 1
                continue
            sources = []
            for img in prod["images"]:
                fp = image_root / img["file"]
                if not fp.exists():
                    print(f"  ! missing file: {fp}")
                    continue
                url = staged_upload(token, fp)
                sources.append((url, f"{title} — {img.get('variant','')} {img.get('role','')}".strip()))
            if sources:
                attach_product_media(token, pid, sources)
                print(f"  OK {title}: {len(sources)} image(s)")
                done += 1
        except Exception as e:  # noqa: BLE001 - report and continue
            print(f"  FAIL {title}: {e}")
            failed += 1
        time.sleep(0.3)  # gentle on rate limits

    if args.covers:
        if not COVERS:
            print("--covers given but COVERS map is empty; fill it in once cover images exist.")
        for cid, fname in COVERS.items():
            fp = image_root / fname
            try:
                if not fp.exists():
                    print(f"  ! missing cover file: {fp}")
                    continue
                url = staged_upload(token, fp)
                set_collection_cover(token, cid, url)
                print(f"  OK cover {cid}: {fname}")
                done += 1
            except Exception as e:  # noqa: BLE001
                print(f"  FAIL cover {cid}: {e}")
                failed += 1

    print(f"\nDone. uploaded={done} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()

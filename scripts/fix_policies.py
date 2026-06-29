#!/usr/bin/env python3
"""Strip all 'No Apologies' references from the Caché store's legal policies.

The in-chat Shopify MCP connector lacks the `write_legal_policies` scope, so policy
edits can't be done from the Claude chat. This script does it via the Caché Automation
app (client_credentials) — Python applies EXACT string replacements to the live policy
bodies, so the large Privacy/Terms documents (cookie tables, links) are never retyped or
corrupted. Idempotent: safe to re-run.

PREREQUISITE — add one scope to the app (one-time):
  Dev Dashboard → Caché Automation → Versions → Create version → add `write_legal_policies`
  to the scopes list → Release. (Without it you'll get an "Access denied … write_legal_policies".)

SETUP / RUN (same creds as the image uploader):
  pip install requests
  export SHOPIFY_CLIENT_ID=...
  export SHOPIFY_CLIENT_SECRET=...
  python3 scripts/fix_policies.py            # dry run: shows what would change
  python3 scripts/fix_policies.py --apply    # actually update the policies
"""

from __future__ import annotations

import argparse
import os
import sys

import requests

SHOP = os.environ.get("SHOPIFY_SHOP", "no-apologies-5")
API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2026-04")

# Applied in order. Longer / more-specific strings first so they win before the
# bare-domain catch-alls run.
REPLACEMENTS = [
    ("sales@noapologiesuk.co.uk", "contact@dnaent.co.uk"),
    ("sales@noapologiesuk.store", "contact@dnaent.co.uk"),
    ("www.noapologiesuk.store", "hiddencache.co.uk"),
    ("noapologiesuk.store", "hiddencache.co.uk"),
    ("noapologiesuk.co.uk", "hiddencache.co.uk"),
    ("No Apologies", "Caché"),
    ("[INSERT TRADING NAME]", "Caché"),
]


def get_token() -> str:
    cid, secret = os.environ.get("SHOPIFY_CLIENT_ID"), os.environ.get("SHOPIFY_CLIENT_SECRET")
    if not (cid and secret):
        sys.exit("Set SHOPIFY_CLIENT_ID and SHOPIFY_CLIENT_SECRET.")
    r = requests.post(
        f"https://{SHOP}.myshopify.com/admin/oauth/access_token",
        data={"grant_type": "client_credentials", "client_id": cid, "client_secret": secret},
        timeout=30,
    )
    if r.status_code != 200:
        sys.exit(f"Token request failed ({r.status_code}): {r.text[:300]}")
    return r.json()["access_token"]


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    r = requests.post(
        f"https://{SHOP}.myshopify.com/admin/api/{API_VERSION}/graphql.json",
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        json={"query": query, "variables": variables or {}},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]


def apply_replacements(body: str) -> tuple[str, int]:
    new, hits = body, 0
    for old, repl in REPLACEMENTS:
        n = new.count(old)
        if n:
            new = new.replace(old, repl)
            hits += n
    return new, hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default is dry run)")
    args = ap.parse_args()

    token = get_token()
    policies = gql(token, "{ shop { shopPolicies { type body } } }")["shop"]["shopPolicies"]

    for p in policies:
        new_body, hits = apply_replacements(p["body"] or "")
        if hits == 0:
            print(f"  {p['type']}: clean (no references)")
            continue
        print(f"  {p['type']}: {hits} reference(s) to fix", "" if args.apply else "(dry run)")
        if args.apply:
            res = gql(
                token,
                "mutation($t:ShopPolicyType!,$b:String!){shopPolicyUpdate(shopPolicy:{type:$t,body:$b}){userErrors{field message}}}",
                {"t": p["type"], "b": new_body},
            )
            errs = res["shopPolicyUpdate"]["userErrors"]
            print(f"    -> {'updated' if not errs else errs}")

    # verify
    if args.apply:
        after = gql(token, "{ shop { shopPolicies { type body } } }")["shop"]["shopPolicies"]
        remaining = sum((b["body"] or "").lower().count("apolog") for b in after)
        print(f"\nRemaining 'apolog' references: {remaining}")
    else:
        print("\nDry run complete. Re-run with --apply to write the changes.")


if __name__ == "__main__":
    main()

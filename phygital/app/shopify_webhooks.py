"""Shopify webhook verification + orders/paid handling.

HMAC verification is real (standard Shopify scheme). The order handler drives the
phygital pipeline: mint tethered NFT -> persist tether -> forward to supplier.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
from typing import Any

from .alibaba import forward_order
from .config import get_settings
from .nft import mint_tethered_nft
from .store import Tether, get_store


def verify_hmac(raw_body: bytes, header_hmac: str | None) -> bool:
    """Verify the X-Shopify-Hmac-Sha256 header against the raw request body."""
    secret = get_settings().shopify_webhook_secret
    if not secret or not header_hmac:
        return False
    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode("utf-8")
    return hmac.compare_digest(expected, header_hmac)


def _buyer_wallet(order: dict[str, Any]) -> str | None:
    """Pull the buyer's wallet address from order note attributes if present.

    Storefront should collect the wallet at checkout (cart attribute "wallet").
    Returns None if absent — the NFT mints to a custody wallet and transfers later.
    """
    for attr in order.get("note_attributes", []) or []:
        if attr.get("name", "").lower() in {"wallet", "wallet_address"}:
            return attr.get("value") or None
    return None


async def handle_order_paid(order: dict[str, Any]) -> dict[str, Any]:
    """Process an orders/paid event through the phygital pipeline."""
    store = get_store()
    order_id = str(order.get("id", ""))
    wallet = _buyer_wallet(order)

    results: list[dict[str, Any]] = []
    for item in order.get("line_items", []) or []:
        sku = item.get("sku")
        if not sku:
            continue  # non-Caché / untracked line item
        token_id = await mint_tethered_nft(sku, wallet)
        store.upsert(
            Tether(sku=sku, order_id=order_id, wallet=wallet, token_id=token_id, status="minted")
        )
        results.append({"sku": sku, "token_id": token_id})

    fulfillment = await forward_order(order)
    return {"order_id": order_id, "tethers": results, "fulfillment": fulfillment}

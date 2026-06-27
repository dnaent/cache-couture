"""Alibaba / OEM supplier fulfillment (Shopify -> manufacturer).

CONTEXT (2026-06-27): The operator chose the **custom OEM supplier** path, not the
generic Alibaba.com Dropshipping app. Caché's signature construction — woven chip mark,
reflective yarn, gunmetal hardware, embedded NFC label (CLAUDE.md §4/§4.1/§5) — cannot
come from generic POD/catalog dropshipping. It requires a real cut-and-sew manufacturer.

IMPORTANT fulfillment reality: custom-branded garments are almost never shipped one unit
at a time straight from the factory. The practical model is batch cut-and-sew -> branded
stock held at a 3PL/fulfillment partner -> per-order fulfillment. So `forward_order` here
targets whatever per-order endpoint the chosen partner exposes — either the supplier's own
order API, a 3PL fulfillment API, or a middleware (e.g. Alibaba/1688 OpenAPI). The payload
shape below is a generic, vendor-neutral template; remap `_build_payload` once the real
supplier/3PL API spec is locked.

No-op while `ALIBABA_API_BASE` is unset (plumbing-only mode).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any

import httpx

from .config import get_settings


class SupplierNotConfigured(RuntimeError):
    """Raised when fulfillment is attempted before a supplier API is configured."""


def _sign(secret: str, body: bytes, timestamp: str) -> str:
    """HMAC-SHA256 over `timestamp.body` — generic scheme; adjust per supplier spec."""
    msg = timestamp.encode("utf-8") + b"." + body
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()


def _build_payload(order: dict[str, Any]) -> dict[str, Any]:
    """Map a Shopify order to a vendor-neutral supplier fulfillment payload.

    Only Caché line items (those carrying a SKU) are forwarded. Remap field names to
    match the real supplier/3PL contract once chosen.
    """
    ship = order.get("shipping_address") or {}
    items = [
        {
            "sku": li.get("sku"),
            "quantity": li.get("quantity", 1),
            "title": li.get("title"),
            "variant": li.get("variant_title"),
        }
        for li in (order.get("line_items") or [])
        if li.get("sku")
    ]
    return {
        "external_order_id": str(order.get("id", "")),
        "order_number": order.get("order_number"),
        "currency": order.get("currency"),
        # Caché brand requirements travel with every order (CLAUDE.md §4/§4.1/§5).
        "branding": {
            "private_label": True,
            "custom_packaging": True,
            "woven_chip_mark": True,
            "nfc_label": True,
        },
        "items": items,
        "shipping_address": {
            "name": ship.get("name"),
            "address1": ship.get("address1"),
            "address2": ship.get("address2"),
            "city": ship.get("city"),
            "province": ship.get("province"),
            "country": ship.get("country"),
            "country_code": ship.get("country_code"),
            "zip": ship.get("zip"),
            "phone": ship.get("phone"),
        },
    }


async def forward_order(order: dict[str, Any]) -> dict[str, Any]:
    """Forward a paid Shopify order to the OEM supplier / 3PL for fulfillment.

    No-op while no supplier API is configured (plumbing-only mode). Returns a result
    dict for the webhook handler to record; never raises on a clean no-op.
    """
    settings = get_settings()
    if not settings.alibaba_api_base:
        return {"forwarded": False, "reason": "supplier_not_configured"}

    payload = _build_payload(order)
    if not payload["items"]:
        return {"forwarded": False, "reason": "no_cache_line_items"}

    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    timestamp = str(int(time.time()))
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": settings.alibaba_api_key,
        "X-Timestamp": timestamp,
    }
    if settings.alibaba_api_secret:
        headers["X-Signature"] = _sign(settings.alibaba_api_secret, body, timestamp)

    url = settings.alibaba_api_base.rstrip("/") + "/orders"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, content=body, headers=headers)

    if resp.status_code >= 400:
        return {
            "forwarded": False,
            "reason": "supplier_error",
            "status": resp.status_code,
            "detail": resp.text[:500],
        }

    ctype = resp.headers.get("content-type", "")
    data = resp.json() if ctype.startswith("application/json") else {}
    return {
        "forwarded": True,
        "supplier_order_ref": data.get("id") or data.get("order_ref"),
        "status": resp.status_code,
    }

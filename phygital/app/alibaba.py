"""Alibaba supplier fulfillment (Shopify -> manufacturer).

NOTE (2026-06-26): No supplier is locked yet, and the recommended primary route is the
official Alibaba.com Dropshipping app for order sync (installed in Shopify, no custom
code). This module is the OPTIONAL custom-API path for when a supplier exposes a
per-order fulfillment endpoint. Also: Caché's signature construction (woven chip mark,
reflective yarn, gunmetal hardware, NFC label — CLAUDE.md §4/§4.1/§5) cannot come from
generic POD; this targets a real cut-and-sew manufacturer.
"""

from __future__ import annotations

from typing import Any

from .config import get_settings


class SupplierNotConfigured(RuntimeError):
    """Raised when fulfillment is attempted before a supplier API is configured."""


async def forward_order(order: dict[str, Any]) -> dict[str, Any]:
    """Forward a paid Shopify order to the supplier for fulfillment.

    No-op while no supplier API is configured (plumbing-only mode).
    """
    settings = get_settings()
    if not settings.alibaba_api_base:
        return {"forwarded": False, "reason": "supplier_not_configured"}

    # TODO: map Shopify line items -> supplier order payload, sign with
    # ALIBABA_API_KEY/SECRET, POST to ALIBABA_API_BASE, return supplier order ref.
    raise SupplierNotConfigured("Alibaba API base set but integration not implemented")

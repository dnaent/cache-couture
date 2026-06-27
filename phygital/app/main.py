"""Caché phygital service — FastAPI entrypoint.

Run (dev):
    cd phygital
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env   # then fill SHOPIFY_WEBHOOK_SECRET
    uvicorn app.main:app --reload --port 8090

Register the webhook in Shopify (Settings -> Notifications -> Webhooks, or Admin API):
    Topic: orders/paid   Format: JSON
    URL:   https://<your-deployed-host>/webhooks/shopify/orders-paid
"""

from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException, Request

from .shopify_webhooks import handle_order_paid, verify_hmac
from .store import get_store

app = FastAPI(title="Caché Phygital Service", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "cache-phygital"}


@app.post("/webhooks/shopify/orders-paid")
async def orders_paid(
    request: Request,
    x_shopify_hmac_sha256: str | None = Header(default=None),
) -> dict[str, object]:
    raw = await request.body()
    if not verify_hmac(raw, x_shopify_hmac_sha256):
        raise HTTPException(status_code=401, detail="invalid HMAC signature")
    order = await request.json()
    return await handle_order_paid(order)


@app.get("/tethers/{sku}")
async def get_tether(sku: str) -> dict[str, object]:
    """SKU -> NFT lookup (CLAUDE.md §13.8). Authentication / certificate endpoint."""
    tether = get_store().get(sku)
    if tether is None:
        raise HTTPException(status_code=404, detail="no tether for SKU")
    return tether.__dict__

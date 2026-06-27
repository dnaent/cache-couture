"""Caché phygital service package.

Implements the Phygital Protocol (CLAUDE.md §5): every physical garment carries an
encrypted SKU and an NFC tag, tethered 1:1 to an NFT that auto-mints to the buyer's
wallet at purchase. This service is the backend glue:

    Shopify (orders/paid webhook) -> verify HMAC -> mint tethered NFT
        -> persist SKU<->tokenId<->wallet -> (future) forward order to supplier.
"""

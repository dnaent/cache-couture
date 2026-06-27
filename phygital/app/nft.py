"""Tethered NFT minting (CLAUDE.md §5).

At purchase, a 1:1 NFT mints to the buyer's wallet and becomes the certificate of
authenticity. Physical and digital cannot be separated; transferring the physical
requires transferring the NFT, else the item is de-authenticated ("bricked").

This is a stub. Wire it to the chosen chain/contract (NFT_* env vars) when ratified.
"""

from __future__ import annotations

from .config import get_settings


class MintNotConfigured(RuntimeError):
    """Raised when a mint is attempted before chain/contract are configured."""


async def mint_tethered_nft(sku: str, wallet: str | None) -> str:
    """Mint the tethered NFT for a SKU and return the token id.

    Returns a deterministic placeholder token id until the chain is wired, so the
    rest of the pipeline (persistence, fulfillment) can be exercised end-to-end.
    """
    settings = get_settings()
    if not (settings.nft_chain and settings.nft_contract_address):
        # Plumbing-only mode: no chain configured yet. Surface a placeholder rather
        # than minting, so downstream handlers stay testable.
        return f"PLACEHOLDER-{sku}"

    # TODO: real mint via NFT_RPC_URL + contract using NFT_MINTER_PRIVATE_KEY.
    # On success return the on-chain token id.
    raise MintNotConfigured("NFT chain configured but mint integration not implemented")

"""Service configuration, loaded from environment / .env (see .env.example)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Shopify
    shopify_store_domain: str = "hiddencache.co.uk"
    shopify_myshopify_domain: str = "no-apologies-5.myshopify.com"
    shopify_admin_api_token: str = ""
    shopify_webhook_secret: str = ""

    # NFT mint (CLAUDE.md §5)
    nft_chain: str = ""
    nft_contract_address: str = ""
    nft_minter_private_key: str = ""
    nft_rpc_url: str = ""

    # Alibaba supplier (fulfillment) — unset until a supplier is locked.
    alibaba_api_base: str = ""
    alibaba_api_key: str = ""
    alibaba_api_secret: str = ""

    # Persistence
    gcp_project: str = "cache-couture"
    firestore_collection: str = "phygital_tethers"


@lru_cache
def get_settings() -> Settings:
    return Settings()

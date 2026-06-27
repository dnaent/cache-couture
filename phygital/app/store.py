"""Tether persistence: SKU <-> tokenId <-> wallet (CLAUDE.md §5, Tethered Ownership).

Dev default is an in-memory store. Swap for Firestore (GCP project cache-couture) by
implementing FirestoreTetherStore against the same interface — the rest of the service
only depends on TetherStore.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol


@dataclass
class Tether:
    sku: str
    order_id: str
    wallet: str | None = None
    token_id: str | None = None
    status: str = "pending"  # pending -> minted -> fulfilled | bricked
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TetherStore(Protocol):
    def upsert(self, tether: Tether) -> None: ...
    def get(self, sku: str) -> Tether | None: ...


class InMemoryTetherStore:
    """Non-persistent store for local development only."""

    def __init__(self) -> None:
        self._rows: dict[str, Tether] = {}

    def upsert(self, tether: Tether) -> None:
        self._rows[tether.sku] = tether

    def get(self, sku: str) -> Tether | None:
        return self._rows.get(sku)


# TODO: FirestoreTetherStore using google-cloud-firestore against
# settings.gcp_project / settings.firestore_collection once we deploy.
_store: TetherStore = InMemoryTetherStore()


def get_store() -> TetherStore:
    return _store

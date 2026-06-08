"""Caché ComfyUI client.

Thin HTTP client over ComfyUI's /prompt + /history + /view endpoints.

Server address: defaults to 127.0.0.1:8000 (the ComfyUI Electron build's
default). Override with the COMFYUI_HOST env var, e.g. ``127.0.0.1:8188``
for a portable / comfy-cli install. CLAUDE.md §17.4 documents the canonical
host.

Used by scripts/bootstrap_faces.py and scripts/bootstrap_garments.py to
drive the workflows/utility/qwen_edit_bootstrap.json graph.
"""

from __future__ import annotations

import copy
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

SERVER_ADDRESS = os.environ.get("COMFYUI_HOST", "127.0.0.1:8000")
CLIENT_ID = str(uuid.uuid4())


def _url(path: str) -> str:
    return f"http://{SERVER_ADDRESS}{path}"


def system_stats() -> dict[str, Any]:
    with urllib.request.urlopen(_url("/system_stats"), timeout=10) as r:
        return json.loads(r.read())


def queue_prompt(prompt: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps({"prompt": prompt, "client_id": CLIENT_ID}).encode("utf-8")
    req = urllib.request.Request(
        _url("/prompt"),
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ComfyUI /prompt rejected workflow: {e.code}\n{body}") from e


def get_history(prompt_id: str) -> dict[str, Any]:
    with urllib.request.urlopen(_url(f"/history/{prompt_id}"), timeout=15) as r:
        return json.loads(r.read())


def get_image(filename: str, subfolder: str, folder_type: str) -> bytes:
    qs = urllib.parse.urlencode(
        {"filename": filename, "subfolder": subfolder, "type": folder_type}
    )
    with urllib.request.urlopen(_url(f"/view?{qs}"), timeout=30) as r:
        return r.read()


def load_workflow(path: str | Path) -> dict[str, Any]:
    """Load a workflow JSON, stripping the optional `_meta` annotation block."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    data.pop("_meta", None)
    return data


def substitute(
    workflow: dict[str, Any], patches: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """Return a deep-copied workflow with per-node input patches applied.

    ``patches`` maps node id (string) → mapping of input key → new value.
    Unknown node ids raise; unknown input keys are added (this is how
    ComfyUI's API graph works — inputs is just a flat dict per node).
    """
    g = copy.deepcopy(workflow)
    for node_id, patch in patches.items():
        if node_id not in g:
            raise KeyError(f"Workflow has no node id {node_id!r}")
        g[node_id].setdefault("inputs", {}).update(patch)
    return g


def submit_and_wait(
    workflow: dict[str, Any],
    poll_interval: float = 2.0,
    timeout: float = 600.0,
) -> dict[str, Any]:
    """Queue a workflow, poll /history until it completes, return the history entry."""
    res = queue_prompt(workflow)
    prompt_id = res["prompt_id"]
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        hist = get_history(prompt_id)
        if prompt_id in hist:
            entry = hist[prompt_id]
            status = entry.get("status", {})
            if status.get("completed") or status.get("status_str") == "success":
                return entry
            if status.get("status_str") == "error":
                msgs = status.get("messages", [])
                raise RuntimeError(
                    f"ComfyUI reported error for prompt {prompt_id}: {msgs}"
                )
        time.sleep(poll_interval)
    raise TimeoutError(f"Prompt {prompt_id} did not complete within {timeout}s")


def fetch_outputs(history_entry: dict[str, Any], dest_dir: str | Path) -> list[Path]:
    """Download every image listed in a completed history entry into dest_dir.

    Returns the list of locally-written paths in queue order.
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    outputs = history_entry.get("outputs", {})
    for node_id in sorted(outputs.keys(), key=lambda x: int(x) if x.isdigit() else x):
        node_out = outputs[node_id]
        for img in node_out.get("images", []):
            data = get_image(img["filename"], img.get("subfolder", ""), img.get("type", "output"))
            out_path = dest / img["filename"]
            out_path.write_bytes(data)
            written.append(out_path)
    return written


if __name__ == "__main__":
    s = system_stats()
    dev = s["devices"][0] if s.get("devices") else {}
    print(
        f"ComfyUI v{s['system']['comfyui_version']} on {SERVER_ADDRESS}\n"
        f"  device: {dev.get('name', '?')}\n"
        f"  vram free: {dev.get('vram_free', 0) / 1024**3:.2f} GiB / "
        f"{dev.get('vram_total', 0) / 1024**3:.2f} GiB"
    )

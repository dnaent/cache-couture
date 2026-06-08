"""Render per-collection ai-toolkit configs from the Caché garment LoRA template.

Reads `configs/ai_toolkit/cache_garment_qwen_12gb.template.yaml`, expands
`__COLLECTION__` / `__TRIGGER__` for every active collection (C2/C3/C4), and
writes one file per collection next to the template.

Active collections are hard-coded here. Collection vocabulary uses the `-ware`
suffix (Lightware / Dailyware / Darkware) — see CLAUDE.md §3 for the rationale.
"""

from __future__ import annotations

from pathlib import Path

ACTIVE_COLLECTIONS = ["lightware", "dailyware", "darkware"]

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "configs" / "ai_toolkit" / "cache_garment_qwen_12gb.template.yaml"
OUTPUT_DIR = REPO_ROOT / "configs" / "ai_toolkit"


HEADER_END = "# === END TEMPLATE HEADER ==="


def render(template: str, collection: str) -> str:
    body = template
    if HEADER_END in body:
        _, _, body = body.partition(HEADER_END)
        body = body.lstrip("\n")
        body = "---\n" + body
    return (
        body
        .replace("__COLLECTION__", collection)
        .replace("__TRIGGER__", f"{collection}_set")
    )


def main() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    for collection in ACTIVE_COLLECTIONS:
        out_path = OUTPUT_DIR / f"cache_garment_{collection}_qwen_12gb.yaml"
        out_path.write_text(render(template, collection), encoding="utf-8")
        print(f"wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

"""Render per-slot ai-toolkit configs from the Caché face LoRA template.

Reads `configs/ai_toolkit/cache_face_qwen_12gb.template.yaml`, expands
`__SLOT__` / `__SLOT_LOWER__` / `__TRIGGER__` for every active cast slot,
and writes one file per slot next to the template.

Active roster is hard-coded here because the INDEX.md markdown table is
for humans, not for parsing. Update ACTIVE_SLOTS when the roster changes.
M03 is retired (merged into M01) — leaving the hole is intentional, the
brand convention is append-only slot numbering.
"""

from __future__ import annotations

from pathlib import Path

ACTIVE_SLOTS = ["M01", "M02", "M04", "M05", "M06", "M07", "M08", "M09", "M10"]

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "configs" / "ai_toolkit" / "cache_face_qwen_12gb.template.yaml"
OUTPUT_DIR = REPO_ROOT / "configs" / "ai_toolkit"


HEADER_END = "# === END TEMPLATE HEADER ==="


def render(template: str, slot: str) -> str:
    body = template
    if HEADER_END in body:
        _, _, body = body.partition(HEADER_END)
        body = body.lstrip("\n")
        body = "---\n" + body
    slot_lower = slot.lower()
    return (
        body
        .replace("__SLOT_LOWER__", slot_lower)
        .replace("__SLOT__", slot)
        .replace("__TRIGGER__", f"{slot_lower}_face")
    )


def main() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    for slot in ACTIVE_SLOTS:
        out_path = OUTPUT_DIR / f"cache_face_{slot.lower()}_qwen_12gb.yaml"
        out_path.write_text(render(template, slot), encoding="utf-8")
        print(f"wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

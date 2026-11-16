#!/usr/bin/env python3
"""Upgrade exact private Beta5.8/Test53 HTML to Beta5.9/Test54c.

The generated HTML embeds copyrighted game data. Keep it private. This
ROM-free builder requires the owner's private Beta5.8 editor and exact Test54c
ROM as inputs. It preserves the embedded older Test44 and clean-map modules.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
from pathlib import Path
import re
import zlib

HERE = Path(__file__).resolve().parent
OLD_EDITOR_SHA = "e79862dd436697489cfe326378e240c67052faccbb69ea8ad3f0f8da87186f19"
ROM_SHA = "924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01"
ROM_SIZE = 4_194_304


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_once(source: str, before: str, after: str, label: str) -> str:
    n = source.count(before)
    if n != 1:
        raise ValueError(f"{label}: expected one occurrence, found {n}")
    return source.replace(before, after, 1)


def csvrows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def load_tables(data_dir: Path) -> dict[str, object]:
    ships = csvrows(data_dir / "ships_v8v4.csv")
    rules = csvrows(data_dir / "npc_fleet_rules_v4.csv")
    stocks = csvrows(data_dir / "stock_limits_46_approved.csv")
    if (len(ships), len(rules), len(stocks)) != (25, 63, 46):
        raise ValueError("Expected 25 ships, 63 NPC generation records and 46 stock entries")
    if any(int(row["slot"]) != i for i, row in enumerate(ships)):
        raise ValueError("Ship model slots are not in native order")
    if any(int(row["Planning slot*"]) != i + 1 for i, row in enumerate(stocks)):
        raise ValueError("Stock planning slots are not in native order")
    return {
        "__GOODS_JSON__": [row["Latest name"] for row in stocks],
        "__SHIPS_JSON__": [row["ship"] for row in ships],
        "__RULES_JSON__": [
            {
                "pc": row["pc"], "status": row["status"],
                "implemented_choices": row["implemented_choices"],
                "after_hex": row["after_hex"],
            }
            for row in rules
        ],
        "__STOCK_JSON__": [int(row["APPROVED new qty"]) for row in stocks],
    }


def translate_beta58_code(template: str) -> str:
    """Rename guarded source and UI, without touching numeric table offsets."""
    mapping = (
        ("// Beta 5.8:", "// Beta 5.9:"),
        ("9f91aaa32e91808397b470e58fd3104fe35c5885b554de5bf6e39a2d5efe6b78", ROM_SHA),
        ("UW53Core", "UW54Core"),
        ("__uw53ProjectPending", "__uw54ProjectPending"),
        ("test53-rom-bundle", "test54c-rom-bundle"),
        ("TEST53", "TEST54C"),
        ("Test53", "Test54c"),
        ("Test 53", "Test 54c"),
        ("test53", "test54c"),
        ("t53", "t54c"),
        ("Beta58", "Beta59"),
        ("Beta5.8", "Beta5.9"),
        ("beta58", "beta59"),
    )
    result = template
    for a, b in mapping:
        result = result.replace(a, b)
    return result


def assemble(editor_path: Path, rom_path: Path, data_dir: Path, output_path: Path) -> dict:
    raw_editor = editor_path.read_bytes()
    if sha(raw_editor) != OLD_EDITOR_SHA:
        raise ValueError("Wrong Beta5.8 source HTML; this builder is exact-source locked")
    raw_rom = rom_path.read_bytes()
    if len(raw_rom) != ROM_SIZE or sha(raw_rom) != ROM_SHA:
        raise ValueError("Wrong Test54c ROM; preserving previous editor baseline")
    html = raw_editor.decode("utf-8")

    old_panel = (HERE / "source/beta58_panel.html").read_text(encoding="utf-8")
    new_panel = translate_beta58_code(old_panel)
    new_panel = replace_once(
        new_panel,
        ' <p class="hint warn"><b>Do not publish this personal HTML file:</b>',
        ' <p class="hint"><b>Test54c inherited changes:</b> Sambuk, Lancaran and Jong ship illustrations; '
        'game-role ship descriptions; Rimbo biography and introductory text. They are preserved '
        'from the bundled ROM, but artwork/text editing is not yet exposed as a guarded field. '
        'The legacy <code>~Ernst~</code> heading remains a known issue.</p>\n'
        ' <p class="hint warn"><b>Do not publish this personal HTML file:</b>',
        "Test54c scope note",
    )
    html = replace_once(html, old_panel, new_panel, "Beta5.8 sidebar panel")

    code = translate_beta58_code((HERE / "source/beta58_core.js").read_text(encoding="utf-8"))
    for key, value in load_tables(data_dir).items():
        code = replace_once(code, key, json.dumps(value, ensure_ascii=False), key)
    start_marker = "// Beta 5.8: guarded editing"
    stop_marker = "\nUW53Core.setup();"
    if html.count(start_marker) != 1 or html.count(stop_marker) != 1:
        raise ValueError("Beta5.8 protected core location changed")
    start = html.index(start_marker)
    stop = html.index(stop_marker, start) + len(stop_marker)
    html = html[:start] + code + html[stop:]

    bundle_text = base64.b64encode(zlib.compress(raw_rom, 9)).decode("ascii")
    bundle_pattern = re.compile(r'<script id="test53-rom-bundle" type="text/plain">[A-Za-z0-9+/=]+</script>')
    html, num = bundle_pattern.subn(
        '<script id="test54c-rom-bundle" type="text/plain">' + bundle_text + '</script>', html
    )
    if num != 1:
        raise ValueError(f"Expected one embedded Test53 bundle, found {num}")

    old_title = "World, Ship & Fleet Studio — Beta 5.8 · Test 53 Integrated"
    new_title = "World, Ship & Fleet Studio — Beta 5.9 · Test 54c Integrated"
    html = replace_once(html, old_title, new_title, "Document title")
    html = replace_once(
        html, "World, Ship & Fleet Studio · Beta 5.8 · Test 53",
        "World, Ship & Fleet Studio · Beta 5.9 · Test 54c", "Header title",
    )
    outside_mapping = (
        ("#test53Section", "#test54cSection"),
        ("loadT53Top", "loadT54Top"),
        ("Load Test 53", "Load Test 54c"),
        ("test53Edits:UW53Core.snapshot()", "test54cEdits:UW54Core.snapshot()"),
        ("obj.test53Edits", "obj.test54cEdits"),
        ("window.__uw53ProjectPending", "window.__uw54ProjectPending"),
        ("openMode==='test53'", "openMode==='test54c'"),
        ("UW53Core", "UW54Core"),
    )
    for before, after in outside_mapping:
        if before not in html:
            raise ValueError(f"Missing legacy hookup for {before!r}")
        html = html.replace(before, after)
    legacy_tokens = (
        "Beta 5.8", "Test 53", "Test53", "test53Edits", "UW53Core", "test53-rom-bundle",
        "test53Section", "loadT53Top", "__uw53ProjectPending", "openMode==='test53'",
    )
    if any(s in html for s in legacy_tokens):
        raise ValueError("Stale Beta5.8/Test53 integration tokens remain")
    if "test44-rom-bundle" not in html or "test44Section" not in html:
        raise ValueError("Legacy Test44 panel must be preserved")
    if html.count('id="test54cSection"') != 1 or html.count('id="test54c-rom-bundle"') != 1:
        raise ValueError("Test54c panel or bundle duplicated")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return {
        "status": "Beta5.9 private editor built; functional QA still required",
        "source_editor_sha256": OLD_EDITOR_SHA,
        "bundled_rom_sha256": ROM_SHA,
        "output": str(output_path),
        "editor_sha256": sha(output_path.read_bytes()),
        "html_bytes": output_path.stat().st_size,
        "new_bundle_compressed_bytes": len(bundle_text) * 3 // 4,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--editor", type=Path, required=True)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=HERE / "reference_data")
    parser.add_argument("--out", type=Path, default=HERE / "deliverables/New_Horizons_World_Ship_Fleet_Studio_Beta_5_9_Test54c_Integrated.html")
    a = parser.parse_args()
    print(json.dumps(assemble(a.editor, a.rom, a.data, a.out), indent=2))

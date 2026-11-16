#!/usr/bin/env python3
"""Add a hash-locked clean-ROM upgrade function to the exact Beta 5.9 editor.

Owner-supplied inputs: private editor HTML (bundles commercial ROM), cumulative IPS.
Output: private integrated HTML. This script itself contains no ROM or patch bytes.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
from pathlib import Path


EDITOR_SHA = "7d9b5263588929b49e186da4b108ac6475201cd25adbe826a7e67a0d757e890e"
IPS_SHA = "b92debc2c64dc10a0570f6da9eca182565b35e13de2caeef125bf4b3eb149286"
IPS_BYTES = 88565


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_once(source: str, needle: str, replacement: str) -> str:
    count = source.count(needle)
    if count != 1:
        raise ValueError(f"Expected exactly one insertion marker; got {count}: {needle[:80]}")
    return source.replace(needle, replacement, 1)


def build(editor: Path, ips: Path, output: Path) -> dict:
    original = editor.read_bytes()
    patch = ips.read_bytes()
    if sha(original) != EDITOR_SHA:
        raise ValueError("Editor HTML does not match the exact approved Beta 5.9 baseline")
    if sha(patch) != IPS_SHA or len(patch) != IPS_BYTES:
        raise ValueError("IPS does not match the independently verified cumulative Test54c patch")
    content = original.decode("utf-8")
    folder = Path(__file__).resolve().parent / "source"
    panel = (folder / "upgrade_panel.html").read_text(encoding="utf-8")
    module = (folder / "upgrade_core.js").read_text(encoding="utf-8")
    if "</script" in module.lower() or "</script" in base64.b64encode(patch).decode("ascii"):
        raise ValueError("Unsafe inline JS/IPS insertion")

    content = replace_once(content, '<div class="layout"><aside>', '<div class="layout"><aside>\n' + panel)
    payload = base64.b64encode(patch).decode("ascii")
    content = replace_once(
        content,
        '<script id="test54c-rom-bundle" type="text/plain">',
        '<script id="test54c-retail-upgrade-ips" type="text/plain">'
        + payload
        + '</script>\n<script id="test54c-rom-bundle" type="text/plain">',
    )
    content = replace_once(content, 'UW54Core.setup();', 'UW54Core.setup();\n\n' + module)
    content = replace_once(
        content,
        'World, Ship & Fleet Studio · Beta 5.9 · Test 54c</small>',
        'World, Ship & Fleet Studio · Beta 5.9 Rev A · Test 54c + Original ROM Upgrader</small>',
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    final_bytes = content.encode("utf-8")
    output.write_bytes(final_bytes)
    return {
        "baseline_editor_sha256": EDITOR_SHA,
        "cumulative_ips_sha256": IPS_SHA,
        "cumulative_ips_size": len(patch),
        "output_sha256": sha(final_bytes),
        "output_bytes": len(final_bytes),
        "output": str(output),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--editor", type=Path, required=True)
    parser.add_argument("--ips", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    import json
    print(json.dumps(build(args.editor, args.ips, args.output), indent=2))

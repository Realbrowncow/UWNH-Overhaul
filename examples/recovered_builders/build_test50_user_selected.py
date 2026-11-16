#!/usr/bin/env python3
"""Test50: exact selected Rimbo Test5 and original Face113 Asmira, all views.

Starting from audited Test49, change only the two 40x48 compressed face
packets plus the SNES checksum. Both supplied images use precisely the ROM's
existing 16-colour shared portrait palette, so no quantisation is necessary.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import zipfile

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
sys.path.insert(0, str(ROOT / "preflight"))
import build_test48_portraits as codec
from portrait_preflight import encode_snes4, decode_snes4, rom_palette, normalise, protected

INPUT = ROOT / "output49/UWNH_Test49_Rimbo_Polished_All_Views_AsmiraV1_EXPERIMENTAL_2026-11-15.smc"
EXPECTED_INPUT_SHA = "c530e21f3c2945821d4d486471ff8eebd150a161ad6d1cd3611936f600bc6028"
IMAGES = {
    "Rimbo": PROJECT / "upload/rimbo test5.png",
    "Asmira": PROJECT / "upload/fixed_face_113.png",
}
FACES = {"Rimbo": (3, 24), "Asmira": (39, 113)}
OUT = ROOT / "output50"
STEM = "UWNH_Test50_Rimbo_Test5_Asmira_Face113_AllViews_EXPERIMENTAL_2026-11-15"
NAV_BASE = 0x0881F3


def sha(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def checksum_snes(rom: bytearray) -> int:
    rom[0xFFDC:0xFFE0] = b"\0" * 4
    ck = (sum(rom) + 510) & 0xFFFF
    rom[0xFFDC:0xFFDE] = (ck ^ 0xFFFF).to_bytes(2, "little")
    rom[0xFFDE:0xFFE0] = ck.to_bytes(2, "little")
    assert (sum(rom) & 0xFFFF) == ck
    return ck


def map_exact_rgb(source: Image.Image, palette: list[tuple[int, int, int]]) -> Image.Image:
    """Copy every input pixel to the corresponding *exact* shared SNES colour."""
    native = normalise(source)
    assert native.size == (40, 48)
    assert all(a == 255 for *_, a in native.getdata()), "No transparency in supplied portraits"
    lookup = {rgb: i for i, rgb in enumerate(palette)}
    assert len(lookup) == 16, "Shared palette has unexpected duplicate colours"
    original = native.convert("RGB")
    unique = set(original.getdata())
    assert unique.issubset(lookup), f"Cannot match source colours exactly: {unique - set(lookup)}"
    indices = bytes(lookup[p] for p in original.getdata())
    indexed = Image.frombytes("P", (40, 48), indices)
    indexed.putpalette([v for rgb in palette for v in rgb] + [0] * (256 * 3 - 48))
    assert indexed.convert("RGB").tobytes() == original.tobytes(), "RGB roundtrip changed pixels"
    return indexed


def main() -> None:
    baseline = INPUT.read_bytes()
    assert len(baseline) == 0x400000 and sha(baseline) == EXPECTED_INPUT_SHA
    assert int.from_bytes(baseline[NAV_BASE + 3 * 50 + 26:NAV_BASE + 3 * 50 + 28], "little") == 24
    assert int.from_bytes(baseline[NAV_BASE + 77 * 50 + 26:NAV_BASE + 77 * 50 + 28], "little") == 113
    assert baseline[NAV_BASE + 3 * 50:NAV_BASE + 3 * 50 + 5] == b"Rimbo"
    assert baseline[NAV_BASE + 77 * 50:NAV_BASE + 77 * 50 + 6] == b"Asmira"
    assert [i for i in range(100) if baseline[0x219200 + 25 * i + 11]] == [77]

    shared = rom_palette(baseline)
    new_rom = bytearray(baseline)
    imported = {}
    report_imports = {}
    for name, path in IMAGES.items():
        source = Image.open(path)
        indexed = map_exact_rgb(source, shared)
        raw = encode_snes4(indexed)
        assert len(raw) == 960 and decode_snes4(raw, shared).tobytes() == indexed.tobytes()
        packet = codec.make_literal_packet(raw)
        assert len(packet) == 1083
        pc = codec.PACKET_SLOTS[name]
        assert baseline[pc:pc + 2] == b"\xFC\x01"
        assert pc + len(packet) <= pc + 0x500
        new_rom[pc:pc + len(packet)] = packet
        imported[name] = indexed
        report_imports[name] = {
            "source_image": path.name,
            "source_dimensions": list(source.size),
            "native_dimensions": [40, 48],
            "native_source_rgb_SHA256": sha(normalise(source).convert("RGB").tobytes()),
            "distinct_colours": len(set(indexed.tobytes())),
            "RGB_pixels_preserved_exactly": 1920,
            "pixel_color_error": 0,
            "compressed_packet_PC": hex(pc),
            "assigned_fixed_faces": list(FACES[name]),
        }
        for face in FACES[name]:
            assert codec.face_ptr(baseline, face) == pc, (name, face)
            assert codec.face_ptr(new_rom, face) == pc

    ck = checksum_snes(new_rom)
    # No change to palette, pointers, character records, sprites, or gameplay.
    allowed = set(range(0xFFDC, 0xFFE0))
    for name in imported:
        pc = codec.PACKET_SLOTS[name]
        allowed.update(range(pc, pc + 1083))
    changed = [i for i, (a, b) in enumerate(zip(baseline, new_rom)) if a != b]
    assert changed and set(changed) <= allowed
    assert new_rom[0xAAF00:0xABF00] == baseline[0xAAF00:0xABF00]
    assert new_rom[codec.FACE_PTR_PC:codec.FACE_PTR_PC + 128 * 3] == baseline[codec.FACE_PTR_PC:codec.FACE_PTR_PC + 128 * 3]
    assert new_rom[NAV_BASE:NAV_BASE + 120 * 50] == baseline[NAV_BASE:NAV_BASE + 120 * 50]
    assert protected(new_rom) == protected(baseline)
    assert [i for i in range(100) if new_rom[0x219200 + 25 * i + 11]] == [77]

    extracted = {}
    for name, indexed in imported.items():
        for face in FACES[name]:
            pc = codec.face_ptr(new_rom, face)
            raw = codec.read_literal_packet(new_rom[pc:pc + 1083])
            decoded = decode_snes4(raw, shared)
            assert decoded.tobytes() == indexed.tobytes()
            assert decoded.convert("RGB").tobytes() == normalise(Image.open(IMAGES[name])).convert("RGB").tobytes()
            extracted[f"{name}_face{face}"] = decoded

    bytes_out = bytes(new_rom)
    ips = codec.make_ips(baseline, bytes_out)
    assert codec.apply_ips(baseline, ips) == bytes_out
    OUT.mkdir(parents=True, exist_ok=True)
    rom_path = OUT / f"{STEM}.smc"
    ips_path = OUT / f"{STEM}_from_Test49.ips"
    rom_path.write_bytes(bytes_out)
    ips_path.write_bytes(ips)
    for name in imported:
        imported[name].save(OUT / f"Test50_{name}_40x48_ExactGamePalette.png")
        imported[name].resize((400, 480), Image.Resampling.NEAREST).save(OUT / f"Test50_{name}_10x_PixelPreview.png")

    overview = Image.new("RGB", (900, 530), (23, 30, 37))
    draw = ImageDraw.Draw(overview)
    for n, name in enumerate(("Rimbo", "Asmira")):
        x = 34 + 440 * n
        draw.text((x, 20), f"{name}: extracted from Test50 ROM", fill=(247, 238, 219))
        overview.paste(extracted[f"{name}_face{FACES[name][0]}"].convert("RGB").resize((360, 432), Image.Resampling.NEAREST), (x, 51))
        draw.text((x, 493), f"Fixed faces {FACES[name]}  |  RGB exactly preserved", fill=(207, 216, 220))
    overview_path = OUT / "Test50_Rimbo_Asmira_ROM_Extracted_Comparison.png"
    overview.save(overview_path)

    report = {
        "status": "STATIC PASS; in-game character selection, Character View, dialogue tests pending",
        "source_rom": INPUT.name,
        "source_sha256": sha(baseline),
        "output_rom": rom_path.name,
        "output_sha256": sha(bytes_out),
        "ips_sha256": sha(ips),
        "changed_byte_count": len(changed),
        "changed_offset_allowlist": ["Rimbo 0x200F00+1083", "Asmira 0x201400+1083", "checksum 0xFFDC+4"],
        "all_changed_bytes_allowlisted": True,
        "palette_and_nonportrait_data_untouched": True,
        "navigator_character_view_face_fields_preserved": {"Rimbo_ID3": 24, "Asmira_ID77": 113},
        "character_selection_and_dialogue_face_aliases": FACES,
        "original_image_pixels_preserved_exactly": True,
        "IPS_exact_roundtrip": True,
        "SNES_checksum": hex(ck),
        "imports": report_imports,
        "gameplay_verified": False,
    }
    audit_path = OUT / f"{STEM}_Static_Audit.json"
    audit_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    readme_path = OUT / f"{STEM}_README.md"
    readme_path.write_text(f"""# Test50 — user-selected Rimbo Test5 and Asmira Face113

**Static PASS; game test still required.** Based exclusively on verified Test49 ROM SHA `{sha(baseline)}`. No shipyard, pricing, fleet, navigator statistics, town, or map changes.

* Rimbo: supplied **rimbo test5.png** at native 40×48, exact colours and every pixel preserved.
* Asmira: supplied **fixed_face_113.png** at exact 3× nearest-neighbour scaling, restored to native 40×48, exact colours and every pixel preserved.
* Installed into the existing shared SNES palette without quantisation, dithering, or palette modifications. Fixed portrait aliases Rimbo **3 and 24**, Asmira **39 and 113** remain linked to the correct new artwork.
* Navigator Rimbo ID3 still uses face **24** and Asmira ID77 still uses face **113**. This explicitly preserves the Test49 fix for Character View.
* Small walking sprites are unchanged.

## Please test

Start a **new game** as Rimbo and inspect (1) the six-character selection screen, (2) Character View / Status, (3) town dialogue / opening portrait, and (4) Asmira's harbour conversation and Character View if available. Check these faces agree in every context. Save/reload if practical.

SHA256 ROM: `{sha(bytes_out)}`. IPS applies ONLY to exact Test49 ROM, not earlier test ROMs. Compressed 4bpp data, shared palette, all protected records, strict offset allowlist, checksum and IPS roundtrip independently verified. No emulator gameplay pass is claimed.
""", encoding="utf-8")
    zip_path = OUT / f"{STEM}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in [rom_path, ips_path, audit_path, readme_path, overview_path,
                  *(OUT / f"Test50_{name}_40x48_ExactGamePalette.png" for name in imported),
                  *(OUT / f"Test50_{name}_10x_PixelPreview.png" for name in imported),
                  Path(__file__)]:
            z.write(p, p.name)
    with zipfile.ZipFile(zip_path) as z:
        assert z.read(rom_path.name) == bytes_out
    print(json.dumps({"status": report["status"], "rom_path": str(rom_path), "sha256": sha(bytes_out), "ips_path": str(ips_path), "zip_path": str(zip_path), "changed_bytes": len(changed)}, indent=2))


if __name__ == "__main__":
    main()

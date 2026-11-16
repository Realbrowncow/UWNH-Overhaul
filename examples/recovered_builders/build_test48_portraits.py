#!/usr/bin/env python3
"""Build Test48 by importing approved Rimbo V3 / Asmira V1 fixed-face art.

Only the exact corrected Test47 input ROM is accepted. This is an isolated
portrait experiment, not a gameplay-confirmed replacement for Test45.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "test48_work"
SOURCE = ROOT / "test48_sources/Uncharted waters/Ship Design/UWNH_Test47_V8v4_V4_Makassar_Jong_Exclusive_CapitalFix_TEST_2026-11-15.smc"
OUTPUT = WORK / "output"
STEM = "UWNH_Test48_RimboV3_AsmiraV1_CustomPortraits_EXPERIMENTAL_2026-11-15"
EXPECTED_SHA256 = "8f191a5bd426f85ad20e79d61b5c69f03da2b9512d31b5e26afed74c1264e192"
FACE_PTR_PC = 0x02BCB7
FACE_PAL_PC = 0x0AAF00
POINTER_ORIGIN_PC = 0x17CEE9
PACKET_ALLOC = 0x500
PACKET_SLOTS = {"Rimbo": 0x200F00, "Asmira": 0x201400}
FACE_SLOTS = {"Rimbo": (3, 24), "Asmira": (39, 113)}
PNG = {
    "Rimbo": WORK / "rimbo/Rimbo_Young_CloseUp_V3_EnhancedEyes_40x48_Indexed.png",
    "Asmira": WORK / "asmira/Asmira_Young_V1_40x48_Indexed16_SNES.png",
}
TILES = {
    "Rimbo": WORK / "rimbo/Rimbo_Young_CloseUp_V3_EnhancedEyes_4bpp_960bytes.bin",
    "Asmira": WORK / "asmira/Asmira_Young_V1_SNES_4bpp_960bytes.bin",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def face_ptr(rom: bytes, face: int) -> int:
    off = FACE_PTR_PC + face * 3
    return POINTER_ORIGIN_PC + int.from_bytes(rom[off:off + 3], "little")


def make_literal_packet(uncompressed: bytes) -> bytes:
    """Use byte-for-byte proven literal-only container from Test47 face assets."""
    assert len(uncompressed) == 30 * 32 == 960
    packet = b"\xFC\x01" + b"".join(
        b"\xFF" + uncompressed[i:i + 8] for i in range(0, 960, 8)
    ) + b"\x00"
    assert len(packet) == 1083
    assert read_literal_packet(packet) == uncompressed
    return packet


def read_literal_packet(packet: bytes) -> bytes:
    assert len(packet) >= 1083
    assert packet[:2] == b"\xFC\x01" and packet[1082:1083] == b"\x00"
    assert all(packet[2 + 9 * n] == 0xFF for n in range(120))
    return b"".join(packet[3 + 9 * n:11 + 9 * n] for n in range(120))


def to_snes_palette(img: Image.Image) -> bytes:
    assert img.mode == "P" and img.size == (40, 48)
    values = img.getpalette()
    assert values is not None
    entries = [values[i * 3:i * 3 + 3] for i in range(16)]
    result = bytearray()
    for red, green, blue in entries:
        r5, g5, b5 = (round(c * 31 / 255) for c in (red, green, blue))
        result.extend((r5 | g5 << 5 | b5 << 10).to_bytes(2, "little"))
    return bytes(result)


def palette_rgb(pal: bytes) -> list[tuple[int, int, int]]:
    assert len(pal) == 32
    colors = []
    for i in range(16):
        w = int.from_bytes(pal[i * 2:i * 2 + 2], "little")
        colors.append(tuple(round(((w >> shift) & 31) * 255 / 31) for shift in (0, 5, 10)))
    return colors


def decode_snes4(tile_data: bytes, palette: bytes) -> Image.Image:
    assert len(tile_data) == 960
    indices = bytearray(40 * 48)
    for tile_id in range(30):
        tile_y, tile_x = divmod(tile_id, 5)
        tile = tile_data[tile_id * 32:(tile_id + 1) * 32]
        for y in range(8):
            for x in range(8):
                mask = 1 << (7 - x)
                value = sum((int(bool(tile[2 * y + plane] & mask)) << plane) for plane in range(2))
                value |= sum((int(bool(tile[16 + 2 * y + plane] & mask)) << (plane + 2)) for plane in range(2))
                indices[(tile_y * 8 + y) * 40 + (tile_x * 8 + x)] = value
    img = Image.frombytes("P", (40, 48), bytes(indices))
    rgb = [c for triplet in palette_rgb(palette) for c in triplet]
    img.putpalette(rgb + [0] * (256 * 3 - 48))
    return img


def make_ips(source: bytes, dest: bytes) -> bytes:
    assert len(source) == len(dest) == 0x400000
    ips = bytearray(b"PATCH")
    offset = 0
    records = 0
    while offset < len(source):
        if source[offset] == dest[offset]:
            offset += 1
            continue
        start = offset
        while offset < len(source) and source[offset] != dest[offset] and offset - start < 0xFFFF:
            offset += 1
        length = offset - start
        assert 0 < length <= 0xFFFF
        ips.extend(start.to_bytes(3, "big"))
        ips.extend(length.to_bytes(2, "big"))
        ips.extend(dest[start:offset])
        records += 1
    ips.extend(b"EOF")
    return bytes(ips)


def apply_ips(source: bytes, patch: bytes) -> bytes:
    assert patch[:5] == b"PATCH" and patch[-3:] == b"EOF"
    out = bytearray(source)
    p = 5
    while p < len(patch) - 3:
        addr = int.from_bytes(patch[p:p + 3], "big")
        size = int.from_bytes(patch[p + 3:p + 5], "big")
        p += 5
        assert size != 0, "This patch intentionally does not use IPS RLE"
        out[addr:addr + size] = patch[p:p + size]
        p += size
    assert p == len(patch) - 3
    return bytes(out)


def main() -> None:
    sys.path.insert(0, str(WORK / "preflight"))
    from portrait_preflight import encode_snes4, protected

    baseline = SOURCE.read_bytes()
    assert len(baseline) == 0x400000 and digest(baseline) == EXPECTED_SHA256
    before_checksum = int.from_bytes(baseline[0xFFDE:0xFFE0], "little")
    assert before_checksum ^ int.from_bytes(baseline[0xFFDC:0xFFDE], "little") == 0xFFFF
    assert sum(baseline) % 65536 == before_checksum

    # Empirically prove the original Test47 raw-literal codec round-trips for
    # three independent existing fixed-face replacement packets.
    old_packets = {}
    for addr in (0x200000, 0x200500, 0x200A00):
        raw = read_literal_packet(baseline[addr:addr + 1083])
        assert make_literal_packet(raw) == baseline[addr:addr + 1083]
        old_packets[hex(addr)] = {"bytes": 1083, "roundtrip": True}

    # Assert preserved gameplay invariants from the source build.
    p = 0x219200
    assert baseline[p + 33 * 25 + 11] == 0
    assert baseline[p + 77 * 25 + 11] == 1
    assert [i for i in range(100) if baseline[p + i * 25 + 11]] == [77]
    original_protected = protected(baseline)

    output = bytearray(baseline)
    changes = {}
    for name in ("Rimbo", "Asmira"):
        img = Image.open(PNG[name])
        assert img.mode == "P" and img.size == (40, 48)
        raw = TILES[name].read_bytes()
        assert raw == encode_snes4(img) and len(set(img.tobytes())) <= 16
        palette = to_snes_palette(img)
        if name == "Asmira":
            expected = (WORK / "asmira/Asmira_Young_V1_CustomPalette_BGR555_32bytes.bin").read_bytes()
            assert palette == expected
        packet = make_literal_packet(raw)
        addr = PACKET_SLOTS[name]
        assert baseline[addr:addr + PACKET_ALLOC] == b"\xFF" * PACKET_ALLOC, (
            name, "target compressed-packet allocation is not blank"
        )
        assert addr + len(packet) <= addr + PACKET_ALLOC
        output[addr:addr + len(packet)] = packet
        pointer_bytes = (addr - POINTER_ORIGIN_PC).to_bytes(3, "little")
        previous = {}
        for face in FACE_SLOTS[name]:
            previous[str(face)] = {
                "old_graphics_pc": hex(face_ptr(baseline, face)),
                "old_pointer_hex": baseline[FACE_PTR_PC + face * 3:FACE_PTR_PC + face * 3 + 3].hex(),
                "old_palette_sha256": digest(baseline[FACE_PAL_PC + face * 32:FACE_PAL_PC + face * 32 + 32]),
            }
            output[FACE_PTR_PC + 3 * face:FACE_PTR_PC + 3 * face + 3] = pointer_bytes
            output[FACE_PAL_PC + 32 * face:FACE_PAL_PC + 32 * face + 32] = palette
        changes[name] = {
            "face_slots": list(FACE_SLOTS[name]),
            "graphics_PC": hex(addr),
            "pointer_bytes": pointer_bytes.hex(),
            "packet_length": len(packet),
            "reserved_block_length": PACKET_ALLOC,
            "raw_snes_4bpp_bytes": len(raw),
            "raw_graphics_SHA256": digest(raw),
            "custom_palette_BGR555_hex": palette.hex(),
            "old_face_slots": previous,
        }

    # Recompute the standard 4 MiB SNES checksum and its one's complement.
    output[0xFFDC:0xFFE0] = b"\x00" * 4
    check = (sum(output) + 4 * 0xFF // 2) & 0xFFFF
    # Two 16-bit complementary values sum to 510 when viewed bytewise.
    assert 4 * 0xFF // 2 == 510
    output[0xFFDC:0xFFDE] = (check ^ 0xFFFF).to_bytes(2, "little")
    output[0xFFDE:0xFFE0] = check.to_bytes(2, "little")
    assert sum(output) % 65536 == check
    assert int.from_bytes(output[0xFFDC:0xFFDE], "little") ^ check == 0xFFFF

    # Byte-level allowlist: only new packets, four 3-byte pointers, four
    # 32-byte individual palette entries, and checksum header can differ.
    allowed = set(range(0xFFDC, 0xFFE0))
    for name in ("Rimbo", "Asmira"):
        allowed.update(range(PACKET_SLOTS[name], PACKET_SLOTS[name] + 1083))
        for face in FACE_SLOTS[name]:
            allowed.update(range(FACE_PTR_PC + face * 3, FACE_PTR_PC + face * 3 + 3))
            allowed.update(range(FACE_PAL_PC + face * 32, FACE_PAL_PC + face * 32 + 32))
    actual = [i for i, (left, right) in enumerate(zip(baseline, output)) if left != right]
    assert actual and all(i in allowed for i in actual)
    # Precisely all 124 face-pointer bytes outside the four intended face IDs
    # remain unchanged, as do all 124 of the other per-face palette records.
    for face in range(128):
        if face in FACE_SLOTS["Rimbo"] + FACE_SLOTS["Asmira"]:
            continue
        assert baseline[FACE_PTR_PC + face * 3:FACE_PTR_PC + face * 3 + 3] == output[FACE_PTR_PC + face * 3:FACE_PTR_PC + face * 3 + 3]
        assert baseline[FACE_PAL_PC + face * 32:FACE_PAL_PC + face * 32 + 32] == output[FACE_PAL_PC + face * 32:FACE_PAL_PC + face * 32 + 32]
    # Protect every audited non-face game section byte-for-byte.
    final_protected = protected(output)
    for section, data in original_protected.items():
        if section == "fixed_face_pointers_128x3":
            continue
        assert data == final_protected[section], section

    # Validate actual ROM-side codec/palette on all four target aliases.
    verified_decoded = {}
    for name in ("Rimbo", "Asmira"):
        original_indices = Image.open(PNG[name]).tobytes()
        for face in FACE_SLOTS[name]:
            assert face_ptr(output, face) == PACKET_SLOTS[name]
            face_palette = bytes(output[FACE_PAL_PC + face * 32:FACE_PAL_PC + face * 32 + 32])
            assert face_palette == to_snes_palette(Image.open(PNG[name]))
            extracted_tiles = read_literal_packet(output[face_ptr(output, face):face_ptr(output, face) + 1083])
            assert extracted_tiles == TILES[name].read_bytes()
            image = decode_snes4(extracted_tiles, face_palette)
            assert image.tobytes() == original_indices
            verified_decoded[f"{name}_face{face}"] = image
    assert verified_decoded["Rimbo_face3"].tobytes() == verified_decoded["Rimbo_face24"].tobytes()
    assert verified_decoded["Asmira_face39"].tobytes() == verified_decoded["Asmira_face113"].tobytes()

    output_bytes = bytes(output)
    ips = make_ips(baseline, output_bytes)
    assert apply_ips(baseline, ips) == output_bytes, "IPS roundtrip failure"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / f"{STEM}.smc").write_bytes(output_bytes)
    (OUTPUT / f"{STEM}.ips").write_bytes(ips)

    # Render previews from the fully patched ROM, not from the original art.
    scale = 8
    sheet = Image.new("RGB", (800, 500), (29, 35, 39))
    draw = ImageDraw.Draw(sheet)
    for j, name in enumerate(("Rimbo", "Asmira")):
        img = verified_decoded[f"{name}_face{FACE_SLOTS[name][0]}"].convert("RGB")
        scaled = img.resize((40 * scale, 48 * scale), Image.Resampling.NEAREST)
        x, y = 40 + j * 400, 58
        sheet.paste(scaled, (x, y))
        draw.text((x, 19), f"{name} - Test48 ROM extraction", fill=(242, 238, 225))
        draw.text((x, 455), f"Fixed faces: {', '.join(map(str, FACE_SLOTS[name]))}", fill=(189, 200, 200))
    sheet.save(OUTPUT / f"{STEM}_ROM_Extracted_Preview.png")
    for key, img in verified_decoded.items():
        img.save(OUTPUT / f"{STEM}_{key}_40x48.png")

    original_face_slots = [3, 24, 39, 113]
    report = {
        "result": "STATIC VALIDATION PASS - GAMEPLAY TEST PENDING",
        "build_date": "2026-11-15",
        "source_test47_sha256": digest(baseline),
        "test48_rom_sha256": digest(output_bytes),
        "rom_size_bytes": len(output_bytes),
        "ips_sha256": digest(ips),
        "ips_roundtrip": "PASS",
        "gameplay_verified": False,
        "target_face_slots": original_face_slots,
        "other_fixed_face_pointers_unchanged": 124,
        "other_fixed_face_palettes_unchanged": 124,
        "changed_byte_count": len(actual),
        "changed_bytes_all_in_whitelist": True,
        "old_codecs_literal_only_roundtrip": old_packets,
        "new_codecs_raw_snes4bpp_roundtrip": "PASS",
        "output_face_palettes_match_approved_art": True,
        "source_protected_nonportrait_sections_unchanged": True,
        "test47_jong_shipyard_permission_preserved": {"Jepara_ID33": False, "Makassar_ID77": True},
        "old_test47_checksum": hex(before_checksum),
        "new_test48_checksum": hex(check),
        "portrait_changes": changes,
        "source_protected_section_sha256s": original_protected,
        "note": "No SNES emulator gameplay test was performed. Test45 remains gameplay-confirmed fallback; Test46 abandoned. No game character, navigator, script, port, fleet or shipyard values edited.",
    }
    (OUTPUT / f"{STEM}_Static_Audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    readme = f"""# UWNH US SNES Test48 - Rimbo V3 + Asmira V1 (experimental)

**ROM source:** corrected Test47 V8v4/V4 Makassar-Jong, SHA256 `{EXPECTED_SHA256}`.
**Test48 ROM SHA256:** `{digest(output_bytes)}`; exactly {len(output_bytes):,} bytes.
**Patch SHA256:** `{digest(ips)}`.

## Portrait changes only

- Fixed faces **3 and 24**: Rimbo Young V3 Enhanced Eyes, 40x48 pixels, 16-colour custom green-background palette. These address character-selection and profile/storyface references.
- Fixed faces **39 and 113**: Asmira Young V1, 40x48 pixels, 16-colour custom dark-green-background palette. These address scripted and profile references.
- Their four individual 32-byte SNES BGR555 palette records changed. No other palette record changed.
- Two separate 1,083-byte literal-encoded 4bpp packets added to previously blank Test47 0x500-byte allocations at PC 0x200F00 and 0x201400. Four 3-byte fixed-face pointers repointed to them.
- No character names, gameplay statistics, start locations, scripts, fleet rules, trade data, ships or port records changed.

## Static validation

- Exact corrected Test47 source SHA: PASS.
- Existing Test47 literal-only packet format reproduced byte-for-byte for three independent source packets: PASS.
- Both new images encode/decode at native 40x48 resolution with precise 16-colour index roundtrip: PASS.
- Test48 ROM extraction of all four fixed faces and per-face palettes: PASS.
- IPS applied back to source produces byte-identical Test48 ROM: PASS.
- All modified bytes fall within the two new packets, four pointer records, four 32-byte face palettes and four checksum bytes: PASS.
- All separately audited non-face gameplay ranges unchanged: PASS.
- SNES checksum/complement and full-ROM byte-sum verification: PASS.
- Makassar Jong sole port construction right preserved (port 77 enabled, Jepara port 33 disabled): PASS.

**This is an experimental ROM. Gameplay validation has NOT yet been performed.**
**Test45** remains the gameplay-confirmed fallback. **Test46** remains abandoned.

## Suggested user gameplay check (fresh New Game as Rimbo)

1. Open the character selection screen. Confirm Rimbo V3 appears instead of Ernst at the expected portrait face.
2. Start as Rimbo and open his status/character portrait. Confirm his skin, eye and smile colours look correct.
3. Advance to Asmira/Hans opening harbour dialogue. Confirm her V1 artwork appears with natural eyes and correct hair/skin colours.
4. Open Asmira's character/status portrait to check that this uses the same V1 art.
5. Move around the relocated Java Amsterdam, then check Makassar Jong shipyard availability and Jepara exclusivity if convenient; existing gameplay features should be unchanged.

**Scope reminder:** This build changes fixed 40x48 portrait images, not Ernst's or Hans's small walking-around-town sprite. That is a separate experiment; do not mistake unchanged roaming sprites for a failure of the fixed portrait import.
"""
    (OUTPUT / f"{STEM}_README.md").write_text(readme, encoding="utf-8")
    print(json.dumps({"result": report["result"], "test48_sha": report["test48_rom_sha256"], "changed_bytes": len(actual), "ips_bytes": len(ips), "output_dir": str(OUTPUT)}, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Test52: guarded, character-specific native town-walker graphics redirect.

Experimental because the game loader's dynamic caller has not been executed
in an emulator here. Only redirect the exact Ernst compressed gfx source bank
and pointer; all other characters, packets, palettes and portraits remain
byte-for-byte identical to gameplay-approved Test50.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).parent))
from decode_walker_lz import Decoder
from build_test50_user_selected import checksum_snes

ROOT = Path(__file__).parent
SOURCE = ROOT / 'output50/UWNH_Test50_Rimbo_Test5_Asmira_Face113_AllViews_EXPERIMENTAL_2026-11-15.smc'
SOURCE_SHA = '7fce9e4b3eef6d9f981fb965ba85a35aed7c6e54683efb96951f0ae5c14cad04'
OUT = ROOT / 'output52'
STEM = 'UWNH_Test52_Rimbo_Spear_ROM_SourceRedirect_ONLY_EXPERIMENTAL_2026-11-16'

DECOMP_ENTRY = 0x00A0BE
ROM_SPACE = 0x250100
WALKER_SOURCE_ERNST = 0x1BE5F2
WALKER_SOURCE_SPEAR = 0x1BB35F


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def emit_branch(blob: bytearray, marks: dict[str, int], fixups: list[tuple[int, str]], opcode: int, target: str):
    blob.append(opcode)
    pos = len(blob)
    blob.append(0)
    fixups.append((pos, target))


def hook_code() -> bytes:
    """Run the relocated original prologue and put selected source on stack.

    Avoid modifying source pointer $56; the original wrapper begins its normal
    destination/bank loading at $C0:A0C8. Register width and stack remain as
    expected at the continuation. This avoids altering the next sprite load.
    """
    b = bytearray()
    marks = {}
    fixups = []
    b += bytes.fromhex('C2 20 E2 10 3B 85 0A A5 56')
    b += bytes.fromhex('C9 F2 E5')  # cmp A16, exact Ernst offset $E5F2
    emit_branch(b, marks, fixups, 0xD0, 'original')
    b += bytes.fromhex('E2 20 A5 58 C9 DB C2 20')
    emit_branch(b, marks, fixups, 0xD0, 'original')
    b += bytes.fromhex('A9 5F B3')  # $DB:B35F native spear compressed image
    emit_branch(b, marks, fixups, 0x80, 'push')
    marks['original'] = len(b)
    b += bytes.fromhex('A5 56')
    marks['push'] = len(b)
    b += bytes.fromhex('48 5C C8 A0 C0')  # PHA; JML $C0:A0C8
    for where, label in fixups:
        delta = marks[label] - (where+1)
        assert -128 <= delta <= 127
        b[where] = delta & 0xFF
    assert len(b) == 36, len(b)
    return bytes(b)


def make_ips(old: bytes, new: bytes) -> bytes:
    """Tiny IPS creator, maximal contiguous differing runs (<=65535 each)."""
    assert len(old) == len(new)
    output = bytearray(b'PATCH')
    i = 0
    while i < len(old):
        if old[i] == new[i]:
            i += 1
            continue
        start = i
        while i < len(old) and old[i] != new[i] and i-start < 65535:
            i += 1
        output += start.to_bytes(3, 'big') + (i-start).to_bytes(2, 'big') + new[start:i]
    output += b'EOF'
    return bytes(output)


def apply_ips(old: bytes, ips: bytes) -> bytes:
    assert ips[:5] == b'PATCH' and ips[-3:] == b'EOF'
    out = bytearray(old)
    pos = 5
    while ips[pos:pos+3] != b'EOF':
        start = int.from_bytes(ips[pos:pos+3], 'big')
        length = int.from_bytes(ips[pos+3:pos+5], 'big')
        out[start:start+length] = ips[pos+5:pos+5+length]
        pos += 5+length
    return bytes(out)


def main():
    baseline = SOURCE.read_bytes()
    assert len(baseline) == 4*1024*1024 and sha(baseline) == SOURCE_SHA
    assert baseline[DECOMP_ENTRY:DECOMP_ENTRY+23] == bytes.fromhex(
        'C2 20 E2 10 3B 85 0A A5 56 48 A5 54 48 A5 58 E2 20 20 4C A2 C2 20 60')
    payload = hook_code()
    assert all(x == 0xFF for x in baseline[ROM_SPACE:ROM_SPACE+len(payload)])
    expected_source, orig_used = Decoder(baseline,WALKER_SOURCE_ERNST).decompress()
    spear_data, spear_used = Decoder(baseline,WALKER_SOURCE_SPEAR).decompress()
    assert len(expected_source) == len(spear_data) == 1024
    assert orig_used == 525 and spear_used == 579
    asset = (ROOT / 'town_walker_assets/rimbo_ernst_african_spear_SNES4bpp_8frames.bin').read_bytes()
    assert spear_data == asset

    patched = bytearray(baseline)
    # $C0:A0BE -> $E5:0100; new routine returns to the original $C0:A0C8.
    patched[DECOMP_ENTRY:DECOMP_ENTRY+4] = bytes.fromhex('5C 00 01 E5')
    patched[ROM_SPACE:ROM_SPACE+len(payload)] = payload
    checksum = checksum_snes(patched)
    result = bytes(patched)
    changed = [n for n,(a,b) in enumerate(zip(baseline, result)) if a!=b]
    allowed = set(range(DECOMP_ENTRY,DECOMP_ENTRY+4)) | set(range(ROM_SPACE,ROM_SPACE+len(payload))) | set(range(0xFFDC,0xFFE0))
    assert set(changed) <= allowed
    assert patched[WALKER_SOURCE_ERNST:WALKER_SOURCE_ERNST+525] == baseline[WALKER_SOURCE_ERNST:WALKER_SOURCE_ERNST+525]
    assert patched[WALKER_SOURCE_SPEAR:WALKER_SOURCE_SPEAR+579] == baseline[WALKER_SOURCE_SPEAR:WALKER_SOURCE_SPEAR+579]
    assert patched[0x200000:0x210000] == baseline[0x200000:0x210000], 'approved Test50 portraits changed'
    ips = make_ips(baseline, result)
    assert apply_ips(baseline,ips) == result
    assert ((patched[0xFFDC] | patched[0xFFDD]<<8) ^ checksum) == 65535
    OUT.mkdir(exist_ok=True)
    out_rom = OUT / (STEM+'.smc')
    out_ips = OUT / (STEM+'_from_Test50.ips')
    out_json = OUT / (STEM+'_AUDIT.json')
    out_readme = OUT / (STEM+'_READ_ME.txt')
    out_zip = OUT / (STEM+'.zip')
    out_rom.write_bytes(result)
    out_ips.write_bytes(ips)
    report = {
        'status': 'STATIC PASS; EXPERIMENTAL, REQUIRES FRESH GAMEPLAY TEST',
        'purpose': 'Use original native African spear holder graphic for Rimbo/Ernst in all eight movement frames; source-pointer hook, not save-state VRAM edit.',
        'warning': 'Asmira/Hans walking sprite unchanged; her original source packet remains unidentified.',
        'test50_source': {'filename': SOURCE.name,'sha256': sha(baseline)},
        'test52_rom': {'filename': out_rom.name,'sha256': sha(result),'bytes':len(result)},
        'ips': {'filename':out_ips.name,'sha256':sha(ips),'exact_roundtrip_pass':True},
        'hook': {'entry_pc':hex(DECOMP_ENTRY),'entry_before':'C2 20 E2 10',
                 'entry_after':'5C 00 01 E5', 'code_pc':hex(ROM_SPACE),'code_length':len(payload),
                 'code_hex':payload.hex(), 'return_snes':'$C0:A0C8',
                 'source_bank_guard':'$DB','source_offset_guard':'$E5F2','redirect_offset':'$B35F',
                 'preserves_dp_pointer_56': True},
        'source_packets': [{'walker':'original Ernst','pc':'0x1BE5F2','compressed_bytes':orig_used},
                           {'walker':'African spear','pc':'0x1BB35F','compressed_bytes':spear_used,
                            'identical_to_user_artwork':True}],
        'other_data': 'All other ROM bytes untouched except SNES checksum complement and checksum.',
        'changed_bytes':len(changed),'snes_checksum':hex(checksum),
        'changed_ranges':[hex(DECOMP_ENTRY)+'..'+hex(DECOMP_ENTRY+3),
                          hex(ROM_SPACE)+'..'+hex(ROM_SPACE+len(payload)-1),
                          '0xFFDC..0xFFDF'],
        'emulator_gameplay_status':'NOT TESTED',
    }
    out_json.write_text(json.dumps(report,indent=2)+'\n')
    out_readme.write_text(
        'UWNH Test52 — RIMBO WALKING SPRITE ROM SOURCE REDIRECT (EXPERIMENTAL)\n'
        '16 November 2026\n\n'
        'Test52 builds on exact Test50 and preserves its Rimbo Test5 and Asmira Face113 40x48 portraits.\n'
        'It hooks only source bank $DB, offset $E5F2 (green-haired Ernst), and redirects\n'
        'to native African spear-holder data bank $DB, offset $B35F. Both full eight-frame\n'
        'graphics streams remain unmodified. The output is a ROM, not patched save states.\n'
        'All non-target source pointers remain unchanged. This is a hypothesis that must\n'
        'be verified by actual gameplay: the generic decompressor wrapper is intercepted,\n'
        'but there is no emulator in this execution environment to validate that it is\n'
        'the path used for every town/building sprite load.\n\n'
        'IMPORTANT: Asmira/Hans walker is NOT YET REPLACED. Current screenshots and save\n'
        'states do not display the original Hans walker; his source packet/selection is\n'
        'still unknown. Her portrait remains correctly patched as in Test50.\n\n'
        'TEST (start a fresh New Game as Rimbo using THIS Test52 ROM, then):\n'
        ' 1. Look at Rimbo outdoors on the street. Expected African spear-holder.\n'
        ' 2. Enter a building; expected spear-holder indoors. Exit; expected spear-holder.\n'
        ' 3. Enter/exit the harbour and return to town. Expected spear-holder.\n'
        ' 4. Save in game, close emulator, reload; verify all directions after returning.\n'
        ' 5. Check Asmira Face113 portrait, dialogue, and other navigators still display.\n'
        'If no spear appears, provide the screen and (if possible) the emulator save state\n'
        'from this exact ROM; do not assume the hook was exercised.\n\n'
        'Do not mix Test50/Test51 savestates with this Test52 ROM when judging persistence.\n'
        'IPS applies ONLY to the exact Test50 ROM (SHA256 in the audit).\n'
    )
    with zipfile.ZipFile(out_zip,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in (out_rom,out_ips,out_json,out_readme):
            z.write(p,arcname=p.name)
    print(json.dumps({'rom':str(out_rom),'sha256':sha(result),'ips':str(out_ips),
                      'zip':str(out_zip),'changes':len(changed),'status':report['status']},indent=2))


if __name__ == '__main__':
    main()

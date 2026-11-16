#!/usr/bin/env python3
"""Test53: keep gameplay-PASS Test52 Rimbo hook and redirect only Hans art.

The Hans packet was verified pixel-for-pixel in the user screenshot at native
walker packet #120 (PC 0x1C5CB3, SNES $DC:5CB3).  The desired native Indian
woman asset is packet #33 (PC 0x1BCBD6, SNES $DB:CBD6).

Because the packets live in different banks, the Hans-only code supplies a
temporary bank in A to the native decompressor.  It does not mutate the RAM
source-bank byte $58.  Other callers jump to the intact Test52 hook.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import numpy as np
from PIL import Image

sys.path.insert(0,str(Path(__file__).parent))
from decode_walker_lz import Decoder
from build_test50_user_selected import checksum_snes
from build_test51_rimbo_source_redirect import make_ips,apply_ips
from extract_full_npc_anim_rows import tile_bytes_to_indices


ROOT=Path(__file__).parent
SOURCE=ROOT/'output52/UWNH_Test52_Rimbo_Spear_ROM_SourceRedirect_ONLY_EXPERIMENTAL_2026-11-16.smc'
SOURCE_SHA='3b325e989e95a9a3f1355cb1e20f8034c50289f6caaf7ad2ed9a8455fbc0e7ee'
OUT=ROOT/'output53'
STEM='UWNH_Test53_Rimbo_Spear_Asmira_IndianWoman_Walkers_EXPERIMENTAL_2026-11-16'

DECOMP_ENTRY=0x00A0BE
ORIGINAL_HOOK=0x250100
HANS_HOOK=0x250140
TRAMPOLINE=0x00A0C2
HANS_SRC=0x1C5CB3
INDIAN_SRC=0x1BCBD6
RIMBO_SRC=0x1BE5F2
SPEAR_SRC=0x1BB35F
CHECKSUM_POS=range(0xFFDC,0xFFE0)


def sha(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def hans_hook()->bytes:
    """Source-select Hans only, delegate all other work to original Test52."""
    code=bytearray()
    fix=[]
    labels={}
    def branch(op,target):
        code.extend((op,0))
        fix.append((len(code)-1,target))

    code+=bytes.fromhex('C2 20 E2 10 A5 56 C9 B3 5C') # 16A/8X; compare $5CB3
    branch(0xD0,'test52')
    code+=bytes.fromhex('E2 20 A5 58 C9 DC C2 20') # source bank must be $DC
    branch(0xD0,'test52')
    code+=bytes.fromhex('3B 85 0A')                 # relocated TSC;STA $0A
    code+=bytes.fromhex('A9 D6 CB 48')              # desired $DB:CBD6; PHA
    code+=bytes.fromhex('A5 54 48')                 # original dest; PHA
    code+=bytes.fromhex('A5 58 E2 20 A9 DB')        # load bank, replace low A only
    # JML, not JSL: the native decompressor pulls its JSR return address and
    # two data words directly off the stack. Any JSL return frame would corrupt
    # those parameters. C0:A0C2 performs JSR; REP20; RTS to the original caller.
    code+=bytes.fromhex('5C C2 A0 C0')              # JML native-bank trampoline
    labels['test52']=len(code)
    code+=bytes.fromhex('5C 00 01 E5')             # JML intact $E5:0100 hook
    for loc,target in fix:
        delta=labels[target]-(loc+1)
        assert -128<=delta<=127
        code[loc]=delta&0xff
    assert len(code)==45, len(code)
    return bytes(code)


def verify_exact_hans_screenshot(rom:bytes)->None:
    """Check the identified source against the screenshot's 3x native pixel grid.

    For each source index, every non-transparent pixel must have one consistent
    screenshot colour; all transparent pixels must be screenshot floor colours.
    This is a strong source-art match even though the room OBJ palette differs.
    """
    screen=np.array(Image.open(ROOT/'docx_walk4/word/media/image4.png').convert('RGB'))
    decoded,_=Decoder(rom,HANS_SRC,limit=1200).decompress()
    assert len(decoded)==1024
    indexes=np.zeros((16,16),np.uint8)
    for by in range(2):
        for bx in range(2):
            t=4+bx+16*by  # eight-frame source, facing front is frame 2
            tile=np.array(tile_bytes_to_indices(decoded,t*32),np.uint8).reshape(8,8)
            indexes[by*8:by*8+8,bx*8:bx*8+8]=tile
    xs=169+1+3*np.arange(16)
    ys=368+1+3*np.arange(16)
    observed=screen[ys[:,None],xs[None,:]]
    floor={(140,97,99),(156,142,140)}
    assert all(tuple(observed[y,x]) in floor for y,x in zip(*np.where(indexes==0)))
    for i in range(1,16):
        colours={tuple(v) for v in observed[indexes==i]}
        assert len(colours)<=1,(i,colours)


def main():
    original=SOURCE.read_bytes()
    assert len(original)==4*1024*1024 and sha(original)==SOURCE_SHA
    # Test52 entry redirects into the existing and gameplay-tested E5:0100 hook.
    assert original[DECOMP_ENTRY:DECOMP_ENTRY+4]==bytes.fromhex('5C 00 01 E5')
    assert original[TRAMPOLINE:TRAMPOLINE+6]==bytes.fromhex('3B 85 0A A5 56 48')
    test52_code=original[ORIGINAL_HOOK:ORIGINAL_HOOK+36]
    assert test52_code==bytes.fromhex(
        'C220E2103B850AA556C9F2E5D00FE220A558C9DBC220D005A95FB38002A556485CC8A0C0')
    code=hans_hook()
    assert all(x==0xff for x in original[HANS_HOOK:HANS_HOOK+len(code)])

    hans,hans_length=Decoder(original,HANS_SRC,limit=1200).decompress()
    woman,woman_length=Decoder(original,INDIAN_SRC,limit=1200).decompress()
    rimbo,rimbo_length=Decoder(original,RIMBO_SRC,limit=1200).decompress()
    spear,spear_length=Decoder(original,SPEAR_SRC,limit=1200).decompress()
    assert all(len(x)==1024 for x in (hans,woman,rimbo,spear))
    assert hans_length==463 and woman_length==485
    assert woman==(ROOT/'town_walker_assets/asmira_hans_indian_woman_SNES4bpp_8frames.bin').read_bytes()
    assert spear==(ROOT/'town_walker_assets/rimbo_ernst_african_spear_SNES4bpp_8frames.bin').read_bytes()
    verify_exact_hans_screenshot(original)

    output=bytearray(original)
    # Replace single JML entry target with independent Hans dispatcher.
    output[DECOMP_ENTRY:DECOMP_ENTRY+4]=bytes.fromhex('5C 40 01 E5')
    # Original entry's unreachable first four bytes become a native-bank
    # trampoline. JSR runs in bank C0 and consumes the exact native stack
    # layout; REP20; RTS then returns directly to the original game caller.
    output[TRAMPOLINE:TRAMPOLINE+6]=bytes.fromhex('20 4C A2 C2 20 60')
    output[HANS_HOOK:HANS_HOOK+len(code)]=code
    checksum=checksum_snes(output)
    result=bytes(output)

    changed={i for i,(a,b) in enumerate(zip(original,result)) if a!=b}
    allowed=set(range(DECOMP_ENTRY,DECOMP_ENTRY+4)) | set(range(TRAMPOLINE,TRAMPOLINE+6)) \
          | set(range(HANS_HOOK,HANS_HOOK+len(code))) | set(CHECKSUM_POS)
    assert changed<=allowed, sorted(changed-allowed)
    assert output[ORIGINAL_HOOK:ORIGINAL_HOOK+36]==test52_code,'Rimbo Test52 hook changed'
    assert output[0x200000:0x210000]==original[0x200000:0x210000], 'portraits changed'
    assert output[0x1B8D33:0x1D0000]==original[0x1B8D33:0x1D0000], 'sprite data changed'
    assert (output[0xFFDC]|output[0xFFDD]<<8)^checksum==65535
    ips=make_ips(original,result)
    assert apply_ips(original,ips)==result
    # Confirm all historical Test52 changes remain, save for its entry target.
    assert sha(output[0x250100:0x250124])==sha(original[0x250100:0x250124])

    OUT.mkdir(exist_ok=True)
    path_rom=OUT/(STEM+'.smc')
    path_ips=OUT/(STEM+'_from_Test52.ips')
    path_json=OUT/(STEM+'_AUDIT.json')
    path_readme=OUT/(STEM+'_READ_ME.txt')
    path_zip=OUT/(STEM+'.zip')
    path_rom.write_bytes(result)
    path_ips.write_bytes(ips)
    audit={
        'status':'STATIC PASS, GAMEPLAY NOT YET TESTED',
        'baseline':{'file':SOURCE.name,'sha256':sha(original)},
        'test53':{'file':path_rom.name,'sha256':sha(result),'bytes':len(result)},
        'ips':{'file':path_ips.name,'sha256':sha(ips),'roundtrip_exact':True},
        'hans_source':{'pc':'0x1C5CB3','snes':'$DC:5CB3','packet_index':120,
                       'compressed_bytes':hans_length,'user_screenshot_16x16_match':'PERFECT'},
        'asmira_desired':{'pc':'0x1BCBD6','snes':'$DB:CBD6','compressed_bytes':woman_length,
                          'decompressed_bytes':len(woman),'exact_asset_verified':True},
        'rimbo':{'current_source':'$DB:E5F2','redirect_to':'$DB:B35F',
                 'compressed_bytes':rimbo_length,'replacement_bytes':spear_length,
                 'test52_hook_unchanged':True,'test52_gameplay_result':'USER PASS'},
        'hook':{'dispatch_pc':'0xA0BE','hans_hook_pc':'0x250140','hans_hook_bytes':code.hex(),
                'test52_hook_pc':'0x250100','native_jsr_trampoline_pc':'0xA0C2',
                'trampoline_bytes':'20 4C A2 C2 20 60',
                'guard':'bank $DC AND offset $5CB3',
                'bank_override':'A low-byte set to $DB for native call; RAM $58 unchanged'},
        'changed_bytes':len(changed),
        'changed_offsets':list(map(hex,sorted(changed))),
        'snes_checksum':hex(checksum),
        'protected_sprite_streams_byte_identical':True,
        'portrait_region_byte_identical':True,
        'gameplay_status':'NOT TESTED (experimental)',
    }
    path_json.write_text(json.dumps(audit,indent=2)+'\n')
    path_readme.write_text(
        'Uncharted Waters: New Horizons — Test53 experimental ROM\n'
        'Rimbo African Spear + Asmira Indian-Woman Walking Sprites\n'
        '16 November 2026\n\n'
        'Built on exact user-gameplay-PASS Test52 ROM.\n'
        'Rimbo/Ernst: retains Test52 African spear-holder, 8 frames, unchanged hook.\n'
        'Asmira/Hans: replaces original blue-clothed character, 8 frames, with native\n'
        'Indian-woman art. The Hans source (PC 0x1C5CB3) was matched pixel-for-pixel\n'
        'against the actual Asmira dialogue screenshot; no guessed graphics slot.\n'
        'Both chosen custom 40x48 portraits are unchanged. All native sprite\n'
        'packets are unchanged; a guarded loader intercept selects the new art.\n\n'
        'STATIC PASS only; actual scene transitions and save/reload require testing.\n'
        'START A FRESH NEW GAME AS RIMBO USING THIS TEST53 ROM:\n'
        '  1. Confirm Rimbo still has African spear in all directions outside.\n'
        '  2. Visit the scene where Asmira speaks to him. Check her walking sprite\n'
        '     is Indian woman (rather than original blue-clothed Hans).\n'
        '  3. Leave the building, return, and repeat. Enter another building.\n'
        '  4. Use the game Save command, close emulator, reopen Test53, reload\n'
        '     the game save, and re-check Rimbo and Asmira.\n'
        '  5. Confirm Asmira Face113 portrait and Rimbo Test5 headband portrait.\n'
        '  6. Check unrelated NPCs and other navigators remain unchanged.\n'
        'NOTE: If Indian-woman graphics use Hans palette, her colours may vary;\n'
        '      report the screenshot and we can refine only her palette.\n'
        'Do not load older emulator save states to judge Test53. Game SRAM saves\n'
        'should remain the appropriate persistence test.\n\n'
        'The IPS applies ONLY to the exact Test52 ROM SHA256 in the audit.\n'
    )
    with zipfile.ZipFile(path_zip,'w',zipfile.ZIP_DEFLATED) as bundle:
        for path in (path_rom,path_ips,path_json,path_readme):
            bundle.write(path,arcname=path.name)
    print(json.dumps({'rom':str(path_rom),'sha256':sha(result),'zip':str(path_zip),
                      'changed':len(changed),'hook_bytes':len(code),'source_hans_exact':True},indent=2))


if __name__=='__main__':main()

#!/usr/bin/env python3
"""UWNH native 40x48 portrait preflight; intentionally READ-ONLY for the ROM.

Reproducible pixel-level quantisation, SNES 4bpp tile packing, and ROM face-index
reference audit, against the exact corrected Test47 build. This does NOT install
art into a ROM, claim an unused face is safe, or implement Koei graphics compression.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image

EXPECTED = '8f191a5bd426f85ad20e79d61b5c69f03da2b9512d31b5e26afed74c1264e192'
ROM_SIZE = 4194304
FACE_TABLE = 0x2BCB7
FACE_COUNT = 128
NAV_RECORDS = 120
NAV_BASE = 0x881F3
PALETTE_PC = 0xAAF00
WORKBOOK_NOTE = 'V4 choice columns I–K of original 64 Fleet Projection are authoritative.'

def sha(b):return hashlib.sha256(b).hexdigest()

def rom_palette(rom):
    def c(v):return v*255//31
    out=[]
    for i in range(16):
        raw=int.from_bytes(rom[PALETTE_PC+2*i:PALETTE_PC+2*i+2],'little')
        out.append((c(raw&31),c((raw>>5)&31),c((raw>>10)&31)))
    return out

def indexed_image(indices,palette):
    assert len(indices)==40*48 and all(0 <= x <16 for x in indices)
    img=Image.frombytes('P',(40,48),bytes(indices))
    full=[v for triplet in palette for v in triplet]+[0]*(256*3-16*3)
    img.putpalette(full)
    return img

def test_pattern(palette):
    # Diagnostic only: exactly 16 palette colours, simple 8-pixel tiles, not character artwork.
    pix=bytearray(40*48)
    for y in range(48):
        for x in range(40):
            tx,ty=x//8,y//8
            pix[y*40+x]=(tx+5*ty + (x%8)//4*3 + (y%8)//4*5)%16
    return indexed_image(pix,palette)

def normalise(img):
    if img.size==(120,144):
        rgba=img.convert('RGBA')
        # Only allow exact 3x nearest-neighbour expanded source, not smoothed preview.
        for y in range(48):
            for x in range(40):
                top=rgba.getpixel((3*x,3*y))
                for dy in range(3):
                    for dx in range(3):
                        if rgba.getpixel((3*x+dx,3*y+dy))!=top:
                            raise ValueError('120x144 input is not an exact nearest-neighbour 3x image')
        return rgba.resize((40,48),Image.Resampling.NEAREST)
    if img.size!=(40,48):
        raise ValueError(f'portrait dimensions {img.size} are not native 40x48')
    return img.convert('RGBA')

def quantise(img,palette):
    rgba=normalise(img)
    indices=bytearray()
    errors=[]
    for r,g,b,a in rgba.getdata():
        if a<128:
            indices.append(0)
            continue
        d=[(r-R)**2+(g-G)**2+(b-B)**2 for R,G,B in palette]
        best=min(range(16),key=d.__getitem__)
        indices.append(best)
        errors.append(d[best]**0.5)
    report={'source_dimensions':list(img.size), 'indexed_16_colours':True,
            'palette_entries_used':sorted(set(indices)),
            'max_colour_distance':round(max(errors,default=0),3),
            'pixels_with_non_exact_RGB':sum(e>0 for e in errors),
            'transparent_pixels_flipped_to_0':40*48-len(errors)}
    return indexed_image(indices,palette),report

def encode_snes4(img):
    if img.mode!='P' or img.size!=(40,48):raise ValueError('need native indexed portrait')
    p=img.tobytes(); out=bytearray()
    for ty in range(6):
        for tx in range(5):
            lo=bytearray(16);hi=bytearray(16)
            for y in range(8):
                for x in range(8):
                    idx=p[(ty*8+y)*40+tx*8+x]
                    if idx>15:raise ValueError('pixel exceeds 4bpp')
                    b=1<<(7-x)
                    for plane in range(2):
                        if idx & (1<<plane):lo[y*2+plane] |= b
                        if idx & (1<<(plane+2)):hi[y*2+plane] |= b
            out.extend(lo);out.extend(hi)
    assert len(out)==960
    return bytes(out)

def decode_snes4(data,palette):
    if len(data)!=960:raise ValueError('960 bytes required')
    p=bytearray(40*48)
    for tile in range(30):
        y0,x0=divmod(tile,5);tiledata=data[32*tile:32*tile+32]
        for y in range(8):
            for x in range(8):
                bit=7-x
                v=sum(((tiledata[y*2+plane]>>bit)&1)<<plane for plane in range(2))
                v+=sum(((tiledata[16+y*2+plane]>>bit)&1)<<(plane+2) for plane in range(2))
                p[(y0*8+y)*40+x0*8+x]=v
    return indexed_image(p,palette)

def nav_audit(rom,out):
    raw=[]
    for i in range(NAV_RECORDS):
        face=int.from_bytes(rom[NAV_BASE+i*50+26:NAV_BASE+i*50+28],'little')
        raw.append((i,face))
    f=collections.defaultdict(list)
    for i,face in raw:
        if face<128:f[face].append(i)
    pointers={i:rom[FACE_TABLE+3*i:FACE_TABLE+3*i+3].hex() for i in range(128)}
    dup=collections.defaultdict(list)
    for i,h in pointers.items():dup[h].append(i)
    used_fixed=set(f)
    with (out/'Test48_FixedFace_Use_Inventory.csv').open('w',newline='',encoding='utf-8')as io:
        w=csv.writer(io)
        w.writerow(['Fixed face index','Pointer PC','Pointer bytes','Navigator IDs referencing','Navigator count', 'Caution'])
        for i in range(FACE_COUNT):
            w.writerow([i,hex(FACE_TABLE+3*i),pointers[i],', '.join(map(str,f[i])),len(f[i]),'NOT proof of script-wide disuse' if not f[i] else 'Referenced by navigator record'])
    with (out/'Test48_Navigator_Face_Inventory.csv').open('w',newline='',encoding='utf-8') as io:
        w=csv.writer(io);w.writerow(['Navigator ID','Raw face code decimal','Raw face code hex','Face family'])
        for i,v in raw:w.writerow([i,v,hex(v),'Fixed' if v<128 else 'Tile-composed'])
    return {'navigators':120,'navigator_face_codes_unique':len(set(y for x,y in raw)),
            'fixed_face_slots_used_by_navigators':len(used_fixed),
            'fixed_face_slots_not_used_by_navigators':[i for i in range(128) if i not in used_fixed],
            'duplicate_fixed_pointer_groups':[ls for ls in dup.values() if len(ls)>1],
            'note':'Unused by 120 navigator records DOES NOT mean safe: story/selection/ruler portraits also reference fixed face slots.'}

def protected(rom):
    sections={
        'ship_specs_25x12':(0x08CE27,25*12),
        'ship_industry_gates_25x2':(0x219E00,25*2),
        'extended_ship_prices_25x4':(0x3E8100,25*4),
        'NPC_rule_bytes_63x2':(0x09EC4D,63*2),
        'NPC_initial_fleets_70x133':(0x089DB2,70*133),
        'fixed_face_pointers_128x3':(FACE_TABLE,128*3),
        'fixed_palette_16x2':(PALETTE_PC,16*2),
        'port_records_100x37':(0x08DA7F,100*37),
        'shipyard_permissions_100x25':(0x219200,100*25),
        'original_town_style_100':(0xB353E,100),
        'original_town_palette_100':(0xB35A7,100),
        'political_records_100x22':(0x08CF53,100*22),
        'character_records_120x50':(NAV_BASE,NAV_RECORDS*50),
    }
    return {name:{'pc_start':hex(off),'size_bytes':ln,'sha256':sha(rom[off:off+ln])} for name,(off,ln)in sections.items()}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rom',type=Path,required=True)
    ap.add_argument('--png',type=Path,help='User art (native 40x48 or exact NN 120x144)')
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    rom=args.rom.read_bytes()
    assert len(rom)==ROM_SIZE,(len(rom),ROM_SIZE)
    assert sha(rom)==EXPECTED,'Only corrected Test47 SHA allowed. Never use abandoned Test46.'
    checksum=int.from_bytes(rom[0xFFDE:0xFFE0],'little')
    complement=int.from_bytes(rom[0xFFDC:0xFFDE],'little')
    assert checksum^complement==0xFFFF and sum(rom)%65536==checksum
    # Jepara and Makassar patch invariant.
    perm=0x219200
    assert rom[perm+33*25+11]==0 and rom[perm+77*25+11]==1
    assert [i for i in range(100) if rom[perm+25*i+11]]==[77]
    palette=rom_palette(rom)
    if args.png:
        input_img=Image.open(args.png)
    else:
        input_img=test_pattern(palette)
    indexed,stats=quantise(input_img,palette)
    raw=encode_snes4(indexed)
    assert decode_snes4(raw,palette).tobytes()==indexed.tobytes()
    indexed.save(args.out/'Test48_Portrait_40x48_Indexed.png')
    indexed.resize((200,240),Image.Resampling.NEAREST).save(args.out/'Test48_Portrait_5x_NearestPreview.png')
    (args.out/'Test48_Portrait_Uncompressed_SNES4bpp_960bytes.bin').write_bytes(raw)
    inv=nav_audit(rom,args.out)
    m={'status':'PASS: ROM baseline, palette, exact 4bpp roundtrip; NO ROM PATCH MADE',
       'source_rom_sha256':EXPECTED,'rom_bytes':len(rom),
       'source_art':str(args.png.name) if args.png else 'technical palette diagnostic pattern (NOT user-approved artwork)',
       'art_input_report':stats,'raw_tile_count':30,'raw_sprite_bytes':960,
       'raw_sprite_sha256':sha(raw),'roundtrip_pixels_exact':True,
       'jepara_jong_permission':False,'makassar_jong_permission':True,
       'workbook_guidance':WORKBOOK_NOTE,
       'palette_RGB8':palette,'navigator_audit':inv,'protected_section_baseline_digests':protected(rom),
       'known_unfinished':'Koei compressed sprite writer, safe fixed-slot allocation and all scripted references; do not create a ROM from this packet without resolving these.',
       'gameplay_tested':False}
    (args.out/'Test48_Portrait_Preflight_Audit.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:m[k] for k in ('status','source_rom_sha256','source_art','raw_sprite_bytes','roundtrip_pixels_exact')},indent=2))
if __name__=='__main__':main()

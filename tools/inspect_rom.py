#!/usr/bin/env python3
"""Read-only validator for selected US SNES UWNH project structures.

It deliberately does not write or patch any commercial game content.
Do not use the addresses below with unknown-region or headered builds.
"""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

PORT_BASE=0x08DA7F
PORT_STRIDE=37
PRICE_BASE=0x240000
PRICE_STRIDE=128
SHIP_BASE=0x08CE27


def read_u16(b:bytes, pos:int)->int:
    return int.from_bytes(b[pos:pos+2],"little")


def inspect(b:bytes, port:int, good:int, ship:int)->dict:
    if len(b)!=4194304:
        raise ValueError(f"Expected an exact 4 MiB, headerless project ROM; got {len(b)} bytes")
    if not (0<=port<100 and 0<=good<46 and 0<=ship<25):
        raise ValueError("Port must be 0..99, good 0..45, ship 0..24")
    ck=read_u16(b,0xFFDE)
    inv=read_u16(b,0xFFDC)
    pn=PORT_BASE+PORT_STRIDE*port
    pr=PRICE_BASE+PRICE_STRIDE*port+2*good
    sh=SHIP_BASE+12*ship
    return {
        "size":len(b),"sha256":hashlib.sha256(b).hexdigest(),
        "checksum_header":f"0x{ck:04X}","complement_header":f"0x{inv:04X}",
        "checksum_complement_consistent":(ck^inv)==0xFFFF,
        "checksum_sum_consistent":sum(b)&0xFFFF==ck,
        "port":{"id":port,"record_pc":f"0x{pn:06X}","special_item_slot":b[pn+32],
                "autosail_geographic_region":b[pn+33],"shipyard_region":b[pn+34]},
        "resale_quote":{"good_id":good,"pc":f"0x{pr:06X}","little_endian_u16":read_u16(b,pr)},
        "ship":{"model_id":ship,"pc":f"0x{sh:06X}","tack_byte":b[sh+2],
                "sailing_byte":b[sh+3],"raw_12_bytes":b[sh:sh+12].hex()},
    }


def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("rom",type=Path,help="Your locally owned 4 MiB headerless UWNH ROM")
    ap.add_argument("--port",type=int,default=33)
    ap.add_argument("--good",type=int,default=0)
    ap.add_argument("--ship",type=int,default=11)
    a=ap.parse_args()
    print(json.dumps(inspect(a.rom.read_bytes(),a.port,a.good,a.ship),indent=2))

if __name__=="__main__":main()

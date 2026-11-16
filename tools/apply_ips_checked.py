#!/usr/bin/env python3
"""Apply an IPS only if the specified parent ROM SHA-256 matches exactly.

No ROM or patch is distributed with this tool. Refuses header size mismatch,
IPS RLE/truncation and output overwrite. Standard IPS can only encode 24-bit
positions; project patches must stay within its representable range.
"""

from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()

def patch_bytes(source:bytes,ips:bytes)->bytes:
    if not ips.startswith(b"PATCH") or not ips.endswith(b"EOF"):
        raise ValueError("Not a supported standard IPS with terminal EOF")
    out=bytearray(source)
    pos=5
    end=len(ips)-3
    while pos<end:
        if pos+5>end:raise ValueError("Truncated IPS record header")
        addr=int.from_bytes(ips[pos:pos+3],"big")
        size=int.from_bytes(ips[pos+3:pos+5],"big")
        pos+=5
        if size==0:
            if pos+3>end:raise ValueError("Truncated IPS RLE record")
            run=int.from_bytes(ips[pos:pos+2],"big")
            payload=ips[pos+2:pos+3]*run
            pos+=3
        else:
            if pos+size>end:raise ValueError("Truncated IPS raw record")
            payload=ips[pos:pos+size]
            pos+=size
        if addr+len(payload)>len(out):raise ValueError("IPS write extends past source ROM")
        out[addr:addr+len(payload)]=payload
    if pos!=end:raise ValueError("Extra IPS bytes")
    return bytes(out)

def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("rom",type=Path)
    ap.add_argument("ips",type=Path)
    ap.add_argument("output",type=Path)
    ap.add_argument("--source-sha256",required=True)
    ap.add_argument("--expected-output-sha256",required=True)
    a=ap.parse_args()
    if a.output.exists():raise SystemExit("Output already exists; refusing overwrite")
    parent=a.rom.read_bytes()
    if len(parent)!=0x400000:raise SystemExit("Expected 4 MiB headerless source")
    if sha(parent).lower()!=a.source_sha256.lower():raise SystemExit("Source SHA-256 mismatch")
    result=patch_bytes(parent,a.ips.read_bytes())
    if sha(result).lower()!=a.expected_output_sha256.lower():raise SystemExit("Output SHA-256 mismatch")
    a.output.write_bytes(result)
    print("Verified output:",a.output,sha(result))

if __name__=="__main__":main()

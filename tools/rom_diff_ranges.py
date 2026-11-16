#!/usr/bin/env python3
"""Report contiguous byte differences and exact SHA-256 fingerprints.

Read-only. Use changed-region output to build a strict allowlist before patching.
"""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

def regions(a:bytes,b:bytes):
    if len(a)!=len(b):raise ValueError("Different file sizes")
    out=[]
    i=0
    while i<len(a):
        if a[i]==b[i]:i+=1;continue
        start=i
        while i<len(a) and a[i]!=b[i]:i+=1
        out.append({"start":hex(start),"last":hex(i-1),"bytes":i-start})
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("before",type=Path)
    ap.add_argument("after",type=Path)
    x=ap.parse_args()
    a=x.before.read_bytes();b=x.after.read_bytes()
    r=regions(a,b)
    print(json.dumps({"source_sha256":hashlib.sha256(a).hexdigest(),
      "output_sha256":hashlib.sha256(b).hexdigest(),"changed_bytes":sum(v["bytes"] for v in r),
      "regions":r},indent=2))

if __name__=="__main__":main()

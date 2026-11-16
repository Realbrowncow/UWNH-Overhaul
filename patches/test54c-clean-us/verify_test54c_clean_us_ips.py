#!/usr/bin/env python3
"""Read-only independent IPS replay and output-hash verifier (no ROM output)."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import struct

CLEAN_SHA = "64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0"
TEST_SHA = "924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify(source_path: Path, patch_path: Path) -> None:
    source = source_path.read_bytes()
    patch = memoryview(patch_path.read_bytes())
    assert len(source) == 0x200000 and sha(source) == CLEAN_SHA
    assert bytes(patch[:5]) == b"PATCH"
    # This independent replay deliberately starts with a 4 MiB zero-filled
    # buffer to catch any uncovered bytes in the extension.
    output = bytearray(0x400000)
    output[:len(source)] = source
    cursor = 5
    seen = 0
    while bytes(patch[cursor:cursor+3]) != b"EOF":
        assert cursor + 5 < len(patch)
        at = int.from_bytes(patch[cursor:cursor+3], "big")
        count = struct.unpack_from(">H", patch, cursor+3)[0]
        cursor += 5
        if count:
            assert cursor + count <= len(patch)
            output[at:at+count] = patch[cursor:cursor+count]
            cursor += count
        else:
            count = struct.unpack_from(">H", patch, cursor)[0]
            value = patch[cursor+2]
            output[at:at+count] = bytes([value]) * count
            cursor += 3
        seen += 1
    assert bytes(patch[cursor:cursor+3]) == b"EOF"
    assert int.from_bytes(patch[cursor+3:cursor+6], "big") == 0x400000
    assert cursor + 6 == len(patch)
    assert len(output) == 0x400000
    assert sha(output) == TEST_SHA
    print(f"INDEPENDENT STATIC PASS: {seen} records; output SHA256 {sha(output)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("patch", type=Path)
    args = parser.parse_args()
    verify(args.source, args.patch)

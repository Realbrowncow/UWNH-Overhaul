#!/usr/bin/env python3
"""Read-only verifier for the exact private Test54b -> Test54c ROM transition.

The commercial ROM and modified ROMs are deliberately NOT distributed with
this public research repository. This script imports only Python stdlib.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PARENT_SHA256 = "712fa01718857fe8398d7c6808c04674e60a0ff7ed0021e23e86ace524f7b7ba"
TEST54C_SHA256 = "924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01"
ROM_SIZE = 4_194_304
CHANGED_BYTES_EXPECTED = 164

# (Headerless PC address, original visible string length, approved new text)
TEXT_FIELDS = [
    (
        0x0EBC25,
        148,
        "Rimbo, a young captain from Demak, charts distant seas for Mercator. "
        "With Asmira at his side, he seeks new horizons and adventure.",
    ),
    (0x0B619B, 61, "Demak sea captain. His friend Mercator asks him"),
    (
        0x0EB9A2,
        62,
        " to explore far-off lands and make a map of the entire world.",
    ),
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_checksum(data: bytes) -> None:
    expected = int.from_bytes(data[0xFFDE:0xFFE0], "little")
    complement = int.from_bytes(data[0xFFDC:0xFFDE], "little")
    assert sum(data) & 0xFFFF == expected, "Invalid SNES checksum"
    assert expected ^ complement == 0xFFFF, "Invalid SNES complement"


def check_files(parent: bytes, result: bytes) -> dict:
    assert len(parent) == len(result) == ROM_SIZE, "Expected headerless 4 MiB ROMs"
    assert sha256(parent) == PARENT_SHA256, "Parent is not exact Test54b"
    assert sha256(result) == TEST54C_SHA256, "Output is not exact Test54c"
    check_checksum(parent)
    check_checksum(result)

    allowed = set(range(0xFFDC, 0xFFE0))
    findings = []
    for offset, original_len, new_text in TEXT_FIELDS:
        new_bytes = new_text.encode("ascii")
        assert len(new_bytes) <= original_len, "Replacement exceeds original limit"
        assert parent[offset - 1] == 0, "Source string lacks left NUL boundary"
        assert parent[offset + original_len] == 0, "Source string lacks trailing NUL"
        assert parent.find(b"\x00", offset) - offset == original_len, "Unexpected source length"
        assert result[offset:offset + len(new_bytes)] == new_bytes, "New text does not match"
        assert result[offset + len(new_bytes)] == 0, "Result is not NUL terminated"
        # Preserve bytes beyond the inserted terminator, including the old tail.
        assert result[offset + len(new_bytes) + 1:offset + original_len + 1] == (
            parent[offset + len(new_bytes) + 1:offset + original_len + 1]
        )
        allowed.update(range(offset, offset + original_len + 1))
        findings.append({"pc_offset": hex(offset), "original_max": original_len, "new_chars": len(new_bytes)})

    differences = [pos for pos, (a, b) in enumerate(zip(parent, result)) if a != b]
    assert len(differences) == CHANGED_BYTES_EXPECTED, "Wrong number of changed bytes"
    assert set(differences) <= allowed, "Changes escaped three text regions/checksum"
    assert result[0x0B7601:0x0B7E42] == parent[0x0B7601:0x0B7E42], (
        "A shipyard description changed unexpectedly"
    )
    assert result[0x04DF31:0x04DF36] == parent[0x04DF31:0x04DF36] == b"Ernst", (
        "Unrelated Ernst dialogue was changed"
    )
    assert parent[0x88289:0x8828E] == result[0x88289:0x8828E] == b"Rimbo"

    return {
        "status": "STATIC PASS",
        "parent_sha256": sha256(parent),
        "test54c_sha256": sha256(result),
        "changed_byte_count": len(differences),
        "fields": findings,
        "notes": "Heading ~Ernst~ remains unresolved and is not fixed by Test54c",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("test54b", type=Path, help="exact private Test54b ROM")
    parser.add_argument("test54c", type=Path, help="exact private Test54c ROM")
    args = parser.parse_args()
    report = check_files(args.test54b.read_bytes(), args.test54c.read_bytes())
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

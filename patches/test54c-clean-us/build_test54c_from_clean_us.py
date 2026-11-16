#!/usr/bin/env python3
"""Build a reproducible IPS from verified clean US retail ROM to Test54c.

The input images are read-only. The 2 MiB -> 4 MiB expansion is encoded in
both explicit IPS records for every byte in the expanded half, and the
standard optional EOF three-byte final-size field. No copyrighted ROM is
included in the resulting deliverables.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


CLEAN_SHA = "64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0"
TEST54C_SHA = "924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01"
CLEAN_SIZE = 2_097_152
TARGET_SIZE = 4_194_304
IPS_NAME = "UWNH_Test54c_CUMULATIVE_from_Clean_US_ROM_2026-11-16.ips"


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def encode_ips(clean: bytes, target: bytes) -> tuple[bytes, dict]:
    assert len(clean) == CLEAN_SIZE and len(target) == TARGET_SIZE
    result = bytearray(b"PATCH")
    pos = 0
    raw_records = rle_records = 0
    raw_bytes = rle_bytes = 0

    # First half requires writing only changed bytes. The expanded upper half
    # is written IN FULL, avoiding assumptions about a patcher's fill byte.
    def write_needed(i: int) -> bool:
        return i >= CLEAN_SIZE or clean[i] != target[i]

    def run_length(i: int, limit: int) -> int:
        value = target[i]
        end = i + 1
        while end < limit and write_needed(end) and target[end] == value:
            end += 1
        return end - i

    while pos < TARGET_SIZE:
        if not write_needed(pos):
            pos += 1
            continue

        remaining = min(TARGET_SIZE - pos, 65535)
        run = run_length(pos, pos + remaining)
        if run >= 8:
            result.extend(pos.to_bytes(3, "big"))
            result.extend(b"\x00\x00")
            result.extend(run.to_bytes(2, "big"))
            result.append(target[pos])
            rle_records += 1
            rle_bytes += run
            pos += run
            continue

        start = pos
        pos += 1
        while pos - start < 65535 and pos < TARGET_SIZE and write_needed(pos):
            check_until = min(TARGET_SIZE, pos + 8)
            if check_until - pos == 8 and run_length(pos, check_until) == 8:
                break
            pos += 1
        size = pos - start
        result.extend(start.to_bytes(3, "big"))
        result.extend(size.to_bytes(2, "big"))
        result.extend(target[start:pos])
        raw_records += 1
        raw_bytes += size

    # IPS supports 24-bit output size. 0x400000 is representable.
    result.extend(b"EOF")
    result.extend(TARGET_SIZE.to_bytes(3, "big"))
    assert raw_bytes + rle_bytes >= TARGET_SIZE - CLEAN_SIZE
    return bytes(result), {
        "raw_records": raw_records,
        "raw_bytes": raw_bytes,
        "rle_records": rle_records,
        "rle_expanded_bytes": rle_bytes,
    }


def replay_ips(clean: bytes, patch: bytes) -> bytes:
    """Independent decoder supporting short source, RLE, and EOF resizing."""
    assert patch[:5] == b"PATCH"
    output = bytearray(clean)
    offset = 5
    while True:
        assert offset + 3 <= len(patch)
        if patch[offset:offset + 3] == b"EOF":
            offset += 3
            if offset + 3 == len(patch):
                new_size = int.from_bytes(patch[offset:offset + 3], "big")
                if new_size > len(output):
                    output.extend(b"\x00" * (new_size - len(output)))
                else:
                    del output[new_size:]
                offset += 3
            assert offset == len(patch)
            return bytes(output)
        addr = int.from_bytes(patch[offset:offset + 3], "big")
        size = int.from_bytes(patch[offset + 3:offset + 5], "big")
        offset += 5
        if size:
            assert offset + size <= len(patch)
            content = patch[offset:offset + size]
            offset += size
        else:
            assert offset + 3 <= len(patch)
            count = int.from_bytes(patch[offset:offset + 2], "big")
            content = patch[offset + 2:offset + 3] * count
            offset += 3
        if addr + len(content) > len(output):
            output.extend(b"\x00" * (addr + len(content) - len(output)))
        output[addr:addr + len(content)] = content


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    clean = args.source.read_bytes()
    target = args.target.read_bytes()
    assert len(clean) == CLEAN_SIZE and digest(clean) == CLEAN_SHA, "Wrong retail US ROM"
    assert len(target) == TARGET_SIZE and digest(target) == TEST54C_SHA, "Wrong Test54c ROM"

    ips, record_stats = encode_ips(clean, target)
    rebuilt = replay_ips(clean, ips)
    assert rebuilt == target and digest(rebuilt) == TEST54C_SHA, "IPS replay mismatch"

    args.out.mkdir(parents=True, exist_ok=True)
    patch_path = args.out / IPS_NAME
    patch_path.write_bytes(ips)
    audit = {
        "status": "STATIC PASS; clean 2MiB US original to exact 4MiB Test54c",
        "source_file": "Uncharted Waters - New Horizons (U).smc",
        "source_bytes": len(clean),
        "source_sha256": CLEAN_SHA,
        "target_file": args.target.name,
        "target_bytes": len(target),
        "target_sha256": TEST54C_SHA,
        "rom_expansion": "2MiB to 4MiB; explicit upper-half writes and IPS EOF final-size tag",
        "patch_file": IPS_NAME,
        "patch_bytes": len(ips),
        "patch_sha256": digest(ips),
        "first_2MiB_changed_bytes": sum(a != b for a, b in zip(clean, target)),
        "upper_2MiB_non_ff_bytes": sum(b != 255 for b in target[CLEAN_SIZE:]),
        "record_stats": record_stats,
        "ips_replay_exact": rebuilt == target,
        "gameplay_status": "Encoding verified statically; full Test54c gameplay regression still pending",
        "known_issue": "Rimbo biography screen heading ~Ernst~ remains unresolved",
    }
    (args.out / "UWNH_Test54c_Clean_US_IPS_Audit_2026-11-16.json").write_text(
        json.dumps(audit, indent=2) + "\n", encoding="utf-8"
    )
    readme = f"""# Uncharted Waters: New Horizons — Test54c cumulative IPS (clean US original)

This release contains a **patch, not a ROM**. The IPS applies directly to the
**unmodified US SNES** ROM you must supply yourself. It incorporates all changes
in Ken Chee's Test54c experimental build, including the earlier ten-ship manual
control change. No separate earlier patch is needed.

## Exact compatibility

| Item | SHA-256 | Size |
|---|---|---|
| Required headerless original US ROM | `{CLEAN_SHA}` | 2,097,152 bytes (2 MiB) |
| Resulting Test54c ROM | `{TEST54C_SHA}` | 4,194,304 bytes (4 MiB) |
| This IPS patch | `{digest(ips)}` | {len(ips):,} bytes |

The IPS writes the expanded upper half explicitly and carries the standard IPS
EOF output-size extension. **Use a patcher that supports IPS RLE and ROM size
expansion**; verify your output SHA-256 before playing. Do not apply this to a
512-byte-headered ROM, the earlier `(...patched).smc` project ROM, or any
Test53/Test54 intermediate.

## How to apply

1. Make a copy of your legally obtained headerless US original ROM.
2. Verify the original has the exact size and SHA-256 above.
3. Open a compatible IPS patcher (for example, Floating IPS) and select this IPS.
4. Patch the copy of the original ROM, choosing a separate output filename.
5. Verify the 4 MiB resulting file has the exact Test54c SHA-256 above.
6. Load the patched file in your SNES emulator. Keep backups of game saves, and
   avoid transferring emulator save states between different ROM versions.

## Scope and limitations

- **Static patch verification: PASS.** Independent IPS replay yielded exactly
  the byte-identical Test54c target ROM.
- Previous Test54c screenshots verified Rimbo's refined biography and intro
  wording; broader gameplay regression is not claimed.
- The biography heading showing `~Ernst~` is still an unresolved known issue.
- This is an experimental ROM hack and is not affiliated with the game's
  original developers or publisher.

Only the patch and supporting documentation may be shared; do not upload the
original or modified ROM image as part of this patch package.
"""
    (args.out / "README_Test54c_Clean_US_IPS_2026-11-16.md").write_text(readme, encoding="utf-8")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()

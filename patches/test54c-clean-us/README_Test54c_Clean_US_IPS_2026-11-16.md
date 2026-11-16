# Uncharted Waters: New Horizons — Test54c cumulative IPS (clean US original)

This release contains a **patch, not a ROM**. The IPS applies directly to the
**unmodified US SNES** ROM you must supply yourself. It incorporates all changes
in Ken Chee's Test54c experimental build, including the earlier ten-ship manual
control change. No separate earlier patch is needed.

## Exact compatibility

| Item | SHA-256 | Size |
|---|---|---|
| Required headerless original US ROM | `64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0` | 2,097,152 bytes (2 MiB) |
| Resulting Test54c ROM | `924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01` | 4,194,304 bytes (4 MiB) |
| This IPS patch | `b92debc2c64dc10a0570f6da9eca182565b35e13de2caeef125bf4b3eb149286` | 88,565 bytes |

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

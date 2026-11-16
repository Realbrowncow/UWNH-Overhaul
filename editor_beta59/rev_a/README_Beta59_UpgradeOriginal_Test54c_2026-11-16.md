# New Horizons World, Ship & Fleet Studio — Beta 5.9 Rev A

**New function: Upgrade Original ROM to Test54c.** This is Ken Chee's private experimental editor. The existing Beta 5.9 editing functions are preserved, and the previous Beta 5.9 release remains a separate fallback.

## What you receive

1. **Separate cumulative IPS:** `UWNH_Test54c_CUMULATIVE_from_Clean_US_ROM_2026-11-16.ips`. You can apply it to a clean US original with a compatible IPS patcher, without using this editor.
2. **Private editor:** `New_Horizons_World_Ship_Fleet_Studio_Beta_5_9_Test54c_UpgradeOriginal_RevA.html`. Its first sidebar panel now upgrades a local clean US ROM to the exact Test54c image and downloads the result.
3. **ROM-free source package:** Python builder, JavaScript module, HTML panel and independent regression tester. This package is appropriate for code review and public research distribution; it excludes the private embedded-ROM editor and all ROM files.

## Upgrade using Beta 5.9 Rev A

1. Open the **private HTML editor** in a modern browser on your own computer. No web service is required.
2. In **Upgrade Original ROM to Test54c**, choose your own unmodified, headerless 2 MiB US `Uncharted Waters: New Horizons` `.smc` or `.sfc` file.
3. Click **Verify and Create Test54c**.
4. The editor verifies the clean original SHA-256, verifies the embedded cumulative IPS, applies all IPS normal/RLE records (including ROM expansion to 4 MiB), and verifies the result is exactly Test54c.
5. On success, it initiates a download called `UWNH_Test54c_from_Clean_US_Verified.smc`. Keep the original ROM unchanged. You can then use the Test54c editor controls, starting with **Load bundled Test54c**, or load your downloaded file through **Choose exact Test54c ROM**.

Wrong-region, altered, previously patched, headered, or otherwise incompatible ROMs are refused. A failed verification cannot trigger a download.

## Upgrade using only the standalone IPS

1. Make a backup copy of your legally obtained, headerless US original.
2. Use a patcher with **IPS RLE and output-size expansion** support, such as Floating IPS, to apply the **cumulative** Test54c `.ips` to that backup copy.
3. Confirm the output is exactly 4,194,304 bytes with the SHA-256 listed below. It is not necessary to apply earlier project IPS files first.

## Exact hashes

| Asset | Bytes | SHA-256 |
|---|---:|---|
| Clean US original, required input | 2,097,152 | `64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0` |
| Standalone cumulative IPS | 88,565 | `b92debc2c64dc10a0570f6da9eca182565b35e13de2caeef125bf4b3eb149286` |
| Exact Test54c target | 4,194,304 | `924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01` |
| Original Beta 5.9 private HTML fallback | 3,846,585 | `7d9b5263588929b49e186da4b108ac6475201cd25adbe826a7e67a0d757e890e` |
| Beta 5.9 Rev A private HTML | 3,971,446 | `c2b97d8f51238c88f15d714385aa9bdb493ee68c838a397310888b38c489007b` |

## Verification and limits

- **PASS:** Original 2 MiB ROM + embedded cumulative IPS = exact 4 MiB Test54c target, compared byte by byte; 5,763 IPS records; target SHA verified.
- **PASS:** The original ROM was not mutated; incorrect sizes, 512-byte-headered and altered inputs were rejected; malformed/truncated patch rejected.
- **PASS:** Existing Beta 5.9 core offline Node regression tests (trade quotes, ships, Economy gates, port regions, portraits, rare-item swaps, settings, safe edits, Test54c IPS/ROM export) still passed.
- **PASS:** The new editor's inline JavaScript syntax checks passed.
- **NOT YET VERIFIED:** Real browser click/download and full in-game playthrough. Prior browser automation was blocked by an environment socket restriction. Test in your own browser and emulator before treating as a stable release.
- Known Test54c issue remains: Rimbo's biography heading can still show `~Ernst~`.

The private HTML contains a compressed ROM, **so do not upload it to GitHub or redistribute it**. Upload only ROM-free code, research documentation and the separate patch, subject to your distribution decisions and applicable rights. Never include the game's original or modified `.smc`/`.sfc` image in a public repository.

Ken Chee — Uncharted Waters: New Horizons (US SNES), research and experimental mod project, 16 November 2026.

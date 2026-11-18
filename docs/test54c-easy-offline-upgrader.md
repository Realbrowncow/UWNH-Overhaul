# Test54c Easy Offline Upgrader

**Recommended for beginners · Uncharted Waters: New Horizons (US SNES)**

The offline upgrader applies Ken Chee (Realbrowncow)'s Test54c modification to your own clean US original, without requiring an IPS patching program. Everything runs locally in a browser; the ROM is never uploaded to a website.

## Download

**[Download Test54c Easy Offline Upgrader (ZIP)](../releases/UWNH_Test54c_Easy_Offline_Upgrader_2026-11-18.zip)**

Alternative: [ROM-free source package](../releases/UWNH_Test54c_Public_Upgrader_Source_2026-11-18.zip) · [Standalone IPS patch for experienced users](../patches/test54c-clean-us/UWNH_Test54c_CUMULATIVE_from_Clean_US_ROM_2026-11-16.ips)

## Five easy steps

1. Download and extract the Easy Offline Upgrader ZIP.
2. Open `UWNH_Test54c_Public_ROM_Free_Upgrader.html` in Chrome, Edge or Firefox.
3. Choose your own unmodified, **headerless 2,097,152-byte US original** `.smc` or `.sfc` ROM.
4. Click **Verify and Create Test54c**.
5. Save `UWNH_Test54c_from_Clean_US_Verified.smc` and open it in your SNES emulator.

The tool verifies the original ROM, embedded patch and completed Test54c output using SHA-256 checksums. It refuses incompatible files without producing an output. Your original file is unchanged.

| File | SHA-256 |
| --- | --- |
| Clean original US ROM | `64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0` |
| Embedded Test54c IPS | `b92debc2c64dc10a0570f6da9eca182565b35e13de2caeef125bf4b3eb149286` |
| Verified 4 MiB Test54c ROM | `924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01` |

**Testing:** Automated patch verification and file-rejection tests passed. The project owner also confirmed the complete installation sequence in a desktop browser, the successful 4 MiB ROM download and the opening scene running in Snes9x. This confirms installation and launch, not a full gameplay regression test.

**Legal note:** The download contains a patch and program code only. It does **not** contain the original or modified game ROM. Users must provide their own legally obtained copy. This is an unofficial fan research project, not affiliated with Koei/Koei Tecmo.

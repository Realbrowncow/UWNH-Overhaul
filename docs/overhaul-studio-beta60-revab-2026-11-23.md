# UWNH Overhaul Studio — Beta 6.0 Rev AB (experimental)

**Project:** UWNH Overhaul — *Uncharted Waters: New Horizons* (US SNES)  
**Creator:** Ken Chee (Realbrowncow)  
**Date:** 23 November 2026  
**Editor target:** Test57b5d, 4 MiB, SHA-256 `ffd8754ab67870b13dee0561fba3d4492f39eea9c6b00662e6f83d26d261bbc4`  
**Status:** Core/static checks passed. **Experimental; not fully gameplay-tested.**

## Downloads in this repository

- [Beta 6.0 Rev AB ROM-free Developer Kit](../releases/UWNH_Beta60_RevAB_Cannon_Editor_ROM_FREE_Developer_Kit_2026-11-23.zip) — editor HTML, source/build script, tests, guide, attribution and the small Test56q→Test57b5d delta IPS. Contains **no original or modified ROM**.
- [Test57b5d delta IPS](../patches/test57b5d-from-test56q/UWNH_Test57b5d_Jamaica_Algiers_PirateLackeyDialogue_ONLY_EXPERIMENTAL_2026-11-22.ips) — only for an **exact Test56q ROM**, never for the clean original. The public editor itself can perform the complete clean-original-to-Test57b5d upgrade.
- [Navigator portrait palette](../assets/palettes/UWNH_Navigator_Portrait_Palette.png) and [ship portrait palette](../assets/palettes/UWNH_Ship_Portrait_Palette.png) — sixteen-colour visual references extracted from the Test56q game palette tables, for artwork preparation.
- [Cannon Editor test guide](./revab-cannon-test-guide.md) — baseline values, safety controls and suggested in-game tests.

Previous Test54c, Test56q and Beta 5.9 downloads are preserved.

## Rev AB highlights

- Upgrade an **exact clean, headerless US SNES ROM** through Test56q to Test57b5d, with ROM SHA-256 validation.
- One unified, guarded **25-model Ship Editor** for model limits, sailing stats, crew, guns and new-ship base prices.
- New **seven-cannon editor** for two native attack values, range and price; five ordinary Economy+Industry shop thresholds. Native names, Saker's always-available rule and Carronade's special gate remain protected.
- Edit **120 navigators'** starting stats/skills and the global NPC duel-equipment rules.
- Import limited-palette character/ship PNG artwork and select among **122 native walking-sprite packets** (not every packet has complete directional frames).
- Edit trade-good names and per-port prices, producer rosters/stock, development, shipyard/region settings and selected rare-item locations.
- Experimental world-map and minimap editing; protected 4 MiB ROM/IPS export and local settings files.
- Existing custom portrait and good-name demonstrations have been visually accepted in isolated gameplay/screenshots. **That is not full Rev AB gameplay certification.**

**Not supported:** arbitrary custom campaigns, general story/quest scripting, unrestricted palette loading, or guaranteed support for every combination of sprite frames. Some narrow experimental script fields may appear, but they are not a general storyline editor.

## Quick start

1. Extract the ZIP and open `New_Horizons_Overhaul_Studio_Beta_6_0_Rev_AB_Test57b5d_ROM_FREE_Source.html` locally in a modern desktop Chrome/Edge browser.
2. Supply **your own original USA SNES ROM** using the editor's clean-ROM upgrader, or load your independently verified Test57b5d ROM. **No commercial ROM is included.**
3. Make a small change and stage it; export the guarded ROM or exact-source IPS. Keep your original ROM and save files separate. Test changes in an emulator/new game before publishing.

The public edition intentionally starts **without a map preview**: no compressed copy of the commercial terrain is bundled. The map loads after you supply your verified ROM.

Clean, headerless US ROM: **2,097,152 bytes**, SHA-256 `64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0`.  
Intermediate Test56q SHA-256: `a8e72f2b9c8db2be7e6f5c10852cd0282cc13b0eea681cc450e398ebaa5aff9b`.

## Verification and credits

The Rev AB tests passed exact no-change output, source/target hash checks, the two-stage upgrade, cannon/ship write isolation, settings roundtrip, rejection of invalid changes, IPS replay and private/public script syntax checks. The public HTML's ROM and terrain bundle fields are empty. **Emulator testing of the new cannon features remains pending.**

Original **All Ten Ships Manual Control** is credited to **erich121**: during sea-battle commands press **SELECT** to toggle `Mates: AUTO ON.` (companion AI) / `Mates: AUTO OFF.` (manual), then **A** to dismiss. The erich121-inspired ship layout uses our own Test57b5d-guarded editing logic. UWNHRando and erich121 are acknowledged as research/editor references; their own licenses and notices remain applicable.

This research project does **not** provide the game ROM, original commercial artwork, audio, SRAM/savestates, or private ROM-bundled editor. ROM-free packages are provided for owners of the US SNES game. For background, screenshots and further release notes see [Ken's Maritime Worlds](https://cheeken78.wordpress.com/uncharted-waters/).

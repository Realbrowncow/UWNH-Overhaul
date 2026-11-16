# Release discipline and fast continuation in a new chat

## Current starting point

| Archive | Role | SHA-256 |
| --- | --- | --- |
| `UWNH_Test54c_Rimbo_Biography_IntroText_EXPERIMENTAL_2026-11-16.smc` | **Current experimental ROM; two updated Rimbo intro screens gameplay PASS** | **`924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01`** |
| `UWNH_Test54b_V4_Gameplay_Role_Shipyard_Descriptions_EXPERIMENTAL_2026-11-16.smc` | Exact parent of Test54c; revised 25-ship text and selected visual checks | `712fa01718857fe8398d7c6808c04674e60a0ff7ed0021e23e86ace524f7b7ba` |
| `UWNH_Test54a_Sambuk_Lancaran_Jong_ShipPortraits_EXPERIMENTAL_2026-11-16.smc` | Exact parent of Test54b; updated native shipyard images | `c94203089c0bdfa3fd64de39599bc2788209c9439f544424cca423a9dc4eb149` |
| `UWNH_Test53_Rimbo_Spear_Asmira_IndianWoman_Walkers_EXPERIMENTAL_2026-11-16.smc` | Walker/portrait parent of Test54a; Beta 5.8's current editor baseline | `9f91aaa32e91808397b470e58fd3104fe35c5885b554de5bf6e39a2d5efe6b78` |
| `UWNH_Test52_Rimbo_Spear_ROM_SourceRedirect_ONLY_EXPERIMENTAL_2026-11-16.smc` | Prior user-saved/reloaded spear-only branch; **source for Test53 IPS** | `3b325e989e95a9a3f1355cb1e20f8034c50289f6caaf7ad2ed9a8455fbc0e7ee` |
| `UWNH_Test50_Rimbo_Test5_Asmira_Face113_AllViews_EXPERIMENTAL_2026-11-15.smc` | Portrait baseline / source for Test52 | `7fce9e4b3eef6d9f981fb965ba85a35aed7c6e54683efb96951f0ae5c14cad04` |
| `UWNH_Test47_V8v4_V4_Makassar_Jong_Exclusive_CapitalFix_TEST_2026-11-15.smc` | V8v4 fleet and Jong source baseline | `8f191a5bd426f85ad20e79d61b5c69f03da2b9512d31b5e26afed74c1264e192` |
| `UWNH_Test45_Demak_Palace_Guard_RulerText_TEST_2026-11-14.smc` | Earlier gameplay-confirmed Demak/palace fallback | `9c9b2d134c2d20af46a143a87867d865b75f8c2a075434e1c5e69a65bf30dc3f` |
| `UWNH_23Port_PASS.smc` | Immutable relocation checkpoint | `114c721eab8b5dce7c850a54aa1be906c5aa0f195add893440c68e9bde6d83c0` |

All current project ROMs listed here are **4,194,304-byte headerless files**. The incremental chain is **Test52 → Test53 → Test54a → Test54b → Test54c**. Each IPS is specific to its *immediate parent hash*, not to a clean game or another test. The editor **World, Ship & Fleet Studio Beta 5.8** remains a separate Test53-based editor; it is not automatically rebuilt with Test54a–c changes. A ZIP containing private complete ROMs and workbooks is maintained separately for project continuity; **never publish it on GitHub**.

## Ten steps to change an earlier feature quickly

1. Open the private continuation documents and newest Test54c static audit first, the Word technical manual second, then the public offset/topic page for the desired feature. Older Test53 continuation notes are historical, not current release authority.
2. Extract the private Test54c package into an isolated workspace. Select exactly the listed Test54c `.smc`; verify SHA-256 and 4 MiB size. If reproducing earlier steps, recover each exact parent ROM separately.
3. Identify the **specific source of truth** for the feature: 23-port rollback / map project, V8v4 ship workbook, V4 NPC workbook, trade Economy master, portrait image, script builder or audited current ROM table.
4. Read the feature-specific source script and changed-byte audit before touching code or data. Confirm absolute port/ship/navigator/good IDs, not newly displayed names.
5. Take a copy named `Test55_<feature>_EXPERIMENTAL` (or a separately agreed Test54d) and change only the agreed data and code. Allocate free space only after a collision audit. Never use destructive in-place editing on the accepted ROM.
6. Verify byte diff, all protected tables, checksum/complement and IPS roundtrip relative to the exact selected parent. Label **static** results distinctly.
7. Prepare the shortest New Game plus ordinary Save/Continue test that can falsify the change. When an older emulator save-state cannot load, do not try to fix the game by editing the state file; use matching SRAM/new game instead.
8. Wait for the user's real gameplay evidence before promoting the feature to gameplay PASS.
9. Save the new `.smc` privately; keep the previous baseline and all approved source workbooks. Update manifest, changelog, table of new offsets and future-chat prompt.
10. For public sharing, publish the *readme/source/patch method* and optionally a lawful patch file, but **no complete commercial ROM**.

## New chat prompt

> Continue my Uncharted Waters New Horizons USA SNES project from **Test54c**, exact 4,194,304-byte SHA-256 `924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01`. Read the Test54a–c research document and latest private Test54c static audit, then recover Test54b/54a/53 parents, original V8v4 ship and V4 fleet workbooks, editor Beta 5.8 and scripts. Preserve Jepara ID33/Demak, Makassar ID77 exclusive Jong/Industry950, per-port prices, 286 independent SRAM stock counters, 64 V4 fleets/416 starting ships/63 rules, portraits and walkers, three Test54a ship pictures, and Test54b's 25 ship descriptions. Test54c's Rimbo full biography and short intro have screenshot gameplay PASS; its title still reads `~Ernst~` and needs separate source tracing. Do not mistake player-only shipyard rules for NPC fleet restrictions. Keep previous ROMs and save states, use matched SRAM, and create isolated builds with exact parent hash, checksum, byte allowlist and IPS roundtrip. The editor remains Beta 5.8/Test53-based. Never claim full campaign PASS from the two intro screens.

## Reproducibility contract

Each build should publish/recover (as appropriate) a manifest containing: parent ROM SHA, output ROM SHA, SHA and size of IPS, source-script name/version, 4 MiB header state, checksum/complement, intended allowlist ranges, byte counts, independently protected systems, per-feature gameplay status and next tests. A `README` is not a substitute for the original script or approved workbook.

See [Publication checklist](../PUBLICATION.md) for public versus private materials.

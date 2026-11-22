# UWNH Overhaul Studio Beta 6.0 Rev AB — Cannon Editor

**ROM:** Test57b5d (authoritative, unchanged)  
**Status:** Experimental. Static tests passed; emulator/gameplay confirmation pending.  
**Fallback:** Beta 6.0 Rev AA, preserved separately.

## New cannon controls

One visible **Cannon Editor** supports all seven native cannon types. Each has independently editable:

- Hull attack (1–99) and crew attack (1–99): separate native 16-bit tables.
- Battle range (1–8).
- Cannon purchase price per gun (1–9,999 ducats).
- Economy + Industry shop-unlock threshold (1–2,000) for the five native threshold-based types.

These are the **actual initial Test57b5d values**, not values copied from a draft economy workbook:

| Native ID | Cannon | Hull | Crew | Range | Price | Economy + Industry gate |
|---:|---|---:|---:|---:|---:|---|
| 1 | Cannon | 20 | 20 | 3 | 700 | 1,000 |
| 2 | Demi-cannon | 16 | 16 | 2 | 500 | 700 |
| 3 | Canon Pedrero | 12 | 12 | 3 | 400 | 400 |
| 4 | Culverin | 14 | 14 | 5 | 800 | 900 |
| 5 | Demi-culverin | 10 | 10 | 4 | 600 | 600 |
| 6 | Saker | 8 | 8 | 2 | 100 | Always available (protected) |
| 7 | Carronade | 20 | 20 | 4 | 900 | Special native conditions (protected) |

Original cannon **names and formatting**, Saker's always-available rule, and Carronade's special shop logic are not editable. The five other unlock values must remain strictly increasing in native shop order (Pedrero, Demi-culverin, Demi-cannon, Culverin, Cannon). Existing port Economy and Industry fields can be edited separately in the studio.

## Protection and regression coverage

- Native cannon arrays: ROM PC `0x0B092B`, `0x0B093B`, `0x0B094B`, `0x0B095B`, seven 16-bit values each. Adjacent terminators and following pointer data are excluded from the writable allowlist.
- Five existing 16-bit compare operands in the native shop threshold helper at ROM PC `0x233A03`, `0x233A08`, `0x233A0D`, `0x233A12`, `0x233A17`. Instruction opcodes and branch targets remain protected.
- All editable values and cumulative threshold ordering are validated on stage, settings import and ROM/IPS export. A malformed project is rejected and earlier staged changes are retained.
- Original Test57b5d hash check, exact no-change output, isolated cannon edits (only allowed table/gate/checksum bytes), stage/restore, settings roundtrip, tamper rejection, IPS replay, preserved ship editor, NPC equipment, navigator editor and upgrade path: **static PASS**.
- Private and ROM-free HTML JavaScript syntax: **PASS**. Private ROM bundle decodes to byte-identical Test57b5d; public source contains no bundled ROM: **PASS**.

These tests are not a live emulator or browser test. The roles of the two native attack tables are based on their native arrangement and changes from the original US ROM; the in-game hull/crew effect requires testing.

## Quick game test for Ken

1. Open **Rev AB PRIVATE**, load the bundled Test57b5d, and expand **Cannon Editor**.
2. Select **Saker (#6)**; confirm 8 hull attack, 8 crew attack, range 2 and 100 ducats, with shop gate locked.
3. Select **Canon Pedrero (#3)**; change price from **400 to 410**, and optionally both attack values by 1. **Stage this cannon**, then export a **ROM** or **IPS**.
4. In a **fresh in-game test**, inspect a shipyard's gun prices and compare cannon performance in a controlled battle. Check Saker/Carronade availability remains as before.
5. Return to the editor, restore Pedrero and export again. The baseline should be unchanged.

## Attribution and handling

The ship-panel layout is inspired by **erich121's New Horizons Editor** with existing MIT credit. The cannon editing encoder is our own, Test57b5d-specific guarded code. Original ten-ship manual control is credited to **erich121**: during sea-battle commands press **SELECT** to toggle `Mates: AUTO ON.` / `Mates: AUTO OFF.`; **A** dismisses the message. Website documentation remains pending user approval.

**PRIVATE HTML contains commercial ROM data; do not upload publicly.** The developer ZIP contains only ROM-free source, small IPS delta, guide, scripts and attribution. No live ROM, saved-game, website or previous-editor file was overwritten.

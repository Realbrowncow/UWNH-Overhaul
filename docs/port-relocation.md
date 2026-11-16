# How we relocated ports and rebuilt the map references

## Which editor does what

**Gilmok's [UWNHRando](https://github.com/Gilmok/UWNHRando)** provides the underlying public randomizer, map-format research and a **Theme Editor** for renaming kingdoms, 13 trade regions, 100 port names, discoveries and 46 commodities. It does not by itself reproduce the protected physical relocations in this project.

Our separately preserved **New Horizons World Map Studio Port Relocation Beta** is a browser HTML tool built using the UWNHRando map-format groundwork. Its actual controls are **Open SNES ROM**, **Open project**, **Set export ROM**, **Relocate Port**, **Find on map**, **Move to X/Y**, **Save project**, **Export .uwmap**, and **Export playable .smc**. It handles existing named ports, not adding new IDs. It has a coastal-placement and spacing guard, undo/redo and project snapshots. The original input ROM remains untouched. The minimap is not automatically regenerated.

## Practical editor procedure

1. Make a byte-identical backup and record SHA-256 of your legally obtained, compatible US ROM. Work on a copy of a precisely chosen project baseline.
2. Open the **Port Relocation Beta HTML** locally; click **Open SNES ROM** and choose the copied ROM.
3. Under **Existing ports (100)**, search or select the source slot to repurpose. A renamed city remains tied to that slot's port ID and many native story references.
4. Select **Relocate Port**, then click the desired coastline, or enter even-integer X/Y coordinates and click **Move to X/Y**. Keep the destination navigable and separate from other port-entry squares. Preserve town architecture/culture unless changing it is separately approved.
5. Use **Save project** to retain all moves; on reopening, explicitly set **Set export ROM** to the intended precise source. Avoid exporting into an already patched game without inspecting the resulting byte diff.
6. Choose **Export playable .smc** and compare new data to the parent. Confirm the tool updated the master 130-port table plus related sorted-coordinate, hash, pointer and discovery lookups. The editor's own checks do not validate campaign scripts, port exits, or ship spawn coordinates.
7. Test in an emulator: visible harbour, port-entry prompt, enter/exit positions, ordinary in-game Save → exit emulator → Continue, capital/story scenes, merchant/shipyard, and any starting ship coordinate separately. Mark the result only for tested screens.

**Compatibility warning:** An older UWNHRando generator commonly expects a **2 MiB headerless source**. The current research ROM is expanded to **4 MiB** with code and tables in upper banks. Do **not** blindly regenerate the latest Test53 with an unchanged 2 MiB editor. Test the exact version/size and manually reconcile exported changed ranges or adapt only the needed data. The same warning applies to an editor that silently rewrites port styles or unrelated commerce fields.

## What changed in binary records

The 130 port and supply-point coordinate records begin at **PC `0x08CF53`**, 22 bytes each. X/Y are little-endian 16-bit fields. Correct physical relocation additionally requires maintaining the sorted list at `0x0AA1DE`, pointer lookup at `0x0AD170`, near-port hash at `0x0F3500`, and some region/discovery indices (`0x02F86B`, `0x02F12F`). A correct map pin without these dependent records can yield wrong entry detection or voyages. The Test20 read-only audit matched all 130 primary positions and derived tables against the protected 23-port checkpoint.

The port's **37-byte economy/metadata record** at `0x08DA7F + 37*port_id` is a *different* table. Its geographic/Autosail byte `+33` is shared with other game routines; its A–K shipyard byte `+34` is separate. A physical move does not automatically make all geographic menus correct, and modifying `+33` globally solely for display could break other systems. The Test22 Autosail heading override corrected headings for particular moved cities while keeping the shared record safe; actual Autosail navigation to Poseidonis later failed and was intentionally left unresolved.

## The protected 23 original replacements

These replace or rename **existing slots**, not new ports. A later Demak/Jepara and Makassar branch supersedes two Java slot assignments as explained below.

| Original source slot | Project city | Original source slot | Project city |
| --- | --- | --- | --- |
| Jaffa | Sinop | Kaffa | Safi |
| Copenhagen | Reval | Abidjan | São Tomé |
| Cairo | Suez (rename) | Argin | Samcheok |
| Guatemala | Chactemal | Maracaibo | La Tora |
| Porto Velho | Tumbes | Barcelona | Poseidonis |
| Caracas | Lingayen | Mecca | Jepara (later repurposed) |
| Banjarmasin | Brunei | Aden | Socotra |
| Jayapura | Onim | Bangkok | Ayutthaya |
| Malindi | Oda | Cayenne | Naha |
| Cochin | Chittagong | Goa | Pulicat |
| Macao | Ningbo | Palma | Macao |
| Pisa | Goa |  |  |

The immutable protected base is `UWNH_23Port_PASS.smc`, SHA-256 `114c721eab8b5dce7c850a54aa1be906c5aa0f195add893440c68e9bde6d83c0`. *Bilbao was removed* from the reworked roster. Do not overwrite this foundation.

## Later Jepara and Makassar identity correction

The **current Test47–Test53 branch** uses **Jepara at port ID 33 (former Amsterdam slot) as Demak's capital**, and **Makassar at port ID 77**. Thus it is wrong to treat the early `Mecca → Jepara` entry in the 23-port historical table as the *current* ID for Jepara. Test45 moved the Amsterdam slot to Java; the opening Mercator and Asmira scenes, relocated entry prompt, ordinary save/reload/exit location and selected palace features were observed in game. Test47's Jong permission uses `33=Jepara`, `77=Makassar`; the authoritative V8v4/V4 workbook controls those names and records.

Jepara retains approved **Style 1 / Palette 0**, its guarded major-port character and capital restrictions. A later architectural Style4 Test46 experiment **failed and was abandoned**. No direct wholesale switch of port cultures or African-style architecture was authorised. This distinction matters: physical port moves, names, art styles, and capital/investment data must be tested as separate changes.

## Naming with the Theme Editor

For supported vanilla-sized inputs, use UWNHRando's **Theme Editor** to change its six kingdom/adjective names, 13 regions, 100 named ports, 30 supply ports, 99 discoveries and 46 commodities, save a `.thm` and reload it to verify. Its normal ROM generation must still be checked against the newer expanded ROM. Names inside compressed story dialogue may be independent references; changing a visible label will not automatically rewrite every scenario or event.

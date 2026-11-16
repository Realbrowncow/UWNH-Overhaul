# Evidence ledger, regression tests and unfinished engineering

## Read these labels literally

**GAMEPLAY PASS:** Ken observed the stated behaviour in an actual SNES emulator and supplied a report or screenshots. **STATIC PASS:** byte-level diff, checksum, IPS roundtrip, table validation, isolated CPU check or script simulation succeeded. **EXPERIMENTAL:** the build is not a release candidate without user gameplay checks. The labels are **feature-specific**, not a blanket claim that an entire ROM is bug-free.

## Condensed chronology

| Milestone | Main result | Verified scope or limitation |
| --- | --- | --- |
| Protected 23 ports | Original relocation foundation | Passed original targeted port checks; never modify fallback |
| Test16–20 | Regional Used Ship generation and guarded offers | Amsterdam, quote fixes, menu checks; full long-term Used state caveat |
| Test21–22 | Autosail initial known cities and headings | Menu changes PASS; voyage targeting **not fixed** |
| Test23–26 | A–K New Ship candidate repair | Reval, Danzig and Amsterdam shipyard gameplay PASS |
| POC6/7/12 | Individual port pricing and distance/premium sample | Genoa/Venice, IDs 98/99, 23 price quotes and 4 transactions |
| Test27–28 | Integrated 4,600 prices and good names | Binary integrity and selected gameplay follow-up |
| Test29 | 286 offer Economy threshold bytes | User reported selected menus looked correct; 158 new gate bytes static |
| Test30 | 286 independent sparse SRAM counters | User-tested multiple ports, same-category independence and Jan/May/Sep cycles |
| Test31-A/B | Early live stock UI | A missing line, B wrong value — superseded |
| **Test31-C** | Corrected live `Stock: N` | **GAMEPLAY PASS** Salt/Brocade `1→0` and ordinary reload |
| Test33 | 75-year boundary | 1596 playable, 1597 ending; new game still original start |
| Test34 | Diego/fleet freezes | Intermittent reports; root cause not proven stable |
| Tests35–38 | Navigator portrait, level, name and Antwerp moves | Café/inn/map sample gameplay PASS |
| Test42–43 | Item/shop integration and 8 special item moves | 14 byte shop diff and exact IPS static; shop survey not exhaustive |
| Test44 | Scenario opcode interpreter | Substantial static reverse engineering; many gates not runtime decoded |
| Test45 | Demak/Jepara relocation, palace, story and faces | Relevant opening scenes and ownership observed in game |
| Test46 | Jepara town style experiment | **FAILED / ABANDONED**; do not merge |
| Test47 | V8v4 25 ships, V4 fleets and Makassar Jong gate | **STATIC PASS**; comprehensive yard/fleet gameplay pending |
| Tests48–50 | Rimbo/Asmira 40×48 portraits and aliases | Test50 eventual in-game visual use confirmed in later branch |
| Test51 | Walker-state experiment | Diagnostic only; superseded by ROM-native source method |
| **Test52** | Rimbo spear-holder all views | User checked and reported save/reload functioning |
| **Test53** | Rimbo spear + Asmira Indian-woman walker | **Visual GAMEPLAY PASS**; Test53 cold save/Continue unverified |
| **Test54a** | Three owner-supplied shipyard images: Sambuk, Lancaran, Jong | **STATIC PASS (42/42)**; Sambuk/Lancaran New Ship appearance gameplay accepted; Jong image still pending |
| **Test54b** | Nineteen rewritten native ship descriptions, six retained | **STATIC PASS** (1,372 changed bytes); selected revised text observed/accepted by owner, not a 25-yard exhaustive test |
| **Test54c (current)** | Rimbo 130-character biography and clean two-part introductory text | **STATIC PASS** (164 changed bytes, exact IPS); **GAMEPLAY PASS** for both texts in user screenshots; `~Ernst~` heading remains |

## Known issues and boundaries

1. **Autosail geographical voyage to relocated Poseidonis**: menu grouping fixed independently; actual destination route continued toward wrong ocean regions. The user chose to **ignore/defer** the navigation problem. Do not silently claim it fixed.
2. **Diego/Raphael fleet screen and battle freeze**: earlier experiments showed both freezes and periods of apparently correct behaviour. A single successful screen is not an exhaustive cure; preserve `.szst` and original gameplay evidence separately.
3. **Test47 NPC generated fleets**: 63 rules and 416 initial positions passed static audits, but future regenerated ship composition and fleet screen stability across all 64 fleets still require targeted gameplay.
4. **Test47 exclusive Jong**: Jepara ID33 is excluded, Makassar ID77 is the only permission at gate950. This is a two-byte static correction; a full investment→unlock demonstration was not recorded.
5. **Portrait use in all contexts**: Test50 aliases cover selection/status/dialogue, but any new face edits need separate tests because portraits may be shared. Test53 walker palettes may vary with context; user found current result acceptable.
6. **Save-state compatibility**: old emulator snapshot files can embed memory inconsistent with a new ROM. Use **ordinary in-game Save/Continue and matching 64 KiB `.srm`** for persistence tests; never overwrite your known-good campaign or assume `.szst0` from another build is interchangeable.
7. **Original producer-price implementation**: the current recovered docs conclusively identify the 4,600 resale quote table but do not record a stand-alone second buy-price table offset. Keep the distinction explicit until an implementation disassembly verifies it.
8. **All-port/all-good coverage**: controlled spot tests and table audits are substantial but not equivalent to 100×46 interactive transaction testing. The 4-digit stock display and every Jan/May/Sep UI refresh need wider coverage.
9. **Rimbo biography header**: Test54c screenshots display the new text beneath an old `~Ernst~` heading. That title is not the already-renamed player record. The visible old name is a **known FAIL**, while the new biography body and short intro both passed. Do not globally replace the raw `Ernst` phrase at PC `0x04DF31` without source tracing.
10. **Test54a shipyard graphics scope**: only Sambuk and Lancaran new-ship images were specifically approved from screenshots. Jong's newly installed portrait statically decodes but lacks a direct user gameplay confirmation. At-sea and battle moving images were not modified.
11. **Test54c regression scope**: screenshots show successful boot into the changed hero/intro screens, but do not validate every game route, Jong Industry unlock, an ordinary cold save/Continue or all fleets in the current build.

## Minimum regression for future Test54d / Test55+

1. **Static:** SHA-256 source check; 4 MiB headerless; exact changed-byte allowlist; ROM checksum/complement; IPS exact reconstruction; table/field range assertions; no collisions in code, portrait packets or 286 SRAM words.
2. **New Game:** start as Rimbo; verify selection face, Jepara opening Mercator event, both correct intro texts, the still-unresolved `~Ernst~` title, Asmira dialogue and walking sprites in two rooms/outdoors, Sultan/palace and named city/port entry.
3. **Save:** normal Save → emulator exit → fresh ROM launch → Continue; check characters, ship positions, market stock and newly changed feature. Keep older `.szst` files untouched and do not use them for cross-ROM judgments.
4. **Economy:** Amsterdam Salt/Brocade or another short pair: independently deplete, save and reload. Check one locked Economy-good producer and one port price with observed index.
5. **Yards:** check Jepara no Jong, Makassar exclusive at Industry950, and a previously approved Region C yard offer, using fresh relevant state.
6. **NPCs:** open two contrasting fleet screens without freeze, check future generation if feasible, verify at least one renamed navigator and pirate encounter.
7. **Time/battle:** if shared low-level game code changed, check 1596 boundary and a short manually controlled ten-ship naval battle, with only the flagship duelling.

Report each row as PASS, FAIL or NOT RUN; include ROM hash, filename, emulator version, new vs continued game, SRAM hash and screenshot/page reference. A failure in an unrelated area does not automatically erase an earlier narrower PASS, but it prevents an unqualified release claim.

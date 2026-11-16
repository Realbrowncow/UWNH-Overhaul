# Ship roster, New Ship construction and Used Ship markets

## Source of truth

The latest recovered design is **V8v4 (15 November)** in the six-sheet reconciled Test47 workbook, with the project owner's two original V8v4 and V4 workbooks preserved separately. It supersedes older V7, V8v3, V17 and provisional names and prices where they conflict. The reconciled source records **25** ship IDs `0–24`. Its complete editable table is exported to [`data/ships_v8v4.csv`](../data/ships_v8v4.csv). The game has fixed model slots; a change to an ID changes all records referencing that ID.

The 25-model base table begins at headerless **PC `0x08CE27`**, 12 bytes per record. Speed uses model record `+2` tacking, `+3` sailing power, and `+6` total capacity. Model price, cannons, hull and crew fields require the confirmed schema from the source editor / audited V8v4 build. Treat all 12 bytes as sensitive. The native 25-byte template at `0x08CBB6+25*id` is *not* a complete independent Used Ship model table.

**Presentation update through Test54c:** the active game now carries Test54a's Sambuk, Jong and Lancaran **shipyard/model pictures** and Test54b's user-approved shipyard descriptions. These are *presentation changes*, not new hull stats, nation build rules or new combat/trading mechanic flags. See [the exact Test54a–c research](test54-ship-pictures-descriptions-rimbo.md) and [description data](../data/shipyard_descriptions_test54b.csv). The user's division into trade and combat roles governs the wording; specifically Galleon is a warship.

## Current V8v4 models

| ID | Ship | Class | Build rule | Industry gate |
| ---: | --- | --- | --- | ---: |
| 0 | Sambuk | Medium | G | 400 |
| 1 | Hansa Cog | Medium | C | 300 |
| 2 | Dhow | Small | G, H, I | 300 |
| 3 | Buss | Large | Danzig only | 900 |
| 4 | Tallette | Small | A, D, E | 250 |
| 5 | Caravela Latina | Small | A, B, C, D, E, F, G | 200 |
| 6 | Caravela Redonda | Small | B, C, K | 250 |
| 7 | Brigantine | Medium | B | 400 |
| 8 | Nao | Medium | A, D, E | 500 |
| 9 | Carrack | Medium | A | 600 |
| 10 | Galleon | Medium | A | 800 |
| 11 | Jong | Large | **Makassar only** | **950** |
| 12 | Lancaran | Medium | H, I | 600 |
| 13 | Sloop | Small | E, K | 350 |
| 14 | Frigate | Medium | B | 700 |
| 15 | Barge | Large | Valencia only | 1000 |
| 16 | Full-rigged Ship | Large | Bristol only | 1000 |
| 17 | Junk | Large | Ningbo only | 900 |
| 18 | Light Galley | Small | E, F, K | 300 |
| 19 | Xebec | Large | Sinop and Suez only | 900 |
| 20 | Venetian Galeass | Large | Venice only | 1000 |
| 21 | La Reale | Medium | E, F | 600 |
| 22 | Tekkousen | Large | Sakai and Poseidonis | 1000 |
| 23 | Atakabune | Medium | J, K | 600 |
| 24 | Kansen | Small | J, K | 350 |

The previous **War Kravel / Bao Chuan** names belong to earlier approved drafts, not this actual applied V8v4 Test47 workbook. Preserve the currently applied names when starting new changes.

## A–K regional construction and Industry

The A–K shipyard region is `+34` within each port's 37-byte record (`0x08DA7F + 37*port_id`). It is **not** the original 13-region Autosail/geographic field at `+33`. Industry gates restrict a candidate even when its ship type belongs to that port's yard group. Additional exclusive-port permissions are retained separately; do not satisfy a threshold by merely assigning a model to a whole region.

Gameplay PASS examples: Reval (Industry260) and Danzig (280) offer Caravela Latina and Redonda; Amsterdam before its Jepara move (Industry730) offered Hansa Cog, Latina, Redonda while Buss remained locked at gate900. The correction required a **native candidate swap** because changing region labels alone was not sufficient.

**Test47 Makassar Jong correction:** Jepara **ID33** is Demak's capital, Industry730, Region H, with Dhow/Lancaran and **no Jong**; it cannot accept capital investment. Makassar **ID77** is investable, Industry450, Region H; Dhow/Lancaran are standard, **Jong is exclusive**, but unlocks only at Industry950. Test47 changed two permission flag bytes; static PASS. In-game unlocking after investment remains a targeted outstanding test.

**Approved fleet-mix exception:** the A–K regions, individual construction ports and Industry gates described here govern **player New Ship purchases**, not the composition or generation of NPC fleets. NPC ship choices follow the owner's separate V4 64-fleet / 416-starting-hull / 63-generator specification for game balance, even when those approved hulls cross player shipyard regions. Do not force the V8v4 construction table onto NPCs. See [NPC fleet rules](npc-fleets-and-navigators.md).

## Prices above one million ducats

The project extended the price representation beyond a 16-bit-only assumption, including a **32-bit price route and native fallback**. V8v4 uses Beech-reference base prices. Tekkousen has mandatory Steel: **895,000 × 1.4 = 1,253,000 ducats** at the stated nominal market condition. Barge base is **961,000**. A previous isolated over-million boundary test proved encoding; the shipyard/build/purchase price should still be regression-tested in each integrated branch.

## Used Ships are a distinct system

The **eight Large model IDs 3, 11, 15, 16, 17, 19, 20, 22** must never be offered as Used Ships. Player resale of an owned Large ship remains possible. The Used generator historically combined regional candidates and a global/worldwide offer path. Test17 restricted it to 11 region-specific lists, candidate table **PC `0x0AA522` (11×8 slots)**, and bypassed the general draw at **PC `0x0A5B33`**. Test20 added a 100-port/current-Industry guard at menu and purchase boundaries.

The user verified wrong Sambuk/Galleon Used offers disappeared in Amsterdam; Tests18/19 adjusted quoted cargo, minimum crew and cannons to match the V8 model. Some earlier quote-versus-owned hull differences were still open when Tested21 was documented. User-approved later Used Ship design considered 80% model capacity (rounded down to tens), 85% tack/power and Teak hull, but old Test21 notes do not prove that every such value has a separate persisted per-vessel implementation. Recheck **current applied ROM** before asserting these later design values as runtime behaviour; a global edit to the 12-byte ship table would also damage New Ships.

## Safe change procedure

1. Open the V8v4 workbook and locate **slot ID**, not only display name. Write down current size, propulsion, total capacity, crew min/max, guns, hull, tack/power, Beech price and special-hull rule.
2. Consult erich121 New Horizons Editor for human-readable field semantics; use the ROM and source workbook to verify exact byte encoding, especially 32-bit price extensions.
3. For a New Ship permission change, check **A–K region, specific port allowlist and Industry gate** together. For a Used offer, check the Used regional candidates and Industry guard instead.
4. Make an isolated build; verify all **25 model records, 100×25 yard permissions and 64 fleet starting compositions**, except intentional changes. Recompute checksum and IPS.
5. In game, use fresh SRAM, confirm the offer/lock and buy one test ship if feasible. For ship-stat changes, verify its quote, owned fleet, ordinary save/Continue, remodeling and sea performance separately.

An example one-byte yard flag patch and protected assertions appear in the Test47 builder in the private continuation archive.

# UWNH Overhaul — Uncharted Waters: New Horizons

## Latest experimental editor — 23 November 2026

**UWNH Overhaul Studio Beta 6.0 Rev AB** targets the authoritative **Test57b5d** mod ROM. It adds a unified 25-ship editor, a guarded seven-cannon editor, 120-navigator starting stats, limited-palette PNG portraits, trade and map controls, plus ROM/IPS export and a clean-US-ROM upgrade path. **Static tests passed; new controls are not fully gameplay-tested.** No game ROM is distributed.

- [Beta 6.0 Rev AB ROM-free release guide](docs/overhaul-studio-beta60-revab-2026-11-23.md) — installation, ROM-free downloads, palette references, testing scope and credits.
- [ROM-free Rev AB kit](releases/UWNH_Beta60_RevAB_Cannon_Editor_ROM_FREE_Developer_Kit_2026-11-23.zip) — includes the editor HTML and source/tests.
- The [Test56q→Test57b5d delta IPS](patches/test57b5d-from-test56q/UWNH_Test57b5d_Jamaica_Algiers_PirateLackeyDialogue_ONLY_EXPERIMENTAL_2026-11-22.ips) is **not** for a clean original ROM; the editor handles the full clean-ROM upgrade.

**Original all-ten-ship manual control by erich121:** SELECT during sea-battle commands toggles mates AUTO ON/OFF, A dismisses the notice. Complete custom campaigns and general story scripting are **not** supported.

**UWNH Overhaul** is Ken Chee (Realbrowncow)'s experimental modification of *Uncharted Waters: New Horizons* (USA SNES), accompanied by engineering notes, reproducible data layouts, implementation case studies and test reports. **UWNH Overhaul Studio** is the name of the associated editing application now offered as experimental Beta 6.0 Rev AB; its gameplay testing is ongoing.

**Historical documentation snapshot (16 November 2026):** At that time the latest integrated and observed-to-boot branch was **Test54c**, a 4,194,304-byte headerless experimental ROM with SHA-256 `924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01`. It inherits Test53's Rimbo/Asmira portraits and walking sprites, Test54a's three shipyard illustrations, and Test54b's revised shipyard descriptions. Test54c's full Rimbo biography and short introduction were checked in-game. The `~Ernst~` biography heading remains an acknowledged defect. Complete campaign and ordinary-save regression are **not** implied by these narrow checks.

This repository describes research and original patch-making methods. **It does not contain the commercial ROM, Koei graphics, BIOS files, emulator states, or private save games.** Bring your own lawfully obtained US SNES game. An IPS must be applied to the **exact SHA-256 source build identified beside it**, never to an arbitrary ROM.

## What we accomplished

| System | Engineering result | Evidence boundary |
| --- | --- | --- |
| World and ports | A protected 23-port relocation foundation; later Java/Demak/Jepara and Makassar placements; coordinate and derived-index consistency checks | Specific port entry, story opening, ordinary save/exit observed in Test45; not every original quest path |
| Nations and story | Demak in the former Holland national slot, palace owner/support and ruler text; Rimbo/Asmira story and portraits | Selected Test45 palace dialogue and alliances gameplay PASS |
| Trade prices | 100 independent port profiles × 46 goods; 4,600 16-bit resale quotes; distance tiers, producer buyback, special premiums | POC price quotations and later integrated checks; 4,600 table statically verified |
| Market access | 286 producing port–good links, 46 Economy thresholds | Test29 and later integration, selected game observations |
| Stock and persistence | 286 independent 16-bit SRAM counters, January/May/September reset, live `Stock:` display | Test30 multiport/cross-year user checks; Test31-C Salt/Brocade screen and save/reload gameplay PASS |
| Ships and yards | 25 ship models, V8v4 balancing, extended ducat price path, 11 A–K regions, Industry gates, restricted Jong | Earlier menu gameplay and Test47 static audit; Makassar Jong unlock awaits direct gameplay test |
| Latest ship presentation | Test54a user-authored Sambuk, Jong and Lancaran shipyard portraits; Test54b 19 rewritten role-consistent descriptions and six retained original entries | Three images and 25 description slots static PASS; Sambuk/Lancaran pictures and selected descriptions observed in game; Jong picture still awaits direct check |
| Used ships | Large-class exclusion, region/Industry candidate filtering and quotation corrections | Amsterdam and related menu gameplay; some old quote-versus-owned durability caveats |
| Cannons | Seven redesigned cannon categories with price/Industry/range progression | Data/static verification, not exhaustive combat regression |
| NPC fleets | 64 fleets, 416 initial ship positions, 63 future generation rules; V4 user-authored choices | Test47 static integrity; comprehensive future-spawn and fleet screen tests outstanding |
| Navigators | Name, levels, skills, locations and portraits; pirate renames and 4 roaming pirate identities | Selected inn/café/map visual checks; not every navigator encounter |
| Art and sprites | Custom 40 × 48 fixed faces and guarded 8-frame 16 × 16 walker source redirects for Rimbo and Asmira | User checked Test53 appearances; sprite-loading code and IPS static verified |
| Rimbo opening | Test54c 130-character user-approved biography and cleaned two-part short introduction | Exact biography and first intro confirmed by two user screenshots; `~Ernst~` heading persists |
| Other game mechanics | Manual command of all ten ships, 75-year campaign boundary, rare-equipment shops, selected Autosail menu fixes | Several specific gameplay passes; Autosail voyage-to-relocated-port remains broken |

**Game-tested** means a named screenshot/test confirmed that *particular* action. **Static-tested** means bytes, source tables, checksum or patch roundtrip checked. **Not yet tested** is not a failure. We deliberately retain those labels at feature level.

## Current public build: UWNH Overhaul Test56q (experimental)

**Test56q** is the latest public experimental build (20 November 2026). It incorporates the earlier world, ship, economy, character, discovery-dialogue and ship-resale experiments, plus further town-NPC dialogue changes. The **Jepara capital duel warning** and **Onim exclusive-goods dialogue** passed targeted gameplay checks; the full 100-port and full-game regression remain outstanding.

- **Recommended:** [Test56q ROM-free Easy Offline Upgrader ZIP](releases/UWNH_Overhaul_Test56q_Easy_Upgrader.zip)
- **Alternative for experienced patchers:** [Test56q cumulative IPS](patches/test56q-clean-us/UWNH_Overhaul_Test56q.ips)
- **Instructions:** [Test56q offline upgrade guide](docs/test56q-easy-offline-upgrader.md) · [illustrated WordPress guide](https://cheeken78.wordpress.com/uncharted-waters/test56q-installation-guide/)

**Input:** clean, unmodified, headerless US ROM of 2,097,152 bytes, SHA-256 `64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0`. **Output:** 4,194,304 bytes, SHA-256 `a8e72f2b9c8db2be7e6f5c10852cd0282cc13b0eea681cc450e398ebaa5aff9b`.

The offline upgrader runs locally in a browser, verifies the game file and generates a new ROM without changing the original. It is not an editor. The IPS and upgrader are **alternatives**, not patches to be applied in sequence. The game ROM is never provided. **Compatibility:** the original Test56q filenames remain available alongside the UWNH Overhaul-branded filenames so earlier download links continue to work.

## Earlier release: Test54c (experimental)

The **[Test54c clean-US cumulative IPS](patches/test54c-clean-us/UWNH_Test54c_CUMULATIVE_from_Clean_US_ROM_2026-11-16.ips)** is available alongside a **[ready-to-download ZIP package](releases/UWNH_Test54c_Clean_US_ROM_IPS_GitHub_2026-11-16.zip)** and the **[complete patching instructions](patches/test54c-clean-us/README_Test54c_Clean_US_IPS_2026-11-16.md)**. The ZIP includes the IPS, audit, builder and independent verifier. It does **not** contain a ROM.

- **Base:** untouched, headerless 2 MiB US ROM, SHA-256 `64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0`.
- **Result:** 4 MiB Test54c, SHA-256 `924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01`.
- **Evidence:** exact IPS replay **PASS**; full gameplay regression **pending**. The `~Ernst~` biography heading remains unresolved.

Use an IPS patcher with RLE and size-expansion support, and verify both hashes. Obtain your own lawful retail copy. The project licences cover **original** materials, not the original game or any third-party content that a patch might encode. This is an unofficial experimental release.

## Editor history: World, Ship & Fleet Studio Beta 5.9 and Rev A

**Branding update:** The next integrated editor will be called **UWNH Overhaul Studio**, beginning with **Beta 6.0** once it is completed and verified. Beta 5.9 and Rev A remain archived under their original filenames and earlier *World, Ship & Fleet Studio* identity; do not confuse the upcoming editor with the already available Test56q offline upgrader.

The [Beta 5.9 source](editor_beta59/base/README_Beta59_Test54c.md) and [Rev A Original-ROM-to-Test54c upgrade source](editor_beta59/rev_a/README_Beta59_UpgradeOriginal_Test54c_2026-11-16.md) are now public for technical review. You can also download the [Beta 5.9 source ZIP](releases/UWNH_World_Ship_Fleet_Studio_Beta_5_9_Test54c_ROM_FREE_Source_2026-11-16.zip) and [Rev A upgrade source ZIP](releases/UWNH_Beta59_UpgradeOriginal_Test54c_RevA_ROM_FREE_Source_2026-11-16.zip).

These are **source/rebuild kits, not standalone editor downloads**. Building the private integrated HTML requires the author's exact private baseline editor and independently obtained game image/IPS; generated HTML embeds commercial game bytes and **must not be uploaded**. See the [editor source overview](editor_beta59/README.md) for dependencies, hashes and limitations. Rev A's original-ROM upgrade and existing editing controls passed independent Node tests; browser click/download and broad emulator regression remain unverified.

## Read the guides

1. [How the ROM is structured](docs/rom-address-map.md) — headerless PC offsets, SNES address concepts and master data map.
2. [Port relocation and map editor](docs/port-relocation.md) — original UWNHRando versus our World Map Studio Port Relocation Beta, data changes and safeguards.
3. [Individual port price engine](docs/individual-port-prices.md) — 4,600 values, bank E4, lookup formula, price design and purchase/resale distinctions.
4. [Trade stock and Economy gates](docs/stock-ledger.md) — 286 SRAM words, Economy access bytes, restock periods and visible quantity.
5. [Ship models and shipyards](docs/ships-and-shipyards.md) — 25 models, large-ship restrictions, V8v4, exclusive Makassar Jong.
6. [Cannons and equipment](docs/cannons-and-equipment.md) — seven weapon types and eight rare-shop moves.
7. [NPC fleets and navigators](docs/npc-fleets-and-navigators.md) — V4 rules, startup ships, recruiters, pirates.
8. [Character portraits and walkers](docs/portraits-and-walkers.md) — 4bpp face packets, shared palettes, two guarded decompressor hooks.
9. [Nations, scenarios and campaign](docs/nations-scenarios-and-campaign.md) — Demak, script streams, renamed characters and campaign length.
10. [Test results and open bugs](docs/testing-and-known-issues.md) — transparent evidence ledger and regression checklists.
11. [How to resume and safely patch](docs/continuation-and-releases.md) — baseline fingerprints, rollback and new-chat protocol.
12. [Source code and reproduction](docs/source-reproduction.md) — recovered original build scripts, archive caveats and safe read-only tools.
13. [Latest Test54a–c research](docs/test54-ship-pictures-descriptions-rimbo.md) — new art pointer slots, 25 character-limited ship descriptions, Rimbo's 3 text locations, hashes and remaining defect.

Machine-readable tables appear in [`data/`](data/): **25** ship specifications, **25** ship-description slot records, **64** fleets, **416** starting ships, **63** generator rules, **46** approved good stock limits, **286** producer–good combinations, the original **23** port relocations and **eight** equipment-shop moves. Read-only helpers are in [`tools/`](tools/), including an exact hash/diff verifier for Test54c. The longer **Word Technical Manual** and **private recovery archive** accompany this public repository as separate user-managed deliverables.

## Key discoveries at a glance

| Headerless PC address | Interpretation |
| --- | --- |
| `0x08CF53` | 130 port/supply coordinate records, 22 bytes each |
| `0x08DA7F` | 100 port records, 37 bytes each; +32 special item slot, +33 geography, +34 A–K shipyard region |
| `0x08CE27` | 25 ship model records, 12 bytes per model |
| `0x240000 + 128*p + 2*g` | Resale quote for port `p=0..99`, good `g=0..45` |
| `0x240000 + 128*p + 119 + s` | Producing offer Economy threshold byte for local offer slot `s` |
| SRAM `$25:6020–$25:625B` | 286 persisted, independent consumed-unit counters |
| `0x02BCB7 + 3*f` | Fixed-face art pointer entry for portrait ID `f` |
| `0x0AAF00 + 32*f` | 16-colour BGR555 portrait palette for fixed-face ID `f` |
| `0x0B7601` onward | 25 native, separately size-capped shipyard description messages (Test54b) |
| `0x0EBC25` | Rimbo's NUL-terminated full biography entry (Test54c) |
| `0x0B619B`, `0x0EB9A2` | Two consecutive displayed short-intro text fragments (Test54c) |

These are **observed locations for the stated project builds**, not universal offsets for all patches, region variants or emulator header conventions. See the full address reference for context.

## Upstream authors and credits

- [erich121 / New Horizons Editor](https://github.com/erich121/uncharted-waters-new-horizons-editor) — outstanding open-source GUI editor, ship data and game-modification reference.
- [Gilmok / UWNHRando](https://github.com/Gilmok/UWNHRando) — original randomizer, theme and map-format reference. The custom browser World Map Studio Port Relocation Beta was built with that research as a foundation; it is **not** a feature of the unmodified Theme Editor.
- Project owner and lead designer **Ken Chee** — all design decisions, ship and NPC workbooks, many rounds of gameplay testing, screenshot evidence and final selection of custom faces/walkers.
- **ChatGPT** — analysis, 65816 research, scripts, patch integration, data checking and documentation in collaboration with Ken.
- Koei / Koei Tecmo — original game and intellectual property, not affiliated with this project.

The upstream projects may have their own licenses. Our notes are original documentation; **do not imply their authors endorse these modifications**. See [PUBLICATION.md](PUBLICATION.md) before uploading binaries, code or art.

## Licensing

**Copyright © 2026 Ken Chee — project owner and lead designer.** Our licensing grants cover only original material for which we hold the necessary rights:

- **Original Python tools and recovered project scripts:** [MIT Licence](LICENSE), insofar as we have rights to license the particular code.
- **Original research writing, guides and copyrightable data compilations:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-DOCUMENTATION.md). Reuse requires credit to Ken Chee, a licence link and an indication of changes.
- **Not covered:** Koei / Koei Tecmo's game, ROM bytes, sprites, audio, trademarks or other third-party works. Upstream code keeps its own licence; IPS/BPS patch bytes and artwork have separate third-party rights considerations.

These licences do not imply endorsement by Koei / Koei Tecmo or the credited upstream editor authors.

## Repository status

This remains an **experimental research and modification project**, not a fully certified campaign release. The ROM-free **Test56q Easy Offline Upgrader** is available for players who own the clean US ROM; the separate IPS is for manual patching. Older Test54c and Beta 5.9 files remain archived. Some experiments still lack complete rebuild or gameplay evidence; exact offsets are stated only when supported by surviving audit or code. **No commercial original or modified ROM is distributed.**

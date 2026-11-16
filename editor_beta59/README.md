# World, Ship & Fleet Studio — Beta 5.9 ROM-free source

Project owner and lead designer: **Ken Chee**. An unofficial research project for *Uncharted Waters: New Horizons* (US SNES), not affiliated with Koei/Koei Tecmo.

## Public packages

| Package | Browsable source | ZIP | Description |
| --- | --- | --- | --- |
| Beta 5.9 / Test54c | [Source files](base/) | [Download ROM-free source ZIP](../releases/UWNH_World_Ship_Fleet_Studio_Beta_5_9_Test54c_ROM_FREE_Source_2026-11-16.zip) | Guarded Test54c data editing, derived from Beta 5.8 |
| Beta 5.9 Rev A | [Upgrade source](rev_a/) | [Download ROM-free Rev A ZIP](../releases/UWNH_Beta59_UpgradeOriginal_Test54c_RevA_ROM_FREE_Source_2026-11-16.zip) | Adds clean-original-to-Test54c verification and IPS upgrade |

Both ZIPs were checked for archive integrity and contain **no `.smc`/`.sfc` image, compressed game image, commercial game art or private integrated editor HTML**. They are source/rebuild kits, not ready-to-run browser editors.

## How Rev A relates to Beta 5.9

1. The base [Beta 5.9 builder](base/build_beta59.py) requires the owner's exact **private Beta 5.8 HTML** (SHA-256 `e79862dd436697489cfe326378e240c67052faccbb69ea8ad3f0f8da87186f19`) and the exact privately held **4 MiB Test54c ROM** (SHA-256 `924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01`). It generates private Beta 5.9 HTML (SHA-256 `7d9b5263588929b49e186da4b108ac6475201cd25adbe826a7e67a0d757e890e`).
2. The [Rev A builder](rev_a/build_beta59_upgrade.py) requires that **private Beta 5.9 HTML** plus the [separately published cumulative IPS](../patches/test54c-clean-us/UWNH_Test54c_CUMULATIVE_from_Clean_US_ROM_2026-11-16.ips) (SHA-256 `b92debc2c64dc10a0570f6da9eca182565b35e13de2caeef125bf4b3eb149286`). It adds **Upgrade Original ROM to Test54c** and generates private Rev A HTML (SHA-256 `c2b97d8f51238c88f15d714385aa9bdb493ee68c838a397310888b38c489007b`).
3. In the private Rev A editor, selecting the exact **headerless 2 MiB US original ROM** and pressing **Verify and Create Test54c** checks the clean ROM hash, applies the cumulative IPS (including the 2→4 MiB expansion), checks the output SHA-256 and offers the upgraded ROM as a local download. The source is not modified.

**Important:** Rebuilding either private editor requires the owner's separately held inputs. The public source alone does not yield a usable editor. Do not publish the generated HTML; it embeds the commercial game image.

## Verification and known limits

- Independent Node replay of the actual Rev A module: **PASS**; 5,763 IPS records, byte-for-byte exact Test54c target, source unchanged, bad inputs refused, inline JavaScript syntax PASS.
- Existing Beta 5.9 Node regression suite against Rev A: **PASS** for bundled-ROM load, unchanged export, trade quotes, ship data, Economy gates, port regions, portraits, special-item swaps, settings guards and IPS/ROM consistency.
- **Not yet verified:** interactive browser click/download and comprehensive emulator gameplay after edits.
- Known Test54c issue: the biography heading may still show `~Ernst~`.

## Licence and credits

Original project software is provided under the repository's [MIT Licence](../LICENSE), and original writing/eligible data under [CC BY 4.0](../LICENSE-DOCUMENTATION.md), insofar as the project holds those rights. Upstream tools retain their own licences. None of these grants authorise distribution of Koei/Koei Tecmo ROM data or game art. See [PUBLICATION.md](../PUBLICATION.md).

Research, design and user testing: **Ken Chee**. Technical analysis, integration and documentation: **ChatGPT in collaboration with Ken Chee**.

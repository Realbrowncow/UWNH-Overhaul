# New Horizons World, Ship & Fleet Studio — Beta 5.9 (Test54c)

**Private owner build · 16 November 2026 · Ken Chee · US SNES game project**

Beta 5.9 updates the integrated offline editor's protected ROM baseline from
**Test53** to **Test54c**, preserving its existing Beta 5.8 editing tools.
The standalone private HTML embeds a full compressed Test54c game image and
must **not** be uploaded to a public GitHub repository or redistributed.

## Getting started

1. Extract the **private editor ZIP** on your computer.
2. Open `New_Horizons_World_Ship_Fleet_Studio_Beta_5_9_Test54c_Integrated.html`
   in current Chrome or Edge; the editor operates offline.
3. Click **Load Test 54c** at the top, or **Load bundled Test 54c** in the
   left panel. The editor decompresses and verifies the exact internal ROM.
4. Under **Test 54c · Mod Systems**, select the fields to adjust and click
   **Stage**. Stage operations do not yet change the protected source image.
5. Use **Show static audit** and **Save Test54c edits JSON** to record changes.
6. **Export edited ROM** or **Export exact-source IPS**. The editor performs
   checksum and allowed-address checks on the result. Validate it in your
   emulator with an ordinary save/reload cycle, not an incompatible save state.

## Exact protected source

| Item | SHA-256 | Size |
|---|---|---|
| Beta 5.9 embedded Test54c ROM | `924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01` | 4,194,304 bytes |
| Beta 5.8 editor used for source | `e79862dd436697489cfe326378e240c67052faccbb69ea8ad3f0f8da87186f19` | 3,841,904 bytes |
| Beta 5.9 private integrated HTML | `7d9b5263588929b49e186da4b108ac6475201cd25adbe826a7e67a0d757e890e` | 3,846,585 bytes |

Do **not** load Test53, Test54a or Test54b through the Test54c guarded panel;
the SHA-256 check deliberately rejects them. The separate older Test44
workspace remains available for its original narrow use cases.

## Changes inherited from the Test54c ROM

- Test54a: revised ship illustrations for Sambuk, Lancaran and Jong.
- Test54b: role-correct descriptions for 25 ship slots (19 revised, 6 retained).
- Test54c: Rimbo's corrected biography and introduction wording.
- Previously integrated features, ship and NPC fleet rules, prices, stock
  ledger, port relocations, character portraits and walker sprites remain
  within the unchanged exact Test54c bytes.
- The previously reported `~Ernst~` biography heading has **not** been fixed.

### Available guarded controls (same scope as Beta 5.8)

| Control | Native data |
|---|---|
| Independent resale quotation | 100 ports × 46 goods, uint16 |
| Producer Economy requirement | Nine local offer slots per port |
| Ship performance | Tacking, sail power, capacity for 25 slots |
| Port region bytes | Geographic/Autosail region, A–K yard region |
| Equipment-shop special item | Port-to-port swaps with inventory count checks |
| Navigator portrait reference | Two-byte standard fixed-face ID 0–127 |
| Older identity editor | Supported protagonist and faction name/portrait mappings |

The new ship illustration pixels, complete ship descriptions, Rimbo biography,
SRAM stock algorithm and NPC generation code are **preserved but not newly
editable** in this release. The guarded panel uses exact known field offsets;
the original 2 MiB world-map encoder is disabled for protected 4 MiB sessions.

## Test evidence and limitations

**Static functional tests: PASS**

- Embedded Test54c decompression and SHA-256 verification.
- Unedited export equals Test54c byte for byte.
- Independent quote, model, Economy, port, face and special-item edits.
- Snapshot/import restore and unsafe/mismatched-source rejection.
- IPS replay matches the modified ROM output exactly.
- The SNES checksum and complement match the output data.
- All six executable JavaScript blocks compile.

**Not yet gameplay validated:** browser visual walkthrough (Chromium failed to
launch in the execution environment), modified-ROM gameplay boot, save/reload,
story progression, current NPC fleet generation and Jong unlock. The source
Test54c gameplay screenshots support its specific text revisions but do not
prove all newly staged edits are safe in a real emulator. Treat exported edits
as experimental until tested.

**Older settings:** A Beta 5.8/Test53 settings JSON cannot be directly
imported into Beta 5.9. It names a different source hash. Reapply your changes
after checking their values against Test54c, then save fresh Test54c settings.

## Public GitHub source package

The accompanying **ROM-free source ZIP** contains the Beta 5.9 builder,
Beta 5.8 integration templates, static QA runner and reference tables. It has
**no commercial ROM, no bundled private HTML and no proprietary game art**.
It requires the exact private Beta 5.8 HTML and Test54c ROM to rebuild Beta 5.9:

```bash
python3 build_beta59.py \
  --editor '/path/to/New_Horizons_World_Ship_Fleet_Studio_Beta_5_8_Test53_Integrated.html' \
  --rom '/path/to/UWNH_Test54c_Rimbo_Biography_IntroText_EXPERIMENTAL_2026-11-16.smc' \
  --out '/path/to/New_Horizons_World_Ship_Fleet_Studio_Beta_5_9_Test54c_Integrated.html'
```

Keep Beta 5.8 as a rollback. Do not publish your private HTML, any complete
game ROM or commercial artwork. Credit Ken Chee for the project and respect
the game publisher and earlier third-party editor/patch authors.

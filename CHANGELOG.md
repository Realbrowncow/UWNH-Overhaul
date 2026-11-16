# Technical project milestones

- **16 Nov 2026 · Test54c (current):** inserted the owner-approved 130-character Rimbo biography, removed duplicated wording from the two-piece short intro and corrected `far-off`; 164 changed bytes, 4 MiB, SHA-256 `924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01`. Static PASS and two owner gameplay screenshots PASS for the changed text. The `~Ernst~` heading is still visible and unresolved.
- **16 Nov · Test54b:** replaced 19 native shipyard descriptions with owner-reviewed trade/combat wording, retained six, stayed within each original character allowance; static PASS. Selected description screens visually accepted by owner. Complete ROM SHA-256 `712fa01718857fe8398d7c6808c04674e60a0ff7ed0021e23e86ace524f7b7ba`.
- **16 Nov · Test54a:** replaced Sambuk (ID0), Jong (ID11), Lancaran (ID12) shipyard/model images using native 4bpp literal-only compressed streams and three new pointers. 42/42 static checks passed. User accepted Sambuk/Lancaran New Ship images; Jong awaits gameplay confirmation. SHA-256 `c94203089c0bdfa3fd64de39599bc2788209c9439f544424cca423a9dc4eb149`.
- **16 Nov 2026 · Test53:** kept Test52 Rimbo spear source hook, added Hans-specific eight-frame Indian-woman packet redirect; user said the tested walking sprites/portraits looked good. Test53 cold save/Continue still pending.
- **16 Nov · Test52:** Rimbo/Ernst green-haired native packet selectively redirected to African spear-bearing native packet; user separately confirmed persistence.
- **15 Nov · Tests48–50:** two custom 40×48 indexed portraits, shared palette, four fixed-face aliases and original character records; Test50 Rimbo Test5 plus Asmira Face113 chosen.
- **15 Nov · Test47:** applied 25 V8v4 ship models, 64 V4 NPC fleets (416 starting ship positions / 63 generator rules); corrected exclusive Jong from Jepara to Makassar with only two byte flags; static PASS.
- **14 Nov · Tests44–46:** decoded scenario stream structures, relocated Jepara/updated Demak ruler and opening scenes in Test45; town-style Test46 variants rejected.
- **13 Nov · Test43:** eight rare equipment shop moves, 14 port-shop byte changes, exact IPS/static validation.
- **12 Nov · NPC and navigator work:** approved 64/416 fleet design, renamed/repositioned navigators and pirate identities.
- **10–11 Nov · Test33–38:** tested campaign continuation through 1596; fleet freezes reported intermittently; navigators and portraits adjusted.
- **9 Nov · Test31-C:** corrected live `Stock:` count, user gameplay PASS for Salt/Brocade and ordinary save/Continue.
- **2–8 Nov · Test27–30:** integrated 4,600 per-port quotes, commodity names, Economy gates and 286 independent persistent producer-good counters; passed targeted tests.
- **Late Oct–early Nov · 23-port relocation, 25 ships, 7 cannons, Used ships, 100-port pricing:** protected baseline, A–K construction and manual ten-ship control evolved through isolated tests.

Each line summarizes a milestone, not a blanket claim of all-gameplay completion. See [Detailed evidence ledger](docs/testing-and-known-issues.md).

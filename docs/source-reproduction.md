# Source scripts, examples and reproducibility limits

The folder [`examples/recovered_builders`](../examples/recovered_builders/) contains **original research scripts** from selected project milestones: Makassar Jong one-port permission override, custom fixed-face packet import, Test50 selected portrait installation, Rimbo guarded decompressor hook, and Test53 Hans dispatcher. They are *archival case studies*, not turnkey patchers for an arbitrary game file. Their expected source checksums, relative local art paths and external Python libraries are intentionally strict. You must supply your **own lawful exact parent ROM** and create the required source images; do not circumvent their SHA-256 checks by removing assertions.

The public `tools/` directory contains four read-only/general utilities requiring Python 3.10+ without external packages:

```bash
python tools/inspect_rom.py YOUR_ROM.smc --port 33 --good 7 --ship 11
python tools/rom_diff_ranges.py BEFORE.smc AFTER.smc
python tools/apply_ips_checked.py EXACT_PARENT.smc legal_patch.ips NEW.smc \
  --source-sha256 EXACT_64_HEX --expected-output-sha256 EXACT_64_HEX
python tools/verify_test54c.py EXACT_TEST54B.smc EXACT_TEST54C.smc
```

Do not publish the resulting `NEW.smc`. The full private continuation ZIP retains the exact previous ROMs, generated artifacts, user-original spreadsheets and art necessary for further development. In general, distribution of **patches** rather than modified ROM binaries is the appropriate preservation boundary, subject to your legal and licensing review.

The public table exports are derived from the authoritative **Test47 corrected V8v4/V4 reconciled workbook** and are a snapshot, not a writable replacement for the owner's original formulas or formatting. All 25 ship rows, 63 NPC generation rules and 416 starting NPC ship assignments are machine-readable. The special Fleet60 caveat and Jong permission correction still apply.

# Test54a–c follow-up

The latest image, ship-description and Rimbo-intro experiments are documented in [Test54a–c research](test54-ship-pictures-descriptions-rimbo.md). The public repository includes **read-only** [`verify_test54c.py`](../tools/verify_test54c.py), which takes the *exact private* Test54b and Test54c ROM files, checks the approved text and expected SHA-256/diff scope, and emits a JSON report. It never writes a ROM. The actual graphic converter and builder, privately selected PNGs, IPS patches and complete ROMs remain outside the public source tree until the owner separately reviews their publication rights.


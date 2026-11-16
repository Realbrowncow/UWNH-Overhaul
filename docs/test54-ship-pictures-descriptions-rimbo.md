# Test 54a to 54c: ship pictures, shipyard descriptions and Rimbo's introduction

This is the latest incremental research branch in the 16 November 2026 public documentation snapshot. All three experiments are based on the already modified, headerless 4 MiB **USA** SNES game. None is a complete ROM patch for an unmodified retail copy.

## Verified build chain

| Build | Parent SHA-256 | Output SHA-256 | Scope | Evidence |
| --- | --- | --- | --- | --- |
| Test53 | Test52 (see release guide) | `9f91aaa32e91808397b470e58fd3104fe35c5885b554de5bf6e39a2d5efe6b78` | Rimbo/Asmira walking sprites and all earlier integrations | Previously checked portraits and walkers in game |
| Test54a | `9f91aaa32e91808397b470e58fd3104fe35c5885b554de5bf6e39a2d5efe6b78` | `c94203089c0bdfa3fd64de39599bc2788209c9439f544424cca423a9dc4eb149` | Three shipyard/model illustrations | 42/42 static checks; Sambuk and Lancaran owner visual PASS, Jong still not separately confirmed |
| Test54b | `c94203089c0bdfa3fd64de39599bc2788209c9439f544424cca423a9dc4eb149` | `712fa01718857fe8398d7c6808c04674e60a0ff7ed0021e23e86ace524f7b7ba` | Nineteen revised descriptions, six retained | Static PASS; user visually accepted the revised ship descriptions in selected game screens |
| **Test54c** | `712fa01718857fe8398d7c6808c04674e60a0ff7ed0021e23e86ace524f7b7ba` | **`924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01`** | Rimbo biography and two-piece short intro | Static PASS; two captured game screens verify the revised texts |

The hash in the output column identifies a complete private experimental build, **not** an item included in this public research repository. The editor **World, Ship & Fleet Studio Beta 5.8** remains a separate Test53-based tool, not a new Test54c editor release.

## Test54a: shipyard pictures

Three owner-supplied 128 x 96 pixel PNG illustrations were mapped into the native 64 x 48, 4bpp, 16-colour ship-picture representation. Nearest-neighbour downsampling used the existing 16-colour ship palette. Each compressed literal-only stream occupied a newly audited, formerly unused 4 KiB slot. The image pointer table and ordinary SNES checksum were updated.

| Ship ID | Model | 4 KiB allocated PC slot | Picture pointer PC | Result |
| ---: | --- | --- | --- | --- |
| 0 | Sambuk | `0x280000` | `0x02BAA4` | Game screen accepted by owner |
| 11 | Jong | `0x28B000` | `0x02BAC5` | Static decoded artwork PASS; runtime visual check outstanding |
| 12 | Lancaran | `0x28C000` | `0x02BAC8` | Game screen accepted by owner |

Each new stream is 1,731 bytes, and the shared palette at PC `0x0AA8E0` was unchanged. Model statistics, market systems, fleets, characters, portrait faces and walking-sprite bytes were byte-identical to Test53. **Only shipyard/model images changed**: this does not replace world-at-sea or naval-battle moving ship sprites. The Test53-to-Test54a IPS SHA-256 is `3016daf65341365acd3df6dd2ecf1c14d1917c768c91d4aa754b0b922c219ffc` (7,834 bytes).

## Test54b: character-limited native shipyard text

The original game stores the 25 shipyard descriptions in discrete message slots, beginning at PC `0x0B7601`. Nineteen descriptions were rewritten to reflect the **user's trading-vs-combat role design**; six slots retain their original visible text. Each replacement had to fit inside its *own original character allowance*, counting spaces and punctuation, without moving message pointers or hooks. The Galleon is correctly described as a **warship**, not a trader. The new descriptions were reviewed for all 25 models. The message IDs run from 168 to 192.

The precise user-approved slots, lengths and roles are in [`data/shipyard_descriptions_test54b.csv`](../data/shipyard_descriptions_test54b.csv). User-written replacement wording is included; original game prose for unchanged slots is identified but not republished as a new text corpus. Test54b changed 1,372 ROM bytes including checksum bytes; its Test54a-to-Test54b IPS SHA-256 is `1f2965a1246e36acf347ac1803323d2d9eadcc9811b870b1fff5a935342c842c` (1,835 bytes).

**The V8v4 shipyard restrictions are for player construction.** They do not override the user's separately approved V4 NPC fleet compositions or their 63 generation rules. Treat the actual 64-fleet/416-starting-ship workbook as authoritative for NPC mix and do not homogenise AI fleets by region. This exception is game-balancing policy, not a shipyard permission bug.

## Test54c: three character-intro strings

The following offsets are **headerless PC addresses in exact Test54b**. ASCII text is NUL terminated. Replacements must be no longer than the old slot and must not overwrite later messages.

| PC offset | Field | Old maximum | Test54c visible content |
| --- | --- | ---: | --- |
| `0x0EBC25` | Full biography | 148 chars | `Rimbo, a young captain from Demak, charts distant seas for Mercator. With Asmira at his side, he seeks new horizons and adventure.` (130) |
| `0x0B619B` | Short introduction, first part | 61 chars | `Demak sea captain. His friend Mercator asks him` (47) |
| `0x0EB9A2` | Short introduction, continuation | 62 chars | ` to explore far-off lands and make a map of the entire world.` (61) |

The two short parts are rendered consecutively, producing the intended single phrase **“asks him to explore far-off lands”**. Test54c changed **164 bytes** relative to exact Test54b (including four ordinary SNES checksum bytes), yielded checksum `0x8EB9`, and the 252-byte IPS reproduced the exact target (`09825452aeadf5eed49adc98a31e20e5b56050e94677c35622dcd53b6037dbc6`). All 25 native shipyard descriptions and the earlier systems were byte-identical to Test54b. [`tools/verify_test54c.py`](../tools/verify_test54c.py) can independently check the two private ROMs and the exact changed-byte scope; no ROM bytes are included here.

**Gameplay evidence:** the owner supplied two screenshots in a Word report. The full biography displayed verbatim and the short introduction was corrected. Those two narrow behaviours are **GAMEPLAY PASS**; full campaign, cold-save regression and all shipyards were not re-tested by these screenshots.

## An unresolved story title

The full biography panel still visibly says **`~Ernst~`** above the updated Rimbo biography. The raw string `Ernst` at PC `0x04DF31` belongs to another dialogue phrase, not a proven source for that heading. The player-name record near PC `0x088289` already identifies `Rimbo`. **Do not blindly change unrelated dialogue or claim the heading is fixed.** Trace its scenario/title source in a separate experiment and ask for gameplay evidence after the targeted fix.

## Checks still due

1. Trace and repair the `~Ernst~` heading in a *separate* future build.
2. Verify Jong artwork in the Makassar shipyard after any Industry-gate investment needed; no Jong should become available in Jepara.
3. Run ordinary New Game → Save → emulator restart → Continue with version-matched SRAM (not a cross-ROM emulator save state).
4. Run focused regression checks for market stock, region-C yards, a contrasting pair of NPC fleet screens and the previously approved walking sprites.

The user-approved Test54c is the **latest integrated, observed-to-boot experimental build**, not an assertion that every system passed exhaustive gameplay validation.

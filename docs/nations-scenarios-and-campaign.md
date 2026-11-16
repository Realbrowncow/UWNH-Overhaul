# Demak, nations, scenario scripts and the 75-year campaign

## Demak as a real in-game nation

The project repurposed the former **Holland national slot 5** as **Demak**. The approved starting allied ports in the Demak branch are **Jepara 100%** and **Bankao, Sunda, Dili, Makassar, Banda 80%**. The Jepara capital is port **ID33**, derived from the original Amsterdam slot, not original Mecca ID77; Makassar is ID77. Capital Industry investment remains unavailable. The palace sphere-of-influence uses native owner/support fields: the user checked the palace count and saw dynamically acquired allied ports after investing in game.

Test45 also changed the palace guard's shared line from **“the King”** to **“the ruler”**, selected a Sultan Trenggana portrait and observed the ruler/palace scene in gameplay. Earlier Test46 attempts to switch Jepara architecture to Style4 with two different palettes failed. **Style1/Palette0 is retained**. Do not silently merge the abandoned architecture images back into the latest branch.

The project owner directed that culturally specific architectures — especially original African town styles — remain intact unless a separate art-style change is approved. Physical relocation is not a blanket change of port architecture, climate, nation, or town services.

## Rimbo and Asmira as the narrative pair

The Ernst protagonist was renamed **Rimbo** and the Hans-linked companion **Asmira**. Test45 compressed-dialogue adaptation preserved 263 native dialogue identifiers and `$n` placeholders while changing the story names and selected terms of address; the opening Mercator and Asmira scenes were observed in relocated Jepara. The final Test50 fixed faces and Test53 town walkers are covered in [Portraits and walkers](portraits-and-walkers.md). Changing a visible navigator name is *not* equivalent to rewriting all compressed story streams or dialogue-trigger conditions.

## What was decoded from the six scenarios

Test44 reverse engineered a scenario script interpreter around **PC `0x09B54A`**, enumerating **42 instruction handlers, 102 conditional entries and 24 numerical gates**, with stream-relative big-endian destinations. The research identified six starting compressed blocks:

| Scenario | Headerless PC block |
| --- | ---: |
| João Franco | `0x0FD72F` |
| Catalina Erantzo | `0x0FF7C6` |
| Otto Baynes | `0x10133F` |
| Ernst / Rimbo | `0x102563` |
| Pietro Conti | `0x1F0000` |
| Ali Vezas | `0x1F0972` |

The Test44 audit enumerated **35 modules, 150 streams and 721 entries** and decoded many port/Fame gates, but did not prove every campaign quest route or every gameplay variable meaning. For a new capital/starting-port edit, inspect trigger conditions, cached port ID, actual ship spawn and the compressed text independently. The earlier Test45 relocated Amsterdam experiment is valuable precisely because it separately tested the opening scene, port recognition and ordinary save/exit position.

## Campaign extension to 1596

The project extended the native campaign boundary by roughly **75 years**. Test33 testing reported that 31 December 1595 / 1 January 1596 and 31 December 1596 could load and play, while **1 January 1597 triggered retirement/ending**. A fresh New Game still began at the original 1522 start in the tested branch; extending the deadline does not itself change the six scenario start years. Save compatibility and multi-scenario edge cases require case-specific testing.

## Known adjacent research

- Autosail Test22 menu heading overrides corrected some relocated-city **labels**, including Poseidonis under Central America and Goa under India. The actual ship route toward relocated Poseidonis remained incorrect; the user explicitly deferred it.
- Exploring inn-to-tavern navigator movement, hiring by nations, pirate pathing, portrait lists and additional scenario gate semantics is ongoing research, not completed production functionality.
- Changing the visual nation flag/ensign for Demak was **not proven** as a separate resource; do not overwrite an arbitrary Holland icon without tracing the correct art table.

## Safe modification workflow

If changing a ruler, capital, ally or character: use port/nation IDs, update native owner/support fields, check all compressed references, then run a fresh start and actual palace/investment/story scene. If extending time, test the day before, the rollover day, the final permitted day, and the ending day as **distinct saved checkpoints**. Keep every successful intermediate ROM and a hash-labelled IPS.

# Independent purchase and resale prices for 100 ports

## The original limitation

The original game uses **13 regional market categories**, each carrying prices for 46 goods (598 regional pairs), and special port rules. A port relocation can inherit a completely inappropriate old regional price. We wanted each of **100 actual ports** to control its own market quotations, with a producer/resale system that no longer depends on the city's old regional identity.

## The implemented table

Test27 merged the user-gameplay-tested POC12 price patch onto the Test26 shipyard ROM. The full table contains **4,600 unsigned 16-bit resale quotations**. It uses a **128-byte port record** in expanded bank E4:

```text
PC_price = 0x240000 + (port_id * 128) + (good_id * 2)
port_id  = 0..99
good_id  = 0..45, native ROM good-ID order
price    = little-endian unsigned 16-bit quotation at PC_price
```

Example: for port 33 and good 7, entry PC = `0x240000 + 33*128 + 7*2 = 0x24108E`. Read two bytes in little-endian order. **Do not write that example number into the ROM without checking its good-ID mapping, approved workbook value, scenario index and price index.** The same 128-byte port block also stores local producer slots and Economy gates after the price entries; do not overwrite the rest of the block during a price edit.

Test27 applied **two original quote-callsite changes** and copied verified POC12 helper code/data in bank E4, plus disabled old specialty flags on 67 native port records so the legacy exception cannot replace the new quotation. It changed **13,491 bytes** relative to Test26, including four checksum bytes. All 4,600 cells were compared to the source audit. An exact-source IPS reconstructed the combined ROM byte-for-byte.

The research landmarks are the original resale quote routine `$C6:9AAC`, goods list `$C6:9A50`, market index `$7E:2126`, good selection `$7E:2128`, and native regional pointer construction at `$C5:01FA` / `$C1:FF20`. The added helper replaces/redirects the relevant lookup so it selects by **port ID and commodity ID**. We know the table base and stride from the surviving Test27 source audit; a separate finalized full **producer buy-price table offset** was not recovered, so do not claim a second 4,600-entry buy table resides at a guessed address. The producing-port purchase price is a separate transactional path from the resale quote.

## Creating approved prices

1. Maintain a master CSV/workbook with **100 explicit port IDs** and **46 native good IDs**. Never use alphabetic display order as a ROM index.
2. Set producer base prices and **10% of base** producer-port buyback where approved. This refers to what the port will pay for goods sold back to its producer, not free purchasing by the player.
3. For 38 distance-sensitive goods, calculate a tier from **navigable sea-square distance to the nearest producer**. Commodity groups have 4–8 reachable maximum-distance tiers; the commonly used eight-band reference is 0–200 = 12.5%, through 1,401+ = 100% of the defined distance uplift. Apply the approved commodity-specific tier schedule, not one generic world radius.
4. For eight fixed-price goods, use their fixed base conventions. Designated fixed-price premium markets multiply by **1.6**, whereas designated distance-sensitive premium ports advance one tier (and can advance to an extra top tier).
5. Apply named premiums: Arms at Goa, Malacca, Hormuz, Mozambique and Alexandria; Ambergris at Lisbon, Venice, Alexandria and Istanbul; Salt where Meat and Fish are available; Sugar where Fruits are available; Iron/Wood/Copper at approved large-shipbuilding ports; Myrrh at Changan/Ningbo/Ayutthaya. Fur at **43 warm non-producing ports** uses a **0.8×** price modifier.
6. Encode the approved integer prices, compare **4,600 out of 4,600** back to the workbook, and only then patch the game. The final displayed quote also reflects the game's category market price index. Test27's guide gives `floor(nominal_price * displayed_category_index / 100)` for test expectations.
7. Run short in-game checks of *both* producer purchases and resale: a quote appearing in the UI and a transaction crediting cash are different behaviours. Test a low port ID and the highest port IDs, **Sakai 98 and Nagasaki 99**, to catch index overflow.

## Changing one price safely in a later chat

1. Confirm the exact current ROM SHA and approved good ID/port ID. Make a new experiment, never edit the preserved baseline in place.
2. Read the 16-bit value at the formula above and compare it with expected nominal workbook value. Confirm whether the desired revision changes a **resale quote** or a **producer purchase offer**.
3. For a resale quote, write exactly the two bytes at that entry, recompute the SNES checksum/complement and create a matching IPS. The stock counter, Economy byte, native specialty flags and port metadata should remain unchanged. If a base-price edit also changes linked premium destinations, regenerate the whole derived matrix from the approved source rather than manually changing a single quote.
4. Verify no other data changed; exercise the merchant quotation at the same category price index and complete an actual transaction.

## Milestones and verification

- POC6 demonstrated independent Genoa/Venice quotations. POC7 extended the mechanism through port IDs **98 and 99**. POC12 tested **23 price quotations and 4 transactions** in game.
- Test27 integrated pricing with Test26 yard code; later Test28 renamed goods; Test29 added approved 46-good Economy gates; Test30 added 286 persistent counters; Test31-C added live remaining-stock display.
- Test31-C user screenshots confirmed Amsterdam **Salt 24** and **Brocade 288** at the observed indices, with correct money/cargo changes and their stock values persisting after ordinary reload. This does **not** imply every price across 100 ports was played.

For raw address reference and checksums, see [ROM address map](rom-address-map.md).

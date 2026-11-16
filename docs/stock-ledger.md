# Individual commodity availability, Economy gates and live stock UI

## From category prototype to independent goods

Early experiments limited a purchase to 20 units and a local category to 60 units, but did not persist correctly across ordinary game saves. Later 8-good pilots established a persistent counter path, after which **Test30 installed all 286 approved producing port–commodity pairs**. This is **not** 4,600 saved counters: most port–good combinations are not producers and have no stock item.

| Property | Current mechanism |
| --- | --- |
| Seller combinations | 286 approved producing port–good links across 100 ports/46 goods |
| Independent counters | 286 `uint16` consumed-quantity words, sparse indexed by port and local product |
| Physical `.srm` offset | `0xA020..0xA25B` inclusive, 572 bytes |
| SNES mapped SRAM | `$25:6020..$25:625B` |
| Version identifier | `$25:6004`, value `0x4D39` (Test30 schema) |
| Restock schedule | Four-month intervals; rollover in **January, May, September** |
| Maximum quantities | Approved 46 per-good caps ranging **1,000–3,000** units |
| Player sale to market | Does **not** refill available producer stock |

The wrapper indexes the active port into a local producer list (up to nine local offers and terminator), then substitutes that **good-specific consumed count** in the native stock quantity/commit paths. A producer's Grain and Meat no longer consume the same category pool; Amsterdam Salt and Brocade maintain separate counters. New Game and cycle rollover reset all 286 counters. A save with an older marker initializes only the new ledger when a producing good is next checked, a compatibility method that must still be tested against real legacy saves. The user-approved exact caps and `(port, good)` producer list are reproduced in [`data/stock_limits_46_approved.csv`](../data/stock_limits_46_approved.csv) and [`data/stock_producers_286_approved.csv`](../data/stock_producers_286_approved.csv). The `Planning slot*` in the first CSV is a source workbook index, **not necessarily the ROM good ID**.

## Economy threshold in the ROM

The 128-byte per-port pricing/offer block also contains producing-commodity Economy requirement bytes:

```text
PC_gate = 0x240000 + port_id*128 + 119 + local_offer_slot
stored_byte = required_Economy / 10
```

Test29 changed **158 requirement bytes** and four checksum bytes to apply user-approved requirements 0–700; 216 producing links initially met their gates, and 70 were initially locked. Reval Economy300: Meat (0) and Amber (150) yes, Fur (450) no. Danzig Economy370: Grain/Amber yes, Copper Ore (500) no. Amsterdam Economy700: Salt and Brocade yes. These are focused test examples, not permissions to change a port's own Economy when only a good requirement is intended.

## Stock value is not the cargo value

Native `Left` describes a player's ship cargo allowance, not inventory held by the port. Tests31-A/B/C added a new separate `Stock: N` line to the Merchant Buy dialog. Test31-B mistakenly read a **virtual deficit offset** as a cap; Test31-C calculates:

```text
maximum_stock = 3000 - virtual_stock_offset
remaining = max(0, maximum_stock - consumed_units)

Example: Salt virtual offset = 300
maximum Salt = 2700
consumed = 2699 --> Stock: 1
buy one --> consumed = 2700 --> Stock: 0
```

The temporary virtual offset is at `$7F:F824`. The display and purchase upper bound then agree. The **user's 9 November Test31-C gameplay screenshots** show Amsterdam Salt `1→0`, Brocade independently `1→0`, prices and ducats correct, and both zero values retained after an ordinary Save, emulator exit and Continue. Values like `Stock: 2700`, all 286 records, and every restock refresh were **not** exhaustively user tested.

## Replication recipe

1. Preserve the approved list of 286 `(port_id, good_id, cap, Economy_gate)` tuples and a mapping from `(port_id, good_id)` to its sparse counter index.
2. Allocate enough SRAM for `286*2` plus version marker, with collision review against the native save schema. Keep market and ship code unchanged.
3. At purchase selection and commit, resolve the current port and producing good, compute `remaining`, clamp purchase quantity to that remaining amount, and increment only the selected counter. Use identical calculation for the text renderer.
4. On ordinary game Save, commit counters; on Continue, load the matching version or migrate safely; on Jan/May/Sep rollover, reset counters once. Port switching and selling goods must not reset or refill them.
5. Validate at zero, one, cap−1 and cap, across ordinary cold Save/Continue, multiple same-category goods and the four-month boundary. Verify `.srm` words directly in addition to screenshots.

Use the exact Test30 mapping CSV and Test31-C patch audits from the original private development archive if altering any SRAM offset. The public guide describes the observed layout but does not recreate all 286 sparse index entries from memory.

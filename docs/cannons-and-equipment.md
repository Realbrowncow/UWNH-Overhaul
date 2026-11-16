# Seven cannons, rare equipment and manual fleet commands

## The seven cannon tiers

Our weapon redesign gave each of the native cannon types a distinct Economy/Industry unlock tier, firing distance and tactical role. The exact approved table below is the design; later battle effectiveness remains governed by original game battle logic and not every combination has been user tested.

| Cannon | Industry requirement | Firing range |
| --- | ---: | ---: |
| Saker | 0 | 2 |
| Demi-Cannon | 200 | 3 |
| Demi-Culverin | 400 | 2 |
| Cetbang | 600 | 3 |
| Cannon | 800 | 4 |
| Culverin | 1000 | 4 |
| Carronade | 1200 | 2 |

The original cannon attribute tables were traced at headerless **PC `0x0B0929` (additional stat), `0x0B0939` (range), `0x0B0949` (power), `0x0B0959` (price)**. Their fields must be reviewed as arrays and matched to the actual cannon IDs in the editor before editing. The full native battle-damage formula was not conclusively reverse engineered in the early project research; never promise direct damage from range/power alone.

## Rare equipment shops

Test43 moved **eight named special item offers** among selected port equipment shops, using the **special-offer byte `+32`** of each **37-byte native port record**:

```text
PC_special = 0x08DA7F + 37*port_id + 32
```

The 13 November Test43 audit reported **14 such slot-byte changes** for eight requested equipment moves, preserving **32 rare + 139 ordinary shop offers**, with no duplicate same-port items, exact IPS roundtrip and valid checksum. The eight approved item moves are preserved in [`data/special_item_relocations_test43.csv`](../data/special_item_relocations_test43.csv):

| Item | From | To in Test43 | Important caveat |
| --- | --- | --- | --- |
| Tax-Free Permit (P) | Salonika 17 | Goa 9 | Native slot ID retained |
| Tax-Free Permit (O) | Tripoli 22 | Azov 24 | Part of coordinated original item move |
| Tax-Free Permit (S) | Azov 24 | Tripoli 22 | Part of coordinated original item move |
| Tax-Free Permit (H) | Antwerp 32 | Hamburg 35 | Native slot ID retained |
| Tax-Free Permit (E) | Danzig 39 | Bordeaux 27 | Native slot ID retained |
| Rune Blade | Pernambuco 52 | Poseidonis 3 | Relocated port name |
| Crusader's Sword | Timbuktu 64 | Jepara 77 (Test43 name) | **Current Test53 ID77 is Makassar**; follow port ID, not stale display name |
| Crusader's Armor | Naples 10 | Suez 75 | Renamed destination |

The normal equipment inventory and adjacent port fields must remain intact. The CSV also records each native item ID and `+32` slot byte address for exact reproduction.

## Ten-ship manual fleet control

The project integrated a **Manual Control patch** so all ten player ships can be ordered directly in naval battles. The user performed gameplay tests on this behaviour. A crucial house rule: **only the flagship/captain initiates duels**; subordinate ships 2–10 can be manually commanded but do not initiate their own duels, because native subordinate duel resolution can unexpectedly end the battle or trigger Game Over. Test this after any major fleet/combat engine merge.

## Editing safely

For cannons, record the current value in each separate native attribute table; change only named weapon entries and recalculate checksum. For equipment, use the port ID rather than the rendered city name, especially after relocations; confirm no duplicate item and compare all 100 offer records, not just one port. For manual control, avoid overwriting its code hooks with unrelated naval battle experiments and always test an actual battle rather than only the menu.

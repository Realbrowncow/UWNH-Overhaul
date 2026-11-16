# ROM address map and editing fundamentals

## Scope and numbering

The current project ROM is the **USA SNES, 4,194,304 bytes, headerless**. Do not apply the familiar `+0x200` copier-header adjustment to these files. A historically supplied `.smc` *with* a 512-byte copier header would need a separate normalization step; extension alone is not evidence of one. The SNES CPU is a 65816. ROM PC offsets and `$bank:address` SNES addresses are two different coordinate systems; use the established mapping for each bank and check any long jumps.

When changing a built ROM: verify the complete SHA-256, copy it to a new filename, record allowed byte ranges, update checksum/complement at PC `0xFFDC..0xFFDF`, generate an IPS relative to that **exact source**, and replay the IPS to prove an exact match. The protected 23-port baseline and previously accepted checkpoints are immutable.

## Consolidated observed addresses

| PC offset / RAM | Record or hook | Confirmed interpretation / caveat |
| --- | --- | --- |
| `0x08CF53 + 22*i` | 130 named-port/supply records | X little-endian at +0, Y at +2, name block +4..+19, starting-known +21 |
| `0x0AA1DE` | 130 sorted coordinate entries | Updated alongside moved physical ports |
| `0x0AD170` | Port pointer/lookup table | Core resolver source |
| `0x0F3500` | 255-slot near-port hash | Must be regenerated when relevant |
| `0x02F86B`, `0x02F12F` | Region/discovery coordinate indices | Cross-check after location edits |
| `0x08DA7F + 37*p` | 100 port records | +32 special equipment; +33 original geographic/Autosail region; +34 A–K shipyard region |
| `0x070C4B` | Autosail menu region filter | Reads original `+33`, shared with other logic |
| `0x070C6D`, `0x070CED` | Autosail known-port checks | Starting-known bit `0x10` |
| `0x052483`, `0x06361D`, `0x068B0B`, `0x07995C` | Other geography consumers | Avoid global edits to port `+33` solely for Autosail |
| `0x08CE27 + 12*ship_id` | 25 ship model records | Model speed at +2/+3, total capacity +6; all fields must be audited |
| `0x08CBB6 + 25*ship_id` | Native per-ID ship template | Does not alone create separate Used-versus-New speed/capacity |
| `0x0AA522` | Used regional candidates | 11 × 8 native candidate table |
| `0x0A5B33` | Used general/worldwide draw | Bypassed for approved region-only offers |
| `0x0B0929`, `0x0B0939`, `0x0B0949`, `0x0B0959` | Cannon attributes | Historical additional stat, range, power, price tables |
| `0x240000 + 128*p + 2*g` | Independent resale quotes | 4,600 16-bit values; `p=0..99`, `g=0..45` |
| `0x240000 + 128*p + 119 + slot` | Producer Economy byte | `0–700` Economy requirement encoded as requirement/10 |
| `$25:6004` | SRAM stock schema marker | Test30 `0x4D39` marker |
| `$25:6020–$25:625B` | 286 consumed counters | 286 × 2 bytes = 572 bytes; physical `.srm` `0xA020..0xA25B` |
| `$7F:F824` | UI temporary virtual stock offset | Actual cap = 3000 − virtual offset; not the cap itself |
| `0x02BCB7 + 3*face_id` | Fixed face pointer | Three-byte difference from PC origin `0x17CEE9` in this module |
| `0x0AAF00 + 32*face_id` | Fixed face palette | 16 SNES BGR555 words |
| `0x0881F3 + 50*navigator_id` | Navigator records | Face ID field at +26 as a little-endian word, shown in Test50 source |
| `0x00A0BE` | Native walker decompressor wrapper | Test52/53 source-selection JML interception |
| `0x250100`, `0x250140` | Sprite hooks | Test52 Rimbo and Test53 Hans dispatch code respectively |
| `0x1BE5F2`, `0x1BB35F` | Rimbo source and spear | Original Ernst graphics and selected African spear packet |
| `0x1C5CB3`, `0x1BCBD6` | Hans source and woman | Exact Hans packet and selected Indian-woman packet |
| `0x09B54A` | Scenario interpreter | Read-only Test44 reverse engineering; 42 handlers identified |
| `0x0FD72F`, `0x0FF7C6`, `0x10133F`, `0x102563`, `0x1F0000`, `0x1F0972` | Six main scenario blocks | João, Catalina, Otto, Ernst, Pietro, Ali respectively |

Do not assume these ranges are all interchangeable free space. For example, `0x240000` is an **occupied** extended price/offer table by Test27 and later. The portrait packet allocations in bank `0x20` are also occupied, and the Test52/53 hook allocations in bank `0x25` are in use. Check for `0xFF` fill, overlaps, pointers and code execution before allocating new bytes.

## Merchant disassembly landmarks

The early 65816 research found purchase entry `$CE:210A`, affordability `$CE:2264–2281`, selection `$CE:22C1–22EA` and `$CE:2300–2329`, payment `$CE:2454–246C`, cargo `$CE:246D–249E`, sale `$CE:3B73–3BB0`, and market/category helpers `$C6:9AAC` and `$C6:9A50`. These are *research landmarks*, not proof that every later hook remains at those native locations. The good list and quote use the selected market/commodity working RAM, including `$7E:2126` and `$7E:2128`.

The local browser Port Relocation Beta and the native UWNHRando Theme Editor operate at different layers. Read the port guide before applying any editor output to the latest branch.

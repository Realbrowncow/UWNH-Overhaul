# NPC fleets, navigators, portraits and roaming pirates

## 64 fleets and 416 starting hulls

The user-approved V4 fleet design covers **64 NPC fleets**, **416 initial ship positions**, and **63 ordinary generation-choice rules**. Test47 changed **37 of 63 native rules** and **188 of 416 starting hull selections** compared with its previous branch. It preserves fleet sizes, captain links, 43-byte headers, status/unused slot bytes and native factory templates; crew, hull, sails and guns were rebuilt/clamped where the hull changed.

The 63 native generator rule addresses are individually recorded in the `V4 63 Rules` worksheet and exported to [`data/npc_fleet_rules_v4.csv`](../data/npc_fleet_rules_v4.csv); typical addresses include PC `0x09EC4D`, `0x09EC4F`, `0x09EC51`. Each rule has three possible hull choices. The user-original V4 workbook's **`64 Fleet Projection`** sheet, columns **I–K**, is the correct choice source, not older content still retained in tabs named `V4 Rules redo` or `416 Ship Projection redo`.

**NPC generation is not constrained to the same A–K construction choices available to players.** NPC hull rules may cross regional build boundaries for variety. Nevertheless the user specified **no Large ship IDs in ordinary NPC fleets or generation**, and **Hansa Cog only for Holland/Dutch NPCs**. Sambuk and Lancaran were excluded from ordinary generated NPC rosters. Special scripted **Fleet60** has a distinct ten-ship Lancaran/Sambuk initial arrangement; its separate future routine was **not** patched by Test47. Never conflate Fleet59 and Fleet60.

User-selected V4 source and applied ROM reconciliation are not the same thing as gameplay confirmation. **Fleet screens and future new-ship generation were still awaiting broad testing** after Test47, and the earlier Diego ship-list freeze is a reason to keep that regression test in the plan.

## Navigator stat and location work

The project changed names, portraits, sailing levels, combat levels, starting locations and selected skills across the navigator roster. An extended **120 navigator record** region begins at PC `0x0881F3`, with **50 bytes per record** in the Test50 audit. For example, the face reference was checked as a little-endian word at `+26`. Treat name length, level/skill bounds and original face references as distinct fields; editing a face number does not import graphic art.

Selected Test35 North Sea navigator attributes were changed and tested; Lawrence Edwards can have a high level without automatically being recruitable at the scene tested. Test36 remapped portraits for **Antoine Fitch (ID99→124), Klaus Shouten (ID106→125), Patrick Toman (ID109→126), George Eggel (ID116→127)**, and the user found them correct at café/inn and map. Test37 renamed these four as female navigators; Test38 placed all four in **Antwerp (port ID32)** and the user observed the inn/café presence.

Other checks concern whether recruitable NPCs remain present after hiring by a nation, whether inns versus taverns can be remapped, and the behaviour of Gus Johnson, Mohammed Syarook and special pirate parties. Those investigations are not blanket gameplay PASS results.

## Four special pirates

Four roaming pirate identities remain roaming **without assigned starting ports**, while their names, stats and face references were customised:

| Original pirate | Navigator ID | New identity | Portrait ID |
| --- | ---: | --- | ---: |
| Pierre Lugulan | 61 | Mary | 112 |
| Louis Scott | 62 | Grace | 101 |
| John Davis | 63 | Sayyida | 121 |
| Jack Raccam | 68 | Eleanor | 117 |

They should not be converted into ordinary tavern recruits just because their location byte resembles a special or empty value. Verify their pirate-sailing encounters independently.

## Modding workflow

1. Identify captain/navigator by stable **ID**, role and actual record/ship fleet; do not search only by display name after renames.
2. For fleet creation, change both the **416 initial ship records** and the **63 runtime generation rules** as needed. A startup roster and future replacement-generation are different paths.
3. Apply the no-Large, Hansa Cog exclusivity and approved game-role rules; clamp crew, cannons, hull and condition to the selected ship model. Preserve headers and status bytes.
4. For navigators, edit the exact 50-byte record and any other character-selection/plot references that use the prior name or portrait. Validate portrait ID and target graphic as separate tasks.
5. Static audit full tables; start fresh, inspect multiple fleet screens, wait for an NPC ship-regeneration event, save/reload, check named navigators and pirate encounters.

See [Portraits and walkers](portraits-and-walkers.md) for image packet techniques and [Testing](testing-and-known-issues.md) for the known Diego screen concern.

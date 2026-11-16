# How we changed portraits and four-direction walking sprites

## Two very different graphics systems

**Large face portraits** are **40 × 48 pixels**, 16 indexed colours, SNES 4bpp: 30 8×8 tiles × 32 bytes = **960 uncompressed bytes**. The fixed-face pointer and palette tables must direct the relevant character IDs to the same selected art.

**Town walking sprites** are **16 × 16 pixels per frame** and use an **eight-frame packet** of 1,024 decompressed bytes (8 × 4 tiles × 32). Frames include directional poses. These are loaded and decompressed dynamically; changing an emulator VRAM snapshot will not survive normal room transitions. Test52/53 used a guarded ROM-code source redirect to existing native art.

## Large portraits — exact ROM method

Test48 established a verifiable import path; Test49 corrected all-view references; **Test50** installed the user's final Rimbo Test5 image and Asmira Face113 without re-quantisation or changing the shared palette. There are **two fixed-face aliases per character**:

| Character | Navigator record | Fixed face aliases | Allocated art packet |
| --- | --- | --- | --- |
| Rimbo / Ernst protagonist | ID3, face24 | 3 and 24 | PC `0x200F00` |
| Asmira / Hans | ID77, face113 | 39 and 113 | PC `0x201400` |

Face pointers reside at `PC 0x02BCB7 + face_id*3`; in Test48 the stored 3-byte little-endian value was a **relative offset from `PC 0x17CEE9`**. The 16-colour BGR555 palette is at `PC 0x0AAF00 + face_id*32`. Navigator face fields are in records at `PC 0x0881F3 + id*50 + 26`. Updating the graphic packet alone is insufficient if the selection screen, town dialogue and Character View use different aliases or navigator record IDs.

In these builds the portrait codec uses a **literal-only packet**. For 960 raw 4bpp bytes, the encoder writes `FC 01`, then for each 8 raw bytes a flag `FF` followed by those eight bytes, ending in `00`: **1083 bytes**. It fit in allocated **0x500-byte** slots. The source Test48 builder first proved existing Test47 packets round-tripped before emitting new ones. This format is empirically valid for those packet instances; do not assume it encodes every native compressed image type.

### Repeatable face replacement

1. Get an original source image at **40×48** with exactly **16 shared ROM palette colours**. If using the enlarged 3× screenshot art, scale by **nearest neighbour only**; no blur, anti-alias, dither or new colours.
2. Convert the 40×48 indexed pixels into SNES planar 4bpp tiles. For each 8×8 tile, pack bit planes 0/1 into 16 bytes and planes 2/3 into another 16. Assert **960 bytes** and decode back to an identical RGB image.
3. Encode the **1083-byte literal packet**, allocate a verified unused block and insert it; recompute 3-byte relative pointers for every face alias. When a palette is shared, preserve it exactly, especially other characters' palette entries.
4. Update only the specific character record's face ID where needed; do not globally reassign a face slot shared by another NPC without identifying every user.
5. Save the source PNG, 4bpp raw asset, new ROM, exact-source IPS and allowed-byte audit. Re-extract the face *from the output ROM* and pixel-compare it to the source.
6. In game, check **six-character selection**, status/Character View, dialogue scene and at least two contexts, then ordinary save/reload. A fixed face may have separate aliases for those contexts.

Test50 asserts portrait packets, 16-color shared palette, aliases and all 120 navigator records, replays its IPS, and checks the SNES header. Its changed-byte allowlist covers only the two 1083-byte data windows and checksum; source images were exactly matched without palette loss.

## Walking sprite selection — Test52 and Test53

User clarification was crucial: **Rimbo's original walking role is Ernst**, the formerly green-haired sprite; **Asmira's original role is Hans**, the blue-clothed figure. The user previously supplied a reference atlas with the African spear holder facing in all directions; we matched the native ROM packet instead of redrawing or copying an emulator state.

| Character | Native source before | Desired native packet | Frames and implementation |
| --- | --- | --- | --- |
| Rimbo / Ernst | `0x1BE5F2` = `$DB:E5F2` | African spear `0x1BB35F` = `$DB:B35F` | Test52 guarded source-offset/bank intercept; 8 frames |
| Asmira / Hans | `0x1C5CB3` = `$DC:5CB3` | Indian woman `0x1BCBD6` = `$DB:CBD6` | Test53 exact Hans guard, temporary source-bank override; 8 frames |

Test53 matched the Hans source against an in-game screenshot at the native 16×16 pixel grid. It did not guess that another character's slot represented Hans. The original packets themselves remain **byte-identical**; no global sprite bank or palette table was replaced. Other townsfolk fall through the original loader.

### 65816 hook layout

The native decompressor wrapper begins at **PC `0x00A0BE`** (SNES `$C0:A0BE`). Test52 changed its opening instruction to a long jump to a fresh handler at **PC `0x250100`** (SNES `$E5:0100`). That handler executes the relocated original prologue, checks the **exact source bank `$DB` plus offset `$E5F2`**, and pushes the African spear source `$B35F` when matched. All other sources proceed unchanged to the existing `$C0:A0C8` continuation. It deliberately preserves the native direct-page `$56` pointer, stack layout and register widths.

Test53 retains Test52's 36-byte handler **identically**, but points the wrapper at a small dispatcher at **PC `0x250140`**. When the source is **`$DC:5CB3`**, it chooses `$DB:CBD6` in a scratch register and uses a **native-bank trampoline at `0x00A0C2`** to call the decompressor with its expected stack layout; for all other sources it delegates to the original Test52 handler. A `JML` is necessary in part because a careless `JSL` return frame would corrupt the native loader's unusual pushed parameters. The bank in DP `$58` is not changed globally.

The Test53 patch's only permitted changes relative to exact Test52 are the loader entry, the six-byte trampoline, the 45-byte Hans dispatcher, and four checksum bytes. Its binary audit separately verifies all sprite compressed streams and the entire protected portrait region are unchanged. Source SHA and output SHA are in the [continuation guide](continuation-and-releases.md). This is a *specific* 65816 source-hook pattern, not a universal patch for all 16×16 sprites.

## User-observed status

Test52: the user previously checked Rimbo's spear sprite and ordinary save/reload. Test53: in `test48e walking sprite5.docx`, the user said **“looks good”** after seeing the Rimbo spear bearer, Asmira Indian-woman walker and their portraits in rooms/dialogue/outdoors. This is a **specific visual gameplay PASS**. A separate Test53 **cold ordinary game Save / emulator close / Continue** cycle was **not** confirmed; do that before treating persistence as fully regression-passed. Older SuperZSNES save states may embed old graphics/pointers and may fail to load across major ROM changes: use a fresh New Game or the correct `.srm`, not a mismatched `.szst` snapshot.

## Future variant work

For another NPC face, first check whether its palette is shared, what fixed-face aliases it uses, and whether the same navigator ID is referenced by the character-selection logic. For another walker, identify its **exact source packet** by decompiling the eight frames and comparing the 16×16 screenshot pixels. Do not redirect all sprite sources to a desired art address, and always preserve code/state fall-through for unrelated characters.

# Test56q — Clean US ROM upgrade (20 November 2026)

**Public experimental build. No commercial game ROM is distributed here.**

This is a cumulative IPS patch for the **original, unmodified US SNES** version of *Uncharted Waters: New Horizons*, not an update to Test54c or another modified ROM. The easiest method is the ROM-free offline upgrader.

- [Download Easy Offline Upgrader ZIP](https://github.com/Realbrowncow/UWNH-Overhaul/raw/refs/heads/main/releases/UWNH_Overhaul_Test56q_Easy_Upgrader.zip)
- [Download Test56q cumulative IPS](https://github.com/Realbrowncow/UWNH-Overhaul/raw/refs/heads/main/patches/test56q-clean-us/UWNH_Overhaul_Test56q.ips)
- [Illustrated installation guide](https://cheeken78.wordpress.com/uncharted-waters/test56q-installation-guide/)

## Use the offline upgrader

1. Download and extract the ZIP to a normal folder.
2. Open the included `UWNH_Test56q_Easy_Offline_Upgrader.html` in a modern browser. It works offline and does not upload your ROM.
3. Select your own clean, unmodified **US** ROM (2,097,152 bytes, **no 512-byte copier header**).
4. Click **Verify and Create Test56q**. The tool verifies the original, applies the included cumulative patch, verifies the result and prompts a download.
5. Open the resulting `.smc` file in your SNES emulator.

The original ROM is unchanged. A clean ROM is **required**; do not apply this to Test54c, Test55, Test56p, or another hacked ROM.

## Verification

- Original clean US ROM SHA-256: `64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0`
- Test56q output SHA-256: `a8e72f2b9c8db2be7e6f5c10852cd0282cc13b0eea681cc450e398ebaa5aff9b`
- Output size: **4,194,304 bytes**
- IPS records: **2,714**

The cumulative IPS is provided for users who already know how to use an IPS patcher; use only an unchanged copy of the same clean US ROM. The offline upgrader is recommended for most players.

## Test56q status

Test56q continues the extended project, including revised ship design, trade, ports, navigators and experimental town dialogue. Gameplay spot checks confirmed Jepara's duel warning and Onim's exclusive-goods dialogue. These limited checks do **not** establish a complete gameplay regression pass of every location or event. Test57 duel experimentation is separate and is **not** included here.

**Credits:** Ken Chee (Realbrowncow). For research/experimentation with a user-supplied ROM. No ROM included.

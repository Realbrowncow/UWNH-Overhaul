# Publication and intellectual property checklist

This public repository contains original research notes, derived design tables, general read-only tools, and a cumulative Test54c IPS patch package. It does **not** host the original or modified commercial ROM, separate game artwork or audio files, emulator states, or personal save games. An IPS contains changed binary bytes and is not automatically covered by the project licences.

The [Test54c clean-US IPS](patches/test54c-clean-us/UWNH_Test54c_CUMULATIVE_from_Clean_US_ROM_2026-11-16.ips), [ZIP](releases/UWNH_Test54c_Clean_US_ROM_IPS_GitHub_2026-11-16.zip), [instructions](patches/test54c-clean-us/README_Test54c_Clean_US_IPS_2026-11-16.md), and [audit](patches/test54c-clean-us/UWNH_Test54c_Clean_US_IPS_Audit_2026-11-16.json) were added at Ken Chee's request after successful independent static replay against the exact 2 MiB original ROM. The builder and verifier are also available in the patch directory. The owner-submitted PNGs, compressed game-native pictures, modified `.smc` builds and owner's Word screenshots are **not** included. Separate project recovery archives remain private.

Before publishing:

1. Review each file, especially screenshots or artwork you may add later, for rights and identifying information.
2. **Do not upload the private continuation ZIP**: it intentionally contains patched commercial game data for personal project recovery.
3. Audit exact-source IPS/BPS patch content and third-party distribution rights; publishing a patch does not confer rights to any underlying game material. Never host resulting `.smc` or `.sfc` images.
4. **Licences now in place:** [MIT](LICENSE) applies to original project Python code where we hold the rights; [CC BY 4.0](LICENSE-DOCUMENTATION.md) covers original research writing and copyrightable data compilations. Credit **Ken Chee**. Third-party code and assets keep their own rights and licences; consult the README's Licensing section.
5. Never represent these notes as an official release by Koei Tecmo, erich121, or Gilmok.
6. Keep the status labels: a binary-level pass does not imply complete campaign testing.

**Patch caveat:** Technical reproducibility and the absence of a full ROM do not establish comprehensive copyright clearance for binary differences. MIT and CC BY 4.0 attach only to original project code and documentation as specified, not to Koei's work. The project owner can decide whether to add further user-authored assets and data in later updates.

# RECEIPT — full skill library vacuum
**Date**: 2026-10-01
**Version**: v0.1.0
**Claim**: Liv HUB
**debug_outcome**: success
**UTC**: 2026-10-01T20:22Z

## Drive
- Parent: `1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0`
- Folder: `v0.1.0_2026-10-01_full-skill-library-vacuum`
- folder_id: `1ykPlHnmIxBF7inT5V-Thf39vA5e4ZXsQ`
- Link: https://drive.google.com/drive/folders/1ykPlHnmIxBF7inT5V-Thf39vA5e4ZXsQ

## Full tarball
- Name: `full_skill_library_v0.1.0_2026-10-01.tar.gz`
- file_id: `1fn7Gs3inl7i5VVVs5I5x2ZxIdb9UdO1y`
- Size: 265046861 bytes
- SHA256: `0278a1c7dbdad0dbf085460eb1710dede67ed874d0f6501537b22556fec3d717`
- Members: 5354
- Slugs: 37 (10 bundled + 27 custom)
- Link: https://drive.google.com/file/d/1fn7Gs3inl7i5VVVs5I5x2ZxIdb9UdO1y/view

## Other Drive file_ids
- MANIFEST_full: `1xH2kbe1hu5a6Y9z0zNS_J2-iXMwzSH3s`
- MANIFEST daily-core: `1GFO-P3RzmD4A3HXu0-uTPE6T1VGqVhUL` (1703 bytes, sha256 a0815e7e3f9766e655926a18199c5c76fd61e5e442904254a02669f7c22ea961)
- chaos-bratz-roster_daily-core: `19ItaWc2z9iC0JEJ4uNxW-gBlyphhnvt1` (517115, 7f22cd02db61895c12e12b40fb081ef1099d828e4a0933fcbe4c9afdcfd851a7)
- format-bible_daily-core: `1-uZ5qEG3DJVjqgl_oRmjX1n60srRUzOo` (24265, 5d04ba7444528d603befc909839c9af8d709f163eba33ef1b12e77c8d8cb002a)
- olivia-dev_daily-core: `1a0ztElYoT6MUQyYzseovKg8lJq82L4Am` (24905, 15627d7a38c02fc8fa04c85f8bcf356fccbd8d6b4ed44fffa82505c9eaedea7b)
- olivia-dev-alpha_daily-core: `1g1UZatLpYlQMeq4rxMZjEOPsVt5QVjJo` (77120, 03c4fdd868e3972d36ab93e331868a64a12a58bcbc382baa801d484311ec7da8)
- system-roadmap_daily-core: `1P60dV7oz7M3JXFQ17FvX_16qhurVgyrN` (296322, 41a64f41d1da7721711c456bf3d7c573f57b660dcc59538e02f5085c8f8eee2a)
- skill-orchestrator_daily-core: `18Ut2FSlcEX_3tC-0auMWfC1Do__pCCCa` (44333008, 361f4d8d0d343942b6ea89cd8550fe8db973de970f0cc77c4a0a0d8a156f24fb)

## Restore
```bash
mkdir -p /tmp/restore_skills
tar -xzf full_skill_library_v0.1.0_2026-10-01.tar.gz -C /tmp/restore_skills
```
Yields `server-skills/` and `bundled-skills/`.

## Notes
Recipe paths `/home/workdir/.grok/skills` and `/root/.grok/skills` were absent. Symlinked server-skills so package_skills.py and library_export.py could run. Full tar packed `/root/.grok/server-skills` plus `/usr/share/grok/bundled-skills`. GitHub holds text receipts only.

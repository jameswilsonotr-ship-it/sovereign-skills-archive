# Fork ledger

MIS-6 records the upstream ideas used by the harness without copying or
rewriting the live skill tree.

| Fork/reference | Upstream or local source | Use in this change |
| --- | --- | --- |
| RinDig `icm-architect` | [github.com/RinDig/icm-architect](https://github.com/RinDig/icm-architect) | Folder contracts and small, walkable surfaces |
| Interpretable-Context-Methodology | [github.com/RinDig/Interpretable-Context-Methodology](https://github.com/RinDig/Interpretable-Context-Methodology) | Provenance for the ICM workspace method |
| Thunderclap | Named fork/reference for the MIS-6 integration surface | Recorded as provenance only; no external bytes are vendored |

The harness is an offline test surface. It does not create a second archive
repository, unpack `CONV2_B`, or write live `skill_tree/**/SKILL.md` files.

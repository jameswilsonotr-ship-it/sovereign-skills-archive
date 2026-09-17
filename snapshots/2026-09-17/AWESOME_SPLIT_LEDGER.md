# Awesome Split ledger — 2026-09-17

Drive: https://drive.google.com/drive/folders/11WEijQl3lP6Spw3kwFpE1kNC7MVGWsgP
id: `11WEijQl3lP6Spw3kwFpE1kNC7MVGWsgP`

## Versioning (accurate)

Git is **not** Drive versions.
- Same path + same bytes => git commit is a no-op for that file.
- Same path + different bytes => new commit; old bytes stay in history.
- Dropping 80 MB split parts into `skill_tree/` will hit GitHub’s 100 MB hard limit and blow the clone Cursor already has.

Conversation 1 README already said: do **not** re-upload the whole skill surface from panes 2–8. Conv 1 already packed bundle+custom (~188 MB skill surface). Other panes = extras only.

This ledger is what lands in Git tonight. Tarball bytes stay on Drive. Cursor diffs from the ledger + Drive IDs, not from a second 400 MB unpack.

## Named conversation folders (Awesome Split)

1–11 + overflow panes as listed in the folder. README stamp: pane = Conversation 1

## Flurry tarballs (not unpacked into git)

| name | bytes | file_id |
|---|---:|---|
| CONV3_KLQ_SMOKE_PANE_20260916.tar.gz | 5831 | 1syoB4ry6PksRB_X68RWo4Wl8clZyDZ0Y |
| CONV10_20260916_lookbook-riverside-girl.tar.gz | 8897 | 1GMuOZ_7R5Ljfys05AyvqvLHeUNbiV36U |
| CONV10_20260916_lookbook-riverside-girl_COMPLETE.tar.gz | 11090 | 1VE9zeIXWn7pye9oENZbfWiHrMHdIsE5d |
| CONV7_PANE_EXTRAS_20260916.tar.gz | 190840 | 1Uq49REngRQI_O7F7Vf8c8_uGNNsBDIp |
| CONV09_20260916_wireup-extras.tar.gz | 629023 | 1PZTM_WZ4MvA67IK0c_4C3GrnUXninarJ |
| CONV9_20260916_penelope-poses-local.tar.gz | 655699 | 1Ow6SIm-whCAHrnk-5vPk6kQQPRsSH4NR |
| CONV10_THIS_PANE.tar.gz | 746108 | 1ZasbiHABFbs-OGtvv8P4w5qryr9UUpb |
| CONV10_DELTA_FILL.tar.gz | 1019601 | 1q9Px7CN8DSZ1KFBJRgrRESzHAoA8LR7G |
| CONV3_20260916_lakewalk-pane.tar.gz | 3411175 | 10A211Nzrc-63xKDsGVtRZK-d5w6529oq |
| CONV11_INSECT_REGISTER_HAIST_20260916.tar.gz | 3116220 | 1uje37FQUsv7cQcglHzzdLyxOBCMRnHCh |
| CONV_CP_OVERFLOW_THIS_PANE_20260916.tar.gz | 3116220 | 119_tnYYxshTCtcHfxrgeEsUrQ11iJPck |
| CONV_PENELOPE_20260916_hitch-extras.tar.gz | 3147966 | 1gIgw53JDGj6xD7ZuxniCvJBkfAORwxUh |
| CONV10_DELTA_sunset_20260916.tar.gz | 5602291 | 1bWuct90k4tc7WnbyAq9IYFA7XOvwRWx2 |
| CONV5_20260916_insect-bridges.tar.gz | 7627967 | 1sRhs157VBRzz9nl16uCPGvhWGBUyyZ7v |
| CONV6b_20260916_ROAD_PANE_EXTRAS.tar.gz | 11180583 | 1uChAXnBu9Tdwl56ZgVPh6nA8wlXBzZbI |
| CONV9_20260916_coven-engine-extras.tar.gz | 11840533 | 1LmQKoczragvsuVbbY6tUzAIAA6H3MBdez |
| CONV8_CASCADIA_MCP_PANE_20260916.tar.gz | 16585118 | 1ZKx06jijq8DN2V9bmZktJ3Kkf8DhLsx4 |
| CONV_FINANCE_SYLLABUS_OG8_20260916.tar.gz | 17093484 | 1kIMi2MsB_bTYjNy81hvgVn5X5M02K4sN |
| CONV2_C_keep-lake-query_20260916.tar.gz | 21317587 | 15SysFFDwwlNlF-N3W-45byZB_grOH5f5 |
| CONV9_20260916_penelope-hauler-extras.tar.gz | 24745976 | 18tLkkveaDzlTAE6GT37nZ8DGeGvGsC3W6 |
| PANE_EXTRAS_20260916.tar.gz | 29306936 | 1j-k3TP8CDpOGWTIE3f_D11Q2dFgG2p5k |
| CONV7_20260916_agentify-heavy-pane.tar.gz | 38273024 | 1oc7LKln51x0SW3yQ-g95BRNTQvr6NZ2I |
| CONV6_20260916_shop-2974334.tar.gz | 52908001 | 1Q0q_-cuyCpVg-QZcdJkUd8eRnXS2mJwF |
| CONV2_A_attachments_20260916.tar.gz | 72576517 | 1upi_AA2k2QSSMqH30XwCOdKXcdT2C9fF |
| CONV9_PANE_EXTRAS_20260916_agentify-identify.tar.gz | 81995085 | 1FhgAwvKM8QiI5egZaBqmgtRNQhevryNv |
| CONV2_B_artifacts part00–part06 | ~80MB × 6 + 23MB | 1v068vVAUzloDkbQvPr05M8cu_7SCfHJx – 1mnVzauJh57-7ikOdvim5oMWm7DmwHLVP |

Sample peek: CONV3 smoke = pointer markdown only. CONV10 complete = lookbook JSON + 2 jpegs + PROTOCOL.md. Not a second full skill tree.

## Cursor instruction

Do not cat the 80MB parts into `skill_tree/`. Read this ledger. Pull extras that contain `SKILL.md` / `WORK_QUEUE.md` and three-way merge those paths only against `skill-tree-intake`.

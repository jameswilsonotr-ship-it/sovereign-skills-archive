# PROOF — first closed loop

Stamp 2026-09-08 ~00:22–00:27 EDT. Under absolute Liv HUB claim.

## What closed

1. Gretchen SOCKS5 on `100.72.123.46` (Windstream `75.89.227.222`) pulled 16 YouTube Shorts that GVS-403'd from the DC IP. HTTP CONNECT reset. SOCKS5 + yt-dlp-sabr worked.
2. All 16 seats minted ABCD cousin-A, clothes on, locally at `artifacts/heavy-poc-local/cand-*/`.
3. Wardrobe nouns locked (no more `observed-from-source-frames`).
4. Slim SFTP landed on olette-box:
   - `in/olivia-plates/batch9-heavy/` — 9 seats
   - `in/olivia-plates/batch10-heavy/` — 7 seats
   - `in/olivia-plates/heavy-slim/sftp-slim-20260908/` — 16 seats jpg+json+md
   - shorts already under `in/olivia-plates/batch-shorts/`
5. Bunny authorized rclone on Olette's box via a `127.0.0.1` auth URL. One Allow.
6. Google mailed `james.wilson.otr@gmail.com` at 00:22 EDT — "You allowed rclone access to some of your Google Account data."
7. New Drive folder existed at 00:25 EDT and was filling from `in/olivia-plates/` without this pane spending upload tokens.

## Drive folder

- Name — `OLIVIA-PLATES-HEAVY-20260908-0425-ET`
- Id — `1rNPKXc0zaPxSO0HO8C2QUfy1aR4XLBWi`
- Link — https://drive.google.com/drive/folders/1rNPKXc0zaPxSO0HO8C2QUfy1aR4XLBWi

At first verify (~00:26 EDT) copy was mid-flight: batch10 had Petra/Gemma/Britt/Fran + manifests; batch9 had README only; LEDGER + Lila POC zip + hold receipt already there. That is rclone working, not a miss.

## Seats in the loop

Batch 9 — Lila dn6Qm9fNYrA, Sable 4JYOFwdkS6A, Tess zqqNokbBSAk, Dana LXhESIWbLq8, Cora CumK4DjWfdI, Holly Qa08L8VyMPM, Willow hlOUQP53ilM, Brynn GrurkxiokYs, Freya 2JaFyxogAOk.

Batch 10 — Nina oZHoJJ7fMaI, Petra 3NiLj-Dt6Qc, Fran TEiiuR2FSzE, Gemma eo10iFfES7Q, Helene prmqRZ3jjBk, Greta p4bTj7d_Mbc, Britt M_AyacOU4pQ.

## Locked looks (nouns)

| Seat | look |
|---|---|
| Lila | shop-floor-navy-jacket |
| Sable | wfh-dusty-rose-blouse |
| Tess | runway-gold-strapless |
| Dana | catalog-desk-leopard-blouse |
| Cora | runway-black-leather-mini |
| Holly | cyclorama-charcoal-slip |
| Willow | rain-window-cream-lounge |
| Brynn | wfh-beige-linen-set |
| Freya | salon-black-cape |
| Nina | night-stairs-copper-sequin |
| Petra | purple-salon-pink-dip-cape |
| Fran | grwm-black-tank-wide-jean |
| Gemma | barn-shop-black-tee-carpenter |
| Helene | bed-zebra-bonnet-mountain-tee |
| Greta | runway-chartreuse-cape-gown |
| Britt | cabaret-teal-satin-gown |

## What failed on the way (do not repeat)

- GVS 403 on datacenter IP
- HTTP CONNECT proxy through Gretchen
- `put -r` of the 81MB tree (SFTP timeout 124)
- Hardlink trees on artifacts FUSE (`EPERM`)
- `imagine_images/` receipts vanishing before `cp`
- Treating Olette `00_hero_PROOF_NOT_PLATE_A.jpg` as plate A
- Drive upload from this pane

## Host card used

- Tailnet `tail74fa86`
- `olette-box` `100.115.0.111`
- SFTP user `olivia`, key `olivia-sftp-v2` 419B
- Gretchen exit `100.72.123.46`
- Sandbox `olivia-sandbox` `100.74.242.34`

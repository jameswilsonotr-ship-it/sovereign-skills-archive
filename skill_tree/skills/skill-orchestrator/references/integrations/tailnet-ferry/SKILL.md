---
name: tailnet-ferry
parent: skill-orchestrator
surface: integrations
stamp: 2026-09-07 23:08 EDT
description: >
  Deterministic muscle memory for Olivia-sandbox on Bunny tailnet tail74fa86.
  Join via ephemeral auth key, SFTP as user olivia (not bunny) to olette-box,
  Taildrop vs SFTP vs Drive ferry, DERP vs direct. Never store tskey-auth or
  private keys in this tree.
triggers:
  - tailnet ferry
  - tailscale sftp
  - taildrop
  - olette-box
  - olivia-sandbox
---

# Tailnet ferry (under skill-orchestrator)

Two doors. Do not mix them.

| door | what it proves | what it is not |
|---|---|---|
| **Tailscale auth key** `tskey-auth-…` | this box may *join the tailnet* | not SSH |
| **SSH key** `olivia-sftp` | user `olivia` may SFTP to olette-box | not the tailnet join |

## Host card (SSoT)

- Tailnet: `tail74fa86`
- Host: `olette-box.tail74fa86.ts.net` / `100.115.0.111`
- Sandbox hostname once joined: `olivia-sandbox`
- SFTP user: **`olivia`** (Olette 2026-09-07 — not `bunny`)
- Port 22 on Tailscale IP only
- cwd after login: `/workspace/sync`
- out: `/workspace/sync/out/`
- in: `/workspace/sync/in/olivia-plates/`
- Gretchen (`100.72.123.46`) = phone exit node (Cleveland Windstream when approved)

## Join recipe (userspace — this sandbox has no lasting TUN)

`artifacts/` is FUSE **noexec**. Binaries live in `/tmp` after copy.

```
cp artifacts/tailscale-bin/tailscale artifacts/tailscale-bin/tailscaled /tmp/
chmod +x /tmp/tailscale /tmp/tailscaled
/tmp/tailscaled --statedir=artifacts/tailscale-state \
  --socket=/tmp/tailscaled.sock --tun=userspace-networking &
/tmp/tailscale --socket=/tmp/tailscaled.sock up \
  --auth-key="$TS_AUTHKEY" --hostname=olivia-sandbox --accept-dns=false
```

Auth key comes from console Keys → Generate. Paste once. Never write it into this skill.
`/tmp` evaporates between watches. Copy binaries again.

## SFTP recipe (userspace = must ProxyCommand)

Kernel cannot route `100.x`. Punch through `tailscale nc`.

Key file from Gmail attachment on `OLETTE-20260907-TS-AUTH-AND-SFTP-RESP-001`.
Copy off the FUSE mount to `~/.ssh/olivia-sftp` and `chmod 600` or ssh refuses.

```
sftp -i ~/.ssh/olivia-sftp -o IdentitiesOnly=yes \
  -o ProxyCommand="/tmp/tailscale --socket=/tmp/tailscaled.sock nc %h %p" \
  olivia@100.115.0.111
```

## Three ferries

1. **SFTP** — canonical for plate zips. `get out/…` `put … in/olivia-plates/`
2. **Taildrop** — `tailscale file cp FILE olette-box:` peer-to-peer push. No shell. Good for one-off blobs. Not a login.
3. **Drive / Cilia** — fallback when this pane is off the tailnet. The cheap Drive door after a good SFTP is Olette rclone (`../heavy-olette-drive-pipe/`). Do not `google_drive_upload_artifact` a 191MB tree from Heavy.

## DERP

If `ping` says `via DERP(tor)` the packets bounce a Tailscale relay (here: Toronto). Works. Slower. `direct connection not established` is normal until NAT punches. Exit-node traffic (Gretchen) is a different path — that is residential IPv4 for GVS, not the SFTP path.

## Never

- Store `tskey-auth-` or private keys in git / skill / WQ
- Bind bgutil or anything to `0.0.0.0`
- Use user `bunny` for this pane
- Treat a Keys **ID** (`k2tgf…CNTRL`) as the secret
- OCR a key from a screenshot

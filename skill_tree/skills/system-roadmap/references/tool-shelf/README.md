# Tool shelf — system-roadmap

Stamp 2026-09-07 23:34 EDT. Park binaries here so `/tmp` wipe does not force a re-download.

`artifacts/` FUSE is **noexec**. Always copy to `/tmp` and `chmod +x` before run.

## Layout
- `bin/tailscale` `bin/tailscaled` — 1.102.3 static amd64
- `bin/yt-dlp-sabr` — bashonly sabr 2026.08.19
- `scripts/yt_short_ingest.py` — copy from image-pipeline
- `scripts/hydrate.sh` — copy bins to /tmp

## Hydrate
```
bash references/tool-shelf/scripts/hydrate.sh
```

## Tailnet
State lives in `artifacts/tailscale-state` (Drive-backed). Next pane (including Heavy) should reuse that statedir instead of burning a new auth key.
SFTP user `olivia`, key `artifacts/secrets/olivia-sftp-v2` copied to `~/.ssh` mode 600.
ProxyCommand: `tailscale nc` (userspace, no TUN).
Exit node: Gretchen `100.72.123.46` when YouTube GVS 403s from DC IP.
SOCKS5 (not HTTP CONNECT) through Gretchen is the proved YouTube door. Full plate→SFTP→rclone-Drive loop lives in `skill-orchestrator/references/integrations/heavy-olette-drive-pipe/`.

## Do not
Store tskey-auth or private keys in this shelf.
Bind POT server to 0.0.0.0.

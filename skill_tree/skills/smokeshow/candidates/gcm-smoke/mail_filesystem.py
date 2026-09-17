#!/usr/bin/env python3
"""GCM-WQ-013 render Cilia body as a directory. Does not send."""
from __future__ import annotations

import argparse
from pathlib import Path

from gcm_lib import stamps


def render(
    msg_id: str,
    verb: str,
    slug: str,
    toc_lines: list[str],
    omission_lines: list[str],
    drive: dict,
    req: str,
    turns_this: int = 1,
    turns_left: int = 0,
    delta: str = "first-run",
    blocked_on: str = "",
) -> str:
    s = stamps()
    toc = "\n".join(f"      {line}" for line in toc_lines) or "      (empty)"
    om = "\n".join(f"      {line}" for line in omission_lines) or "      (none)"
    return f"""/{msg_id}/
  00_HEADER
    stamp_utc: {s['stamp_utc']}
    stamp_ny: {s['stamp_ny']}
    msg_id: {msg_id}
    verb: {verb}
    slug: {slug}
    skill: {s['skill']}
    claim: {s['claim']}
    time_is_not_the_budget: true
    turns_this_run: {turns_this}
    turns_remaining_estimate: {turns_left}
    blocked_on: {blocked_on or 'none'}
  01_TOC
{toc}
  02_OMISSIONS
{om}
  03_TURNS
    turns_this_run: {turns_this}
    turns_remaining_estimate: {turns_left}
    time_is_not_the_budget: true
  04_DRIVE
    folder_id: {drive.get('folder_id', '')}
    tar_id: {drive.get('tar_id', '')}
    folder_url: {drive.get('folder_url', '')}
  05_REQ
    {req}
  06_DELTA
    {delta}
"""


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--msg-id", required=True)
    p.add_argument("--verb", default="smoke")
    p.add_argument("--slug", default="smoke")
    p.add_argument("--out", type=Path)
    args = p.parse_args(argv)
    body = render(
        args.msg_id,
        args.verb,
        args.slug,
        toc_lines=["fixtures planted"],
        omission_lines=["live sunset not run"],
        drive={},
        req="ACK smoke exit code only",
    )
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(body, encoding="utf-8")
    print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

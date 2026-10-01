#!/usr/bin/env python3
"""community_post_fetch.py — three doors around the youtube.com/post consent wall.

  python3 community_post_fetch.py Ugkx... [--dest DIR] [--backend all|innertube|invidious|ytdlp]

1. innertube  — resolveurl → FEpost_detail + params → youtubei/v1/browse
2. invidious  — GET /api/v1/post/<id>  (attachments often thin; still tried)
3. ytdlp      — /tmp/yt-dlp + community plugin if present

Does not load youtube.com/post in a browser.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen

POST_RE = re.compile(r"(Ugkx[A-Za-z0-9_-]+)")
INVIDIOUS = ["https://inv.nadeko.net", "https://yewtu.be", "https://invidious.nerdvpn.de"]
UA = "Mozilla/5.0 (Agentify community_post_fetch/0.2)"
YTDLP_BINS = ["/tmp/yt-dlp", "yt-dlp"]
PLUGIN_DIR = Path("/home/workdir/artifacts/yt-dlp-plugins/community")


def post_id(s: str) -> str:
    m = POST_RE.search(s)
    if not m:
        raise SystemExit(f"no Ugkx id in {s}")
    return m.group(1)


def _req(url, data=None, headers=None, timeout=20):
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    return urlopen(Request(url, data=data, headers=h), timeout=timeout)


def _json(url, data=None, headers=None):
    try:
        raw = _req(url, data=data, headers=headers).read()
        if raw[:1] not in (b"{", b"["):
            return {"_error": "not-json", "_url": url}
        return json.loads(raw.decode("utf-8", "replace"))
    except Exception as e:
        return {"_error": str(e), "_url": url}


def walk_images(obj, out=None):
    if out is None:
        out = []
    if isinstance(obj, dict):
        for v in obj.values():
            if isinstance(v, str) and v.startswith("http") and any(x in v for x in ("ytimg", "ggpht", "googleusercontent")):
                out.append(v)
            else:
                walk_images(v, out)
    elif isinstance(obj, list):
        for i in obj:
            walk_images(i, out)
    return out


def uniq_bases(urls):
    seen, out = set(), []
    for u in urls:
        b = u.split("=")[0]
        if b not in seen:
            seen.add(b)
            out.append(u)
    return out


def prefer_post_stills(urls):
    fcrop = [u for u in urls if "fcrop" in u or "ytimg.com/vi" in u]
    return uniq_bases(fcrop or urls)


def hi_res(u: str) -> str:
    if "=" in u and "ggpht" in u:
        return u.split("=")[0] + "=s2048"
    return u


def youtube_client():
    html = _req("https://www.youtube.com/").read().decode("utf-8", "replace")
    key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html)
    ver = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', html)
    return {
        "key": key.group(1) if key else "",
        "ver": ver.group(1) if ver else "2.20260904.01.00",
    }


def resolve_post(pid: str) -> dict:
    for root in INVIDIOUS:
        j = _json(f"{root}/api/v1/resolveurl?url=https://www.youtube.com/post/{pid}")
        if j and j.get("browseId"):
            j["_instance"] = root
            return j
    return {}


def backend_innertube(pid: str) -> dict:
    nxt = resolve_post(pid)
    client = youtube_client()
    if not client["key"]:
        return {"backend": "innertube", "ok": False, "images": [], "error": "no innertube key"}
    body = {
        "context": {"client": {"clientName": "WEB", "clientVersion": client["ver"], "hl": "en", "gl": "US"}},
        "browseId": nxt.get("browseId") or "FEpost_detail",
    }
    if nxt.get("params"):
        body["params"] = nxt["params"]
    raw = _json(
        f"https://www.youtube.com/youtubei/v1/browse?key={client['key']}&prettyPrint=false",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-YouTube-Client-Name": "1", "X-YouTube-Client-Version": client["ver"]},
    )
    if raw.get("_error"):
        return {"backend": "innertube", "ok": False, "images": [], "error": raw["_error"], "resolve": {k: nxt.get(k) for k in ("browseId", "params", "ucid")}}
    imgs = prefer_post_stills(walk_images(raw))
    return {
        "backend": "innertube",
        "ok": bool(imgs),
        "images": imgs[:20],
        "resolve": {k: nxt.get(k) for k in ("browseId", "ucid", "_instance")},
        "n_raw_urls": len(walk_images(raw)),
    }


def backend_invidious(pid: str) -> dict:
    for root in INVIDIOUS:
        raw = _json(f"{root}/api/v1/post/{pid}")
        if raw.get("_error") or raw.get("_error") == "not-json":
            continue
        imgs = prefer_post_stills(walk_images(raw))
        if raw.get("authorId") or raw.get("author") or imgs:
            return {
                "backend": "invidious",
                "ok": bool(imgs),
                "instance": root,
                "images": imgs[:20],
                "authorId": raw.get("authorId") or raw.get("author"),
                "keys": list(raw.keys())[:12],
            }
    return {"backend": "invidious", "ok": False, "images": []}


def backend_ytdlp(pid: str, cookies: str | None) -> dict:
    url = f"https://www.youtube.com/post/{pid}"
    extra = []
    if PLUGIN_DIR.exists():
        extra += ["--plugin-dirs", str(PLUGIN_DIR)]
    if cookies:
        extra += ["--cookies", cookies]
    last = "no-bin"
    for b in YTDLP_BINS:
        try:
            p = subprocess.run(
                [b, *extra, "--dump-json", "--skip-download", "--no-warnings", url],
                capture_output=True, text=True, timeout=45,
            )
            if p.returncode == 0 and p.stdout.strip().startswith("{"):
                rec = json.loads(p.stdout.splitlines()[0])
                thumbs = [t.get("url") for t in (rec.get("thumbnails") or []) if t.get("url")]
                return {"backend": "ytdlp", "ok": bool(thumbs), "images": thumbs[:20], "extractor": rec.get("extractor")}
            last = (p.stderr or p.stdout or "")[-300:]
        except FileNotFoundError:
            last = f"missing {b}"
        except Exception as e:
            last = str(e)
    return {"backend": "ytdlp", "ok": False, "images": [], "error": last}


def download_images(urls, dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    saved = []
    for i, u in enumerate(urls, 1):
        u2 = hi_res(u)
        out = dest / f"post_{i:02d}.jpg"
        try:
            out.write_bytes(_req(u2, timeout=20).read())
            saved.append(str(out))
        except Exception:
            try:
                out.write_bytes(_req(u, timeout=20).read())
                saved.append(str(out))
            except Exception:
                continue
    return saved


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url_or_id")
    ap.add_argument("--dest", default="")
    ap.add_argument("--backend", default="all", choices=["all", "innertube", "invidious", "ytdlp"])
    ap.add_argument("--cookies", default="")
    args = ap.parse_args()
    pid = post_id(args.url_or_id)
    dest = Path(args.dest) if args.dest else Path("/home/workdir/artifacts/inbound") / f"yt-post-{pid}"
    dest.mkdir(parents=True, exist_ok=True)
    report = {"id": pid, "dest": str(dest), "backends": []}
    order = ["innertube", "invidious", "ytdlp"] if args.backend == "all" else [args.backend]
    winner = None
    for name in order:
        if name == "innertube":
            r = backend_innertube(pid)
        elif name == "invidious":
            r = backend_invidious(pid)
        else:
            r = backend_ytdlp(pid, args.cookies or None)
        report["backends"].append(r)
        if r.get("ok") and r.get("images") and winner is None:
            winner = r
    report["winner"] = winner["backend"] if winner else None
    if winner:
        report["saved"] = download_images(winner["images"], dest / "stills")
    (dest / "FETCH.json").write_text(json.dumps(report, indent=2)[:200000], encoding="utf-8")
    slim = {"id": pid, "winner": report["winner"], "saved": report.get("saved", []), "ok": [{b["backend"]: b.get("ok")} for b in report["backends"]]}
    print(json.dumps(slim, indent=2))
    return 0 if winner else 2


if __name__ == "__main__":
    raise SystemExit(main())

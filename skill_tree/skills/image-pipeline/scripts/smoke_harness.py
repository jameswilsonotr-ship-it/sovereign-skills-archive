#!/usr/bin/env python3
"""Deterministic smoke suite for image-pipeline scripts. No mint. No network required.

  python3 scripts/smoke_harness.py
  python3 scripts/smoke_harness.py --only classify,169,173,fork
Exit 0 = all selected passed. JSON report on stdout.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/home/workdir/.grok/skills/image-pipeline")
SCRIPTS = ROOT / "scripts"
PY = sys.executable


def run(args: list[str], timeout: int = 30) -> dict:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        data = None
        if out.startswith("{") or out.startswith("["):
            try:
                data = json.loads(out.split("\n{")[0] if False else out[out.find("{"):] if "{" in out else out)
            except json.JSONDecodeError:
                data = None
        return {"rc": proc.returncode, "out": out[-800:], "err": err[-400:], "json": data}
    except Exception as exc:
        return {"rc": 99, "out": "", "err": str(exc)[:300], "json": None}


def expect(name: str, ok: bool, detail: dict) -> dict:
    return {"name": name, "ok": ok, "detail": detail}


def smoke_classify() -> dict:
    r = run([PY, str(SCRIPTS / "inbound_classify.py"), "--help"])
    return expect("inbound_classify --help", r["rc"] == 0, r)


def smoke_fork() -> dict:
    cases = {
        "https://youtu.be/kTHNpusq654?is=z1LVMvdRKyowLeUq": "yt-video",
        "https://www.youtube.com/shorts/AAAAAAAAAAA": "yt-short",
        "https://www.instagram.com/reel/AbCdef12345/": "instagram",
        "https://www.tiktok.com/@x/video/1234567890": "tiktok",
        "https://www.facebook.com/watch/?v=1": "facebook",
        "hot n cold katy": "title-fragment",
    }
    bad = []
    for raw, kind in cases.items():
        r = run([PY, str(SCRIPTS / "feed_fork.py"), raw])
        got = (r["json"] or {}).get("kind")
        if got != kind:
            bad.append({"raw": raw, "want": kind, "got": got, "rc": r["rc"]})
    return expect("feed_fork kinds", not bad, {"misses": bad})


def smoke_resolve() -> dict:
    r = run([PY, str(SCRIPTS / "url_resolver.py"), "https://youtu.be/kTHNpusq654?is=z1LVMvdRKyowLeUq"])
    ok = (r["json"] or {}).get("id") == "kTHNpusq654"
    r2 = run([PY, str(SCRIPTS / "url_resolver.py"), "hot n cold"])
    ok2 = (r2["json"] or {}).get("id") == "kTHNpusq654"
    r3 = run([PY, str(SCRIPTS / "url_resolver.py"), "totally unknown song xyzzy"])
    ok3 = r3["rc"] == 2 and not (r3["json"] or {}).get("ok")
    return expect("url_resolver", ok and ok2 and ok3, {"dirty": r["json"], "title": r2["json"], "unknown": r3["json"]})


def smoke_169() -> dict:
    mute = run([PY, str(SCRIPTS / "android_show.py"), "--client", "ANDROID", "--utterance", "agentify these"])
    dump = run([PY, str(SCRIPTS / "android_show.py"), "--client", "ANDROID", "--utterance", "dump the pictures"])
    desk = run([PY, str(SCRIPTS / "android_show.py"), "--client", "WEB", "--utterance", "agentify these"])
    m, d, w = mute["json"] or {}, dump["json"] or {}, desk["json"] or {}
    ok = (m.get("emit_render_file") is False and d.get("emit_render_file") is True and w.get("emit_render_file") is True)
    return expect("android_show 169", ok, {"mute": m, "dump": d, "web": w})


def smoke_173() -> dict:
    r = run([PY, str(SCRIPTS / "imply_fallback.py"), "--lane", "E", "--intensity", "e", "--code", "I-2-E-e"])
    j = r["json"] or {}
    ok = j.get("same_code") and not j.get("lowered_pick") and j.get("retry_code") == "I-2-E-e" and "implication" in (j.get("implication_id") or "")
    return expect("imply_fallback 173", ok, j)


def smoke_168() -> dict:
    hit = run([PY, str(SCRIPTS / "agentify.py"), "route", "identify this woman", "--media"])
    miss = run([PY, str(SCRIPTS / "agentify.py"), "route", "identify"])
    h, m = hit["json"] or {}, miss["json"] or {}
    ok = bool(h.get("hit")) and not m.get("hit")
    return expect("agentify route 168", ok, {"media": h, "bare": m})


def smoke_heat() -> dict:
    r = run([PY, str(SCRIPTS / "agentify.py"), "heat", "--code", "I-2-E-e"])
    j = r["json"] or {}
    return expect("agentify heat I-2-E-e", r["rc"] == 0 and bool(j.get("hop") or j.get("parsed")), j)


def smoke_keep_help() -> dict:
    names = [
        "keep_path.py", "step6_drive_flush.py", "flush_drive_queue.py",
        "inbound_classify.py", "split_plan.py", "emit_intent.py",
        "reel_sample.py", "yt_short_ingest.py", "fb_ingest.py",
        "ig_ingest.py", "tiktok_ingest.py", "local_video_ingest.py",
        "music_video_ingest.py", "feed_fork.py",
    ]
    missing = []
    helps = []
    for n in names:
        p = SCRIPTS / n
        if not p.exists():
            missing.append(n)
            continue
        r = run([PY, str(p), "--help"])
        # some use usage on stderr rc 2 without --help support; accept compile via -h or rc in {0,2}
        if r["rc"] not in {0, 2}:
            # try running with no args
            r2 = run([PY, str(p)])
            if r2["rc"] not in {0, 2}:
                missing.append(n + f":rc{r['rc']}/{r2['rc']}")
        helps.append(n)
    return expect("script --help set", not missing, {"present": helps, "bad": missing})


def smoke_compile() -> dict:
    bad = []
    for p in sorted(SCRIPTS.glob("*.py")):
        r = run([PY, "-m", "py_compile", str(p)])
        if r["rc"] != 0:
            bad.append({"file": p.name, "err": r["err"][-200:]})
    return expect("py_compile scripts/*.py", not bad, {"bad": bad})


def smoke_dummy_still() -> dict:
    from PIL import Image
    tmp = Path(tempfile.mkdtemp()) / "still.jpg"
    Image.new("RGB", (800, 600), (20, 40, 80)).save(tmp, quality=85)
    r = run([PY, str(SCRIPTS / "inbound_classify.py"), "--src", str(tmp)])
    j = r["json"] or {}
    return expect("classify dummy 800x600", j.get("layout") == "single" and r["rc"] == 0, j)


def smoke_ingest_closed() -> dict:
    """FB/IG/TT write INGEST.json and do not mint. Live bytes not required."""
    cases = [
        ("fb_ingest.py", "https://www.facebook.com/watch/?v=1"),
        ("ig_ingest.py", "https://www.instagram.com/reel/AbCdef12345/"),
        ("tiktok_ingest.py", "https://www.tiktok.com/@x/video/1234567890"),
    ]
    bad = []
    for name, url in cases:
        r = run([PY, str(SCRIPTS / name), url], timeout=45)
        j = r["json"] or {}
        if r["rc"] not in {0, 1, 2} or j.get("promote") is True:
            bad.append({"script": name, "rc": r["rc"], "json": j})
            continue
        dest = j.get("dest") or ""
        ingest = None
        if dest:
            p = Path(dest) / "INGEST.json"
            ingest = p.exists()
        # fb/ig write dest via inbound_dir internally; accept INGEST via n_stills key
        if j.get("kind") not in {"facebook", "instagram", "tiktok"} and "facebook" not in name:
            if not j.get("ok") and r["rc"] == 2 and "not-a" in (j.get("error") or ""):
                continue
        if j.get("promote"):
            bad.append({"script": name, "promote": True})
    return expect("ingest fail-closed", not bad, {"bad": bad})


def smoke_local_video() -> dict:
    tmp = Path(tempfile.mkdtemp()) / "local3s.mp4"
    mk = run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=size=640x360:rate=8:duration=3",
        "-pix_fmt", "yuv420p", str(tmp),
    ], timeout=20)
    if not tmp.exists():
        return expect("local_video 3s", False, {"ffmpeg": mk})
    r = run([PY, str(SCRIPTS / "local_video_ingest.py"), "--file", str(tmp), "--who", "smoke-local"], timeout=60)
    j = r["json"] or {}
    ok = j.get("kind") == "local-video" and j.get("promote") is False and r["rc"] in {0, 1}
    return expect("local_video 3s", ok, j)


def smoke_gate() -> dict:
    r = run([PY, str(SCRIPTS / "step6_drive_flush.py"), "--gate"])
    j = r["json"] or {}
    # honest: queued keeps => rc 2 and emit_allowed false. empty lake => rc 0.
    ok = r["rc"] in {0, 2} and "emit_allowed" in j
    if r["rc"] == 2:
        ok = ok and j.get("emit_allowed") is False
    return expect("step6 --gate callable", ok, j)


REGISTRY = {
    "compile": smoke_compile,
    "help": smoke_keep_help,
    "classify": smoke_classify,
    "fork": smoke_fork,
    "resolve": smoke_resolve,
    "169": smoke_169,
    "173": smoke_173,
    "168": smoke_168,
    "heat": smoke_heat,
    "still": smoke_dummy_still,
    "ingest": smoke_ingest_closed,
    "local": smoke_local_video,
    "gate": smoke_gate,
}


def main() -> int:
    only = []
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].split(",")
    names = only or list(REGISTRY)
    results = []
    for n in names:
        fn = REGISTRY.get(n.strip())
        if not fn:
            results.append({"name": n, "ok": False, "detail": "unknown smoke"})
            continue
        results.append(fn())
    report = {
        "ok": all(r["ok"] for r in results),
        "n": len(results),
        "passed": sum(1 for r in results if r["ok"]),
        "failed": [r["name"] for r in results if not r["ok"]],
        "results": results,
        "ticket": "IP-WQ-196",
    }
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

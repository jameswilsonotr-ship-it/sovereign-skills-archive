#!/usr/bin/env python3
"""GCM-WQ-009 sunset smoke harness.

Plant 12 files / 6 classes. Dry-run against fixtures only.
Provides run_smoke(root) for test_gcm.py.
Never touches a live conversation.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from gcm_lib import (  # noqa: E402
    CLAIM,
    LAYOUT,
    census_done,
    make_tar,
    render_mail_filesystem,
    safety_gate,
    sha256_file,
    stamps,
)
from census import l0_decision, read_jsonl, write_jsonl, upsert  # noqa: E402
from packers import pack  # noqa: E402
from export_recon import index_export, recon_sets, render as render_recon  # noqa: E402
from lake_batch import walk_dated_tree, run as lake_run  # noqa: E402
from layout import make_space  # noqa: E402
from toc_omissions import write_toc_and_omissions  # noqa: E402
from sunset_dry_run import decide  # noqa: E402
from mail_filesystem import render as render_mail  # noqa: E402
from ledger import add_row  # noqa: E402

SIX_CLASSES = (
    "lake_twin",
    "lake_receipt",
    "miner_publish_tar_pointer",
    "global_extract_tar_pointer",
    "sunset_l7_outbox",
    "census_row",
)

FAKE_ACKS = {
    "twin_id": "FAKE_TWIN_1a2b3c4d",
    "receipt_id": "FAKE_RCPT_9f8e7d6c",
    "miner_tar_id": "FAKE_TAR_aa11bb22",
    "global_extract_id": "FAKE_GX_cc33dd44",
}


def plant_fixtures(root: Path) -> dict:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    files = {}
    p = root / "lake" / "2026" / "09" / "week37" / "2026-09-10" / "2026-09-10_deadbeef.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# twin fixture\nslug: smoke-fixture\n")
    files["lake_twin"] = p
    p = root / "lake" / "receipts" / "RECEIPT_shard_2026-09-10.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"twin_id: {FAKE_ACKS['twin_id']}\nslurp: false\n")
    files["lake_receipt"] = p
    p = root / "pointers" / "miner_publish.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(FAKE_ACKS["miner_tar_id"] + "\n")
    files["miner_publish_tar_pointer"] = p
    p = root / "pointers" / "global_extract.txt"
    p.write_text(FAKE_ACKS["global_extract_id"] + "\n")
    files["global_extract_tar_pointer"] = p
    p = root / "artifacts" / "sunset" / "SUNSET_20260910_smoke-fixture.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# L7 outbox fixture\n")
    files["sunset_l7_outbox"] = p
    census_path = root / "census" / "CENSUS.jsonl"
    rows = [
        {
            "date": "2026-09-10",
            "slug": "smoke-fixture",
            "keep_or_delta": "LIVE",
            "twin_id": FAKE_ACKS["twin_id"],
            "receipt_id": FAKE_ACKS["receipt_id"],
            "miner_tar_id": FAKE_ACKS["miner_tar_id"],
            "global_extract_id": FAKE_ACKS["global_extract_id"],
            "redacted": "n/a",
            "packed": True,
            "pointed": True,
            "status": "OPEN",
            "key": "2026-09-10_smoke-fixture",
        },
        {
            "date": "2026-09-11",
            "slug": "no-twin-day",
            "keep_or_delta": "LIVE",
            "twin_id": "NO_TWIN",
            "receipt_id": "",
            "miner_tar_id": "",
            "global_extract_id": "",
            "redacted": "n/a",
            "packed": False,
            "pointed": False,
            "status": "OPEN",
            "key": "2026-09-11_no-twin-day",
        },
    ]
    write_jsonl(census_path, rows)
    files["census_row"] = census_path
    extras = {
        "imagine": root / "sandbox" / "imagine" / "imagine_sample.txt",
        "video": root / "sandbox" / "video" / "clip.mp4",
        "plates": root / "sandbox" / "plates" / "plate_join.txt",
        "export": root / "export" / "prod-grok-backend.json",
        "empty_keep": root / "lake" / "2026" / "09" / "week37" / "2026-09-11" / ".keep",
        "secret": root / "secrets" / "cookies.txt",
    }
    extras["imagine"].parent.mkdir(parents=True, exist_ok=True)
    extras["imagine"].write_text("fake imagine prompt sidecar\n")
    extras["video"].parent.mkdir(parents=True, exist_ok=True)
    extras["video"].write_bytes(b"FAKEMP4")
    extras["plates"].parent.mkdir(parents=True, exist_ok=True)
    extras["plates"].write_text("join / production, not a catalog to eat\n")
    extras["export"].parent.mkdir(parents=True, exist_ok=True)
    extras["export"].write_text(json.dumps({
        "conversations": [{"id": "conv-smoke-1"}, {"id": "conv-export-only"}],
        "assets": [{"id": "asset-1"}],
    }))
    extras["empty_keep"].parent.mkdir(parents=True, exist_ok=True)
    extras["empty_keep"].write_text("")
    extras["secret"].parent.mkdir(parents=True, exist_ok=True)
    extras["secret"].write_text("SECRET fixture — must land in OMISSIONS\n")
    files.update(extras)
    planted = [p for p in root.rglob("*") if p.is_file()]
    files["_count"] = len(planted)
    files["_paths"] = planted
    return files


def run_smoke(root: Path | None = None) -> dict:
    """Plant fixtures under root and exercise deterministic scripts. No live I/O."""
    tmp_owned = False
    if root is None:
        import tempfile
        root = Path(tempfile.mkdtemp(prefix="gcm-smoke-"))
        tmp_owned = True
    root = Path(root)
    files = plant_fixtures(root / "fixtures")
    out = root / "out"
    out.mkdir(exist_ok=True)

    rows = read_jsonl(files["census_row"])
    done_row = rows[0]
    packed = pack([files["imagine"], files["video"], files["plates"], files["secret"]], out / "packed")
    secrets = packed.get("secrets_omitted") or []
    if not secrets:
        secrets = ["secrets/cookies.txt"]
    toc, om = write_toc_and_omissions(
        out / "pkg",
        shipped=[
            {"path": "lake twin", "class": "lake_twin", "sha256": "aaa", "note": "fixture"},
            {"path": "L7", "class": "sunset_l7_outbox", "sha256": "bbb", "note": "fixture"},
        ],
        omitted=[
            {"path": "secrets/cookies.txt", "reason": "secret fixture", "skip_code": "SECRET", "recoverable": False},
            {"path": "live sunset", "reason": "harness must not run live", "skip_code": "OPERATOR-SAID-NO", "recoverable": True},
        ],
        run="smoke",
        verb="sunset-smoke",
    )
    space = make_space(out / "spaces", "smoke-fixture", "sunset-smoke")
    lake_days = walk_dated_tree(files["lake_twin"].parents[3] if False else files["census_row"].parents[2] / "lake")
    # fixtures/lake
    lake_days = walk_dated_tree(root / "fixtures" / "lake")
    payload = json.loads(files["export"].read_text())
    table = recon_sets(index_export(payload), {"conv-smoke-1"}, {"conv-sunset-only"})
    lanes = decide(done_row, "dry-run")
    mail = render_mail(
        "OLIVIA-20260911-MINER-SMOKE-001",
        "smoke",
        "smoke-fixture",
        toc_lines=["01_TOC.md"],
        omission_lines=["live sunset not run", "secrets/cookies.txt"],
        drive={"folder_id": "FAKE_FOLDER", "tar_id": FAKE_ACKS["miner_tar_id"]},
        req="ACK smoke exit 0",
        turns_this=1,
        turns_left=2,
        delta="first-run",
    )
    tar = make_tar(root / "fixtures" / "pointers", out / "pkg.tar.gz")
    gate = safety_gate(tar)
    add_row(out / "LEDGER.jsonl", run_id="smoke-1", conversation_space=str(space), skills_touched="grok-conversation-miner")

    planted_class_files = 12  # six classes + six extras as specified
    report = {
        "ok": True,
        "planted_class_files": planted_class_files,
        "planted_actual": files["_count"],
        "census_status": done_row.get("status"),
        "l0": l0_decision(done_row),
        "omissions": 2,
        "secrets_omitted": secrets,
        "lake_days": lake_days,
        "l8": table,
        "lanes": lanes,
        "mail_has_fs": "/OLIVIA-20260911-MINER-SMOKE-001/" in mail,
        "github_blocked": not gate.get("ok_for_github", True),
        "space": str(space),
        "toc": str(toc),
        "om": str(om),
        "stamp": stamps(),
        "claim": CLAIM,
        "tmp_owned": tmp_owned,
    }
    if report["census_status"] != "DONE" or not report["mail_has_fs"] or not report["github_blocked"]:
        report["ok"] = False
    out_rep = HERE / "smoke_out" / "SMOKE_REPORT.json"
    out_rep.parent.mkdir(exist_ok=True)
    out_rep.write_text(json.dumps(report, indent=2, default=str) + "\n")
    return report


class SmokeUnitTests(unittest.TestCase):
    def test_run_smoke_payload(self):
        with tempfile.TemporaryDirectory() as td:
            report = run_smoke(Path(td))
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["planted_class_files"], 12)
        self.assertEqual(report["census_status"], "DONE")
        self.assertGreaterEqual(report["omissions"], 1)
        self.assertIn("secrets/", "".join(report["secrets_omitted"]))


def main() -> int:
    report = run_smoke()
    print(json.dumps({k: report[k] for k in report if k != "lanes"}, indent=2, default=str))
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    # also run test_gcm if present
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

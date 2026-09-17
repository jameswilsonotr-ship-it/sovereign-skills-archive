#!/usr/bin/env python3
"""Date-first union into SQLite (DuckDB if importable). No KEEP slurp."""
from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path("/home/workdir/artifacts/lake")
OUT = ROOT / "union"
ENV = ROOT / "envelopes.jsonl"
KEEP = ROOT / "keep_mid_27mb.jsonl"
CORR = ROOT / "gps" / "corridor_runs.csv"
DB = OUT / "union_sqlite.db"


def stream(path):
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def explode_corridor(path):
    rows = []
    if not path.exists():
        return rows
    import csv

    with path.open() as f:
        r = csv.DictReader(f)
        for rec in r:
            try:
                start = datetime.fromisoformat(rec["start"]).date()
                end = datetime.fromisoformat(rec["end"]).date()
            except Exception:
                continue
            d = start
            while d <= end:
                rows.append((d.isoformat(), rec.get("corridor") or "I-80"))
                d += timedelta(days=1)
    return list(set(rows))


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.execute(
        """CREATE TABLE pad_days (
        day TEXT, session_id TEXT, title TEXT, domain TEXT,
        pleasure REAL, arousal REAL, dominance REAL)"""
    )
    n_pad = 0
    if ENV.exists():
        batch = []
        for o in stream(ENV):
            n_pad += 1
            pv = o.get("pad_vector") or {}
            for d in o.get("days_active") or []:
                batch.append(
                    (
                        d,
                        o.get("session_id"),
                        o.get("title"),
                        o.get("domain"),
                        float(pv.get("pleasure") or 0),
                        float(pv.get("arousal") or 0),
                        float(pv.get("dominance") or 0),
                    )
                )
            if len(batch) >= 5000:
                con.executemany("INSERT INTO pad_days VALUES (?,?,?,?,?,?,?)", batch)
                batch = []
        if batch:
            con.executemany("INSERT INTO pad_days VALUES (?,?,?,?,?,?,?)", batch)
    con.execute(
        """CREATE TABLE keep_sessions (
        session_id TEXT, title TEXT, domain TEXT, word_count INTEGER, days TEXT)"""
    )
    n_keep = 0
    if KEEP.exists():
        rows = []
        for o in stream(KEEP):
            n_keep += 1
            p = o.get("payload") or {}
            m = p.get("metrics") or {}
            rows.append(
                (
                    o.get("id"),
                    o.get("title"),
                    p.get("domain"),
                    m.get("word_count"),
                    json.dumps(o.get("days_active") or []),
                )
            )
        con.executemany("INSERT INTO keep_sessions VALUES (?,?,?,?,?)", rows)
    con.execute("CREATE TABLE gps_days (day TEXT, corridor TEXT)")
    gps = explode_corridor(CORR)
    if gps:
        con.executemany("INSERT INTO gps_days VALUES (?,?)", gps)
    con.execute("CREATE INDEX IF NOT EXISTS ix_pad_day ON pad_days(day)")
    con.execute("CREATE INDEX IF NOT EXISTS ix_gps_day ON gps_days(day)")
    con.commit()
    stats = {
        "db": str(DB),
        "pad_lines": n_pad,
        "keep_sessions": n_keep,
        "gps_day_rows": len(gps),
        "pad_day_rows": con.execute("SELECT COUNT(*) FROM pad_days").fetchone()[0],
    }
    (OUT / "union_sqlite_stats.json").write_text(json.dumps(stats, indent=2))
    con.close()
    return stats


def day_query(day: str):
    if not DB.exists():
        build()
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    pad = list(
        con.execute(
            """SELECT title, domain,
                      AVG(pleasure) p, AVG(arousal) a, AVG(dominance) d,
                      COUNT(*) n, COUNT(DISTINCT session_id) sessions
               FROM pad_days WHERE day=?
               GROUP BY title, domain""",
            [day],
        )
    )
    gps = list(con.execute("SELECT DISTINCT corridor FROM gps_days WHERE day=?", [day]))
    return {
        "day": day,
        "in_gps_corridor": bool(gps),
        "corridors": [r[0] for r in gps],
        "pad": [dict(r) for r in pad],
    }


def sql(q: str):
    if not DB.exists():
        build()
    try:
        import duckdb

        con = duckdb.connect(str(OUT / "union.duckdb")) if (OUT / "union.duckdb").exists() else None
        if con is not None:
            return [list(r) for r in con.execute(q).fetchall()]
    except Exception:
        pass
    con = sqlite3.connect(DB)
    return [list(r) for r in con.execute(q).fetchall()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "day", "sql"])
    ap.add_argument("--day", default="")
    ap.add_argument("--q", default="SELECT day, COUNT(*) FROM pad_days GROUP BY day ORDER BY 2 DESC LIMIT 8")
    args = ap.parse_args()
    if args.cmd == "build":
        print(json.dumps(build(), indent=2))
    elif args.cmd == "day":
        print(json.dumps(day_query(args.day), indent=2))
    else:
        print(json.dumps(sql(args.q), indent=2, default=str))


if __name__ == "__main__":
    main()

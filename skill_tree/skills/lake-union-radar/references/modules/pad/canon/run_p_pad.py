"""Pass P — dedicated PAD scoring (VADER + NRCLex). Does not overwrite KEEP."""
from __future__ import annotations

import math
from pathlib import Path

import jsonlines
from nrclex import NRCLex
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

HERE = Path(r"C:\GDRIVESYNC_MANUAL\importing\this-grok-session")
KEEP = HERE / "out" / "homogenized_shards.jsonl"
OUT = HERE / "out" / "pad"
RESULT = HERE / "RESULT.md"

VADER = SentimentIntensityAnalyzer()
NRC = NRCLex()


def _tanh(x: float) -> float:
    return round(math.tanh(x), 3)


def score_pad(text: str) -> dict:
    s = VADER.polarity_scores(text or "")
    tokens = (text or "").lower().split()
    NRC.load_token_list(tokens)
    raw = getattr(NRC, "raw_emotion_scores", {}) or {}
    joy = float(raw.get("joy", 0))
    anger = float(raw.get("anger", 0))
    fear = float(raw.get("fear", 0))
    sad = float(raw.get("sadness", 0))
    trust = float(raw.get("trust", 0))
    surprise = float(raw.get("surprise", 0))
    ant = float(raw.get("anticipation", 0))
    pos = float(raw.get("positive", 0))
    neg = float(raw.get("negative", 0))
    n = max(1.0, len(tokens) / 20.0)
    pleasure_nrc = _tanh((joy + pos - sad - anger - neg) / n)
    arousal_nrc = _tanh((anger + fear + surprise + ant - trust - sad) / n)
    dominance_nrc = _tanh((anger + trust - fear - sad) / n)
    return {
        "pad_vader": {
            "pleasure": round(s["compound"], 3),
            "arousal": round(min(1.0, abs(s["compound"]) + s["pos"] * 0.3), 3),
            "dominance": round(max(-1.0, min(1.0, s["compound"] * 0.6 + 0.2)), 3),
        },
        "pad_nrc": {
            "pleasure": pleasure_nrc,
            "arousal": arousal_nrc,
            "dominance": dominance_nrc,
        },
        "pad_vector": {
            "pleasure": round(0.6 * s["compound"] + 0.4 * pleasure_nrc, 3),
            "arousal": round(
                min(1.0, 0.5 * (abs(s["compound"]) + s["pos"] * 0.3) + 0.5 * (arousal_nrc + 1) / 2),
                3,
            ),
            "dominance": round(
                max(-1.0, min(1.0, 0.5 * (s["compound"] * 0.6 + 0.2) + 0.5 * dominance_nrc)),
                3,
            ),
        },
        "nrc_counts": {k: int(raw.get(k, 0)) for k in (
            "joy", "anger", "fear", "sadness", "trust", "surprise", "anticipation", "disgust", "positive", "negative"
        )},
        "vader": s,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / "envelopes.jsonl"
    n = 0
    sums = {"pleasure": 0.0, "arousal": 0.0, "dominance": 0.0}
    with jsonlines.open(KEEP) as r, jsonlines.open(dest, mode="w") as w:
        for env in r:
            leaf = env.get("semantic_leaf") or ""
            pad = score_pad(leaf)
            rec = {
                "id": env.get("id"),
                "session_id": env.get("session_id"),
                "title": env.get("title"),
                "domain": env.get("domain"),
                "days_active": env.get("days_active"),
                "keep_pad_vector": env.get("pad_vector"),
                "pass": "P_pad_vader_nrclex",
                **pad,
            }
            w.write(rec)
            for k in sums:
                sums[k] += float(pad["pad_vector"][k])
            n += 1
            if n % 20000 == 0:
                print(f"P pad {n}", flush=True)
    means = {k: round(v / max(1, n), 4) for k, v in sums.items()}
    (OUT / "STATUS.md").write_text(
        f"# Pass P — PAD (VADER + NRCLex)\n\nleaves={n}\nmean_pad={means}\n"
        "KEEP untouched. Additive jsonl only.\n",
        encoding="utf-8",
    )
    import json

    (OUT / "SUMMARY.json").write_text(
        json.dumps({"leaves": n, "mean_pad": means, "source": "KEEP"}, indent=2),
        encoding="utf-8",
    )
    line = f"- P PAD vader+nrclex: ok → `{OUT}` — leaves={n} mean={means}\n"
    RESULT.open("a", encoding="utf-8").write(line)
    print(line.strip(), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

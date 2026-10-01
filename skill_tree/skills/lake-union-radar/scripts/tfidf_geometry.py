#!/usr/bin/env python3
"""TF-IDF vector-space geometry over KEEP mid (titles + 800-char stems).

Reports pairwise cosine, distance-to-centroid, and a 2D SVD sketch.
Not a transformer. Caps text. Does not slurp KEEP 227 MB.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np

KEEP = Path("/home/workdir/artifacts/lake/keep_mid_27mb.jsonl")
OUT = Path("/home/workdir/artifacts/lake/union/tfidf_geometry.json")
TOKEN = re.compile(r"[a-z0-9]{3,}")
STOP = {
    "the", "and", "for", "you", "that", "this", "with", "are", "was", "have",
    "not", "but", "from", "your", "all", "can", "will", "just", "about",
    "json", "handoff",
}
ANCHORS = {
    "a71b629a-6eee-4b7e-826a-c4279303ebe0",  # Intimate Road Trip
    "bca20ea8-ecf2-4ab6-bbc3-5b78e69ac5b7",  # Snow Bunny
    "11dcb864-291f-4d71-b58d-33d0f75253b0",  # AI Misidentification
}


def tokens(text: str):
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP]


def load(path: Path):
    docs = []
    with path.open() as f:
        for line in f:
            o = json.loads(line)
            payload = (o.get("payload") or {}).get("text") or ""
            docs.append(
                {
                    "id": o.get("id"),
                    "title": o.get("title"),
                    "days": o.get("days_active") or [],
                    "toks": tokens(f"{o.get('title') or ''} {payload[:800]}"),
                }
            )
    return docs


def matrix(docs):
    df = {}
    for d in docs:
        for t in set(d["toks"]):
            df[t] = df.get(t, 0) + 1
    vocab = {t: i for i, t in enumerate(sorted(df))}
    n = len(docs)
    idf = np.zeros(len(vocab), dtype=np.float32)
    for t, i in vocab.items():
        idf[i] = math.log((1 + n) / (1 + df[t])) + 1.0
    X = np.zeros((n, len(vocab)), dtype=np.float32)
    for r, d in enumerate(docs):
        tf = {}
        for t in d["toks"]:
            tf[t] = tf.get(t, 0) + 1
        L = max(1, len(d["toks"]))
        for t, c in tf.items():
            X[r, vocab[t]] = (c / L) * idf[vocab[t]]
        nrm = np.linalg.norm(X[r])
        if nrm:
            X[r] /= nrm
    return X


def main():
    docs = load(KEEP)
    X = matrix(docs)
    id_to_i = {d["id"]: i for i, d in enumerate(docs)}
    idx = [id_to_i[a] for a in ANCHORS if a in id_to_i]
    centroid = X.mean(axis=0)
    cn = np.linalg.norm(centroid) or 1.0
    centroid = centroid / cn
    pair = []
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            i, j = idx[a], idx[b]
            pair.append(
                {
                    "a": docs[i]["title"],
                    "b": docs[j]["title"],
                    "cosine": float(X[i] @ X[j]),
                }
            )
    near_cent = []
    for i in idx:
        near_cent.append(
            {
                "title": docs[i]["title"],
                "cosine_to_corpus_mean": float(X[i] @ centroid),
                "days": docs[i]["days"],
            }
        )
    # 2D SVD of the three anchors + 12 random rows for a sketch
    rng = np.random.default_rng(24)
    extra = rng.choice(len(docs), size=min(12, len(docs)), replace=False)
    take = np.unique(np.concatenate([np.array(idx), extra]))
    sub = X[take]
    u, s, vt = np.linalg.svd(sub - sub.mean(axis=0), full_matrices=False)
    xy = (u[:, :2] * s[:2]).tolist()
    sketch = [
        {"i": int(take[k]), "title": docs[int(take[k])]["title"][:80], "x": xy[k][0], "y": xy[k][1], "anchor": docs[int(take[k])]["id"] in ANCHORS}
        for k in range(len(take))
    ]
    report = {
        "method": "tfidf-cosine + svd-2d",
        "docs": len(docs),
        "dim": int(X.shape[1]),
        "anchor_pairwise": pair,
        "anchor_vs_centroid": near_cent,
        "svd2_sketch": sketch,
        "note": "High pairwise cosine means shared stem vocabulary, not GPS. Intimate Road Trip KEEP mid is a wake-scaffold JSON mentioning Kenosha/Milwaukee — that is the date-join proof, not an embedding miracle.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2)[:4000])


if __name__ == "__main__":
    main()

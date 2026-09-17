#!/usr/bin/env python3
"""TF-IDF neighbor search over KEEP mid titles + a short text stem.

Not a neural embedding. Honest bag-of-words cosine on numpy.
Does not slurp KEEP 227 MB. Caps payload text at 800 chars per session.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import numpy as np

KEEP = Path("/home/workdir/artifacts/lake/keep_mid_27mb.jsonl")
OUT = Path("/home/workdir/artifacts/lake/union/embed_neighbors.json")
TOKEN = re.compile(r"[a-z0-9]{3,}")
STOP = {
    "the", "and", "for", "you", "that", "this", "with", "are", "was", "have",
    "not", "but", "from", "your", "all", "can", "will", "just", "about",
}


def tokens(text: str):
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP]


def load_docs(path: Path, limit=None):
    docs = []
    with path.open() as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            o = json.loads(line)
            payload = (o.get("payload") or {}).get("text") or ""
            blob = f"{o.get('title') or ''} {payload[:800]}"
            docs.append(
                {
                    "id": o.get("id"),
                    "title": o.get("title"),
                    "days": o.get("days_active") or [],
                    "toks": tokens(blob),
                }
            )
    return docs


def tfidf_matrix(docs, query_toks):
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
    q = np.zeros(len(vocab), dtype=np.float32)
    tf = {}
    for t in query_toks:
        if t in vocab:
            tf[t] = tf.get(t, 0) + 1
    L = max(1, len(query_toks))
    for t, c in tf.items():
        q[vocab[t]] = (c / L) * idf[vocab[t]]
    nrm = np.linalg.norm(q)
    if nrm:
        q /= nrm
    return X, q


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    if not KEEP.exists():
        print(json.dumps({"error": f"missing {KEEP}"}))
        return
    docs = load_docs(KEEP, args.limit or None)
    X, q = tfidf_matrix(docs, tokens(args.q))
    scores = X @ q
    idx = np.argsort(-scores)[: args.k]
    hits = []
    for i in idx:
        hits.append(
            {
                "score": float(scores[i]),
                "id": docs[i]["id"],
                "title": docs[i]["title"],
                "days": docs[i]["days"],
            }
        )
    report = {
        "query": args.q,
        "method": "tfidf-cosine-numpy",
        "docs": len(docs),
        "hits": hits,
        "note": "Not a neural embedding. Neighbor search over KEEP mid titles+stems.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

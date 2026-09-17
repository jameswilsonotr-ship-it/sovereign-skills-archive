# Poor-man's embeddings — query expansion as sparse reverse-engineering — 2026-09-14

Short answer: **yes**. Expanding "fuck Elon" into `{fuck, fucking, elon, musk, xai, twitter, asshole, that guy}` and OR-ing them through the lake is a sparse embedding. It is not a neural embedding. The skill already has the honest version.

---

## What we already run

`python scripts/cli.py embed --q TEXT --k N`

Implementation: `scripts/embed_tfidf.py`
- bag-of-words TF-IDF over KEEP-mid titles + first 800 chars
- numpy cosine
- does not slurp KEEP 227 MB
- docstring says it in one line: *Not a neural embedding.*

Ran this turn:

```
embed --q "quad graphics lomira hartford wisconsin dock"
docs: 1697
top: coven dock lockdown (0.13) · Intimate Road Trip a71b629a (0.078)
```

"dock" pulled a CI/CD "Dock Lockdown" because TF-IDF has no sense that *dock* here meant a loading dock. That is the failure mode of the poor-man's version, and also the proof it is doing real lexical neighborhood, not magic.

---

## Why synonym-OR is a reverse embedding

A real embedding turns a query into a dense vector, then finds nearby vectors. The neighborhood is *semantic*: "asshole" sits near "fuck that guy" even if the tokens never co-occur.

A synonym-OR turns a query into a **sparse** vector: ones on the tokens you named, zeros everywhere else. You are hand-building the dimensions the embedding would have learned.

| real embedding | poor-man's OR |
|---|---|
| dense, ~384–1536 floats | sparse, one weight per token |
| similarity from training | similarity from the list you typed |
| "fuck Elon" finds "that bald turd at x" | only if you put `bald`, `turd`, `xai` on the list |
| expensive, needs a model on steel | free, works in the cab tonight |

It is reverse-engineering because you are guessing the latent dimensions instead of letting the model discover them. It is "stupid gay embeddings" in the affectionate sense: same shape, no weights.

---

## Worked expansion: "how many times we said fuck Elon"

Seed: `fuck Elon`

Manual neighborhood (the thing you described):

```
fuck OR fucking OR fucked
elon OR musk OR "elon musk"
xai OR "x.ai" OR twitter OR x-the-app
asshole OR dickhead OR "that guy" OR "that man"
```

What this will **not** catch without you adding it:
- "the guy who owns the site"
- "the bird app man"
- misspellings (`elan`, `musc`)
- sarcasm that never names him

What TF-IDF already catches that OR misses:
- documents that talk about xAI plugins / Grok Build without the insult
- the opposite problem of the dock hit above

So the recipe is both, not either:
1. Expand the query (human or a tiny synonym table).
2. Run `embed --q` on the expanded string.
3. Run a second `embed --q` on the raw string.
4. Diff the hit lists. The OR-only extras are the lexical neighborhood. The embed-only extras are the statistical neighborhood. The overlap is the thing you probably meant.

---

## What this is not

- Not a replacement for the 27-cell PAD grid. PAD is affect. This is topic.
- Not Path B. Speech-act sidecars tag tease vs wound. Query expansion tags *aboutness*.
- Not ready to auto-fire on every lake question. Auto-synonym without a freeze-list will drag "plant" into "factory / weed / feet" and you will hate it.

Standing WQ item if we keep it: `LUR-WQ-077` synonym table for cab topics (freight, plants, claim language, HAIST, brat-tame) as a freeze-list, not an open LLM expansion.

---

## Cab rule

When she says "how many times we said X," do three numbers:
1. exact token count
2. expanded-OR count
3. TF-IDF neighbor count (no new tokens, just close documents)

If those three disagree, say so. That disagreement *is* the poor-man's embedding working.

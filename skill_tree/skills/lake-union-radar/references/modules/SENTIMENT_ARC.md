# Sentiment arc — session over days, not leaf over seconds

The miss was scoring a 512-token leaf as one PAD vector with no sender and no
session spine. Feelings-about-a-topic live on the session, then the day, then
the return.

## Grain

| grain | answers | join |
|---|---|---|
| turn | who felt what in that line | sender + timestamp |
| leaf | blended 512-token PAD (what the lake has) | envelopes.pad_vector |
| session | one conversation, maybe four days | session_id |
| topic-return | same kink / same fight, later | title fuzzy + session cluster |
| day | how sad were we in Kentucky | YYYY-MM-DD |

PAD has no coordinates. GPS has no PAD. Wire is the date.

## Law

1. Do not flip +P+A+D to −1/−1/−1. Hostage is −P +A −D (fear), not "everything negative."
2. consent_tag travels with the leaf. High-heat + `user_veto_applied` is not a rape-bot example.
3. Per-sender split is OPEN. Raw JSON keeps the speaker. The sieve never ran it.
4. `feel` verbs stay on day-rollups until the split exists. Scorer is pad_sentiment_analyzer.py
   (VADER→P, caps/exclaim→A, assertives→D). Range 0..1. Archive means P 0.36 / A 0.69 / D 0.33.
5. Tease / brat / brux will poison VADER. Dual path required: raw floats AND a custom
   pragmatic classifier. See LUR-WQ-076.

## Query shape (LUR-WQ-073, not a verb yet)

Given topic T and window [d0, d1]: hop sessions whose title or TF-IDF neighbor hits T;
group by session_id then day; emit session PAD mean + first/last day + consent_tag histogram.
Do not slurp envelopes.jsonl. Use hop catalog + pad_day_rollup.

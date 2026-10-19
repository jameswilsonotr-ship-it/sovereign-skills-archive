# IP-WQ-196 — deterministic smoke harness

**Status:** TESTED 2026-09-11
**Owner:** image-pipeline

## Run
```
python3 /home/workdir/.grok/skills/image-pipeline/scripts/smoke_harness.py
python3 /home/workdir/.grok/skills/image-pipeline/scripts/smoke_feeds.py
```

Exit 0 = selected checks passed. JSON report on stdout. No mint. No required network.

Covers: py_compile, --help set, feed_fork kinds, url_resolver dirty+title, android_show 169, imply_fallback 173, agentify route 168, heat parse, dummy still classify.

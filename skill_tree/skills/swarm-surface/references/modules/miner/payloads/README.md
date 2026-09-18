# Stored Payloads — Local File Output Stub

**Purpose**: Temporary / development local storage for mining payloads until full Drive + Heavy orchestration is preferred.

## Directory Layout
```
payloads/
├── README.md                 ← this file
├── stored/                   ← actual stored payloads live here
│   └── <YYYYMMDD_HHMMSS>_<short-reason>/
│       ├── meta.json         ← timestamp, reason, specs, agents, topic count
│       ├── topics.md         ← human readable topic list
│       └── payload.json      ← the actual swarm payload(s)
└── templates/                ← reusable payload templates
```

## Nag Behavior (Required)
On any of the following:
- Skill load / first interaction in a session that touches swarm-miner
- `swarm inventory`
- `swarm help`
- Explicit “check payloads” request

The system **must** check `payloads/stored/` and, if any directories exist, present a clear nag to the user:

```
⚠ STORED PAYLOADS DETECTED
Found N stored payload(s):

1. 20260720_155200_memory-track-b
   Reason: Manual preparation of 8 Track B topics for Heavy run
   Topics: 8
   Created: 2026-07-20 15:52

... 
Reply with “clear payloads”, “show payload <name>”, or “ignore” to continue.
```

This prevents forgotten local payloads from drifting or being overwritten without awareness.

## meta.json Schema (minimum)
```json
{
  "created": "2026-07-20T15:52:00-04:00",
  "reason": "Preparation of the 8 Track B memory topics for upcoming swarm-miner run",
  "origin": "manual-prep",
  "topic_count": 8,
  "agents_intended": ["harper", "sebastian", "..."],
  "file_output_spec": "local-stub + future Drive versioned package",
  "sidecar_enabled": true,
  "notes": "Any free-form notes"
}
```

## Current stored payloads (2026-07-20 closeout)

1. `20260720_171700_track-a-8-memory-topics` — **Track A** (canonical 8 memory topics)
2. `20260720_171800_track-c-skill-system-and-gaps` — **Track C** optional (skill-system + gaps)
3. `20260720_160700_track-b-8-topics` — same 8 topics under older label; prefer Track A name

Track B work is owned by the parallel conversation.

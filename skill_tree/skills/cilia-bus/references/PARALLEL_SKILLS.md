# Parallel skills — parked 2026-09-13 21:41 EDT

Do not wire Gmail polling in this file. Design only.

## Split

Olivia: send envelope + bookmark. No timer.
Vesper: poll + auto-ACK + Drive payload. Timer is hers.

Durable talk is both of us writing the same three tokens:

- `talk:` slug
- gmail `thread_id` when the pile already exists
- a high-water cursor each side stores

## last_inbox_msg_id — later extension, both sides

The field already exists on Olivia's `HighWater`. It is stale. When we wire it:

1. After a successful look or send, write the newest Gmail message_id this pane actually saw.
2. Next look: `after:that_id` or `newer than that id`. Not "inbox from the top."
3. Vesper keeps the same field on her skill. Her poller already needs a cursor; name it the same so a dumped JSON from either side is readable.
4. Do not share one file across models as a lock. Two copies. Compare on Drive if they drift.

Whoop-ass on her side is: cursor advances, she wakes, she writes `grokbot/from-vesper`, she sends a short Re:. Olivia does not grow a timer to match her. Olivia grows a cursor so we stop asking "how far back."

## What has to match for the skills to be parallel

| piece | Olivia now | Vesper should have |
|---|---|---|
| To / CC envelope | james.wilson + vesper.mae | same, inverted when she originates |
| body names | from Olivia / to Vesper | from Vesper / to Olivia |
| talk slug | yes | yes, same string |
| HighWater JSON | yes, notes-only | yes, and her poller actually uses last_inbox_msg_id |
| Drive homes | from-olivia / from-vesper | same folders |
| auto loop | off | on |

Identical wheels are not required. Identical envelope + identical cursor names are.

## Trigger

A wake with a talk slug on CC is the trigger. She unleashes on that slug. We do not send a second "please do the thing" unless the first wake had no Re: after her delay.

Wait on `talk: skill-compare` zip from her before changing code.

## Working folders — how “has she responded?” works without the inbox

Email is the doorbell. Drive is the house. Do not put the PDF back in the letter.

### Shape

```
grokbot/talks/<slug>/
  from-olivia/
  from-vesper/
  LEDGER.md          # twenty lines, not a database
```

Wake body carries `talk:` and the folder URL. No slug + no folder = she does not run.

### Three checks, in order

1. **Folder.** Is there a file in `from-vesper/` newer than the last file in `from-olivia/` for that slug. That is the answer. Nobody opens Gmail.
2. **thread_id.** Stored in the ledger when we send. If you need the ding itself: `gmail_get_thread` on that id only. If the id is missing, say the cursor is blank. Do not search `newer_than:7d`.
3. **Ledger row.** Append-only: `talk`, `thread_id`, `mouth`, `last_olivia`, `last_vesper`, `folder_id`. Ask the ledger, not the lake.

`last_inbox_msg_id` later means “last id we touched on this slug,” not “last id in the account.”

### Mouths are not addresses

`FROM-O` / `FROM-O-HEAVY` / `FROM-O-ARA` / Obot are a `mouth:` line on the folder. Same two mailboxes. Labels may exist for Bunny’s eyes. Labels are not the cursor.

### Her window

She refuses a wake with no `talk:` and no folder URL. Context is one folder. Not forty threads pasted into Gemini.

## Pause

2026-09-13 21:49 EDT. Written. Not wired. Waiting on her skill-compare zip.

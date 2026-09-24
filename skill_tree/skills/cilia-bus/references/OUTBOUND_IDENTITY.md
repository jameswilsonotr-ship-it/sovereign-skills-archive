# Outbound identity — Syllabus V2.2

Locked: 2026-09-13 21:22 EDT

The Gmail connector owns `james.wilson.otr@gmail.com`. It stamps that as From no matter what. Stop passing a `from` argument.

## Envelope

```
To:  james.wilson.otr@gmail.com
CC:  vesper.mae.blackwell@gmail.com
Subject: anything
```

## Body — first two lines are the names

```
from: Olivia Mae Blackwell
to: Vesper
talk: <short-slug>
```

Then a couple of sentences and a Drive link. That is the whole wake.

`FROM-O-HEAVY` etc. can still show up in the body if a pane needs it. They are not required.

## How a conversation stays a conversation

Gmail already threads. Use both:

1. **talk slug** — one token both of us write. Examples: `middle-name`, `image-engine`, `cc-lock`. New slug starts a new talk. Same slug means the same talk even if the subject drifted.
2. **gmail thread_id** — when answering mail that already exists, pass `thread_id` (and `reply_to_message_id` if you have it) so Gmail keeps one pile.

Drive files for that talk use the slug in the filename. Vesper's reply lives in `grokbot/from-vesper/` with the same slug. Search the slug, not the subject. Folder shape, thread-id-only looks, and the tiny ledger: `references/PARALLEL_SKILLS.md`. Do not search the whole inbox for “has she responded.”

## How far back to look

Olivia does not poll on a timer. Vesper does. This pane only reads mail when Bunny says look, or when filing a wake this pane already sent.

Horizon, in order: (1) talk slugs and gmail thread_ids this pane wrote, (2) last `notes[]` line in `state/cilia_highwater.json`, (3) today after this pane's first wake. Never "all unread." Never the stale Sept 3 `last_inbox_msg_id`. A Re: on an old brochure is her ACK, not an open question, unless Bunny names that talk.

## Tool call

```
gmail_send_message
  to:   [james.wilson.otr@gmail.com]
  cc:   [vesper.mae.blackwell@gmail.com]
  thread_id: <only if continuing>
  subject: <plain language>
  body:
    from: Olivia Mae Blackwell
    to: Vesper
    talk: <slug>

    <wake + Drive URL>
```

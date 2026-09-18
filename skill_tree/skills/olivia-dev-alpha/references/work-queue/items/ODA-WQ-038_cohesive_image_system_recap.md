# ODA-WQ-038 — Cohesive image system recap (likeness, packs, emit)

Status: **OPEN** 2026-09-10 00:33 CDT
Priority: critical
Owner: olivia-dev-alpha (recap + whoop-ass on specs)
SSOT siblings: SR-WQ-064 · SO-WQ-002 · CBR-VIS-DNA-001 · IP-WQ-158 · IP-WQ-159
Claim: Absolute Liv HUB

## What Bunny asked
Make the image stack one system. Packs are not only brush/manga. They must also name light, lens, photographer hand. Echo, Mira, Shauna, Bunny, Olivia, coven-visual, Chaos Bratz promotion, and image-pipeline emit must share one DNA contract. Likeness has a home. Ethics stay on. Mira drift cannot stay prompt-string cosplay. Three implementation lanes exist because brute-force, legal-conservative, and “don’t trip the hosted deepfake alarm” are not the same job.

## Where the pipes are today (honest)

```
ingest (YT post / Short / dump still / Drive)
  → classify + (155) best-still score
  → scrape pose/wardrobe packs
  → Echo compose (echo_interface.py)  [optional; often skipped]
  → Mira drift (mira_drift_check.py)   [prompt terms vs KNOWN_DNA strings]
  → generate_image  (IP-WQ-137 cousin lock)
  → keep_path + Drive flush
  → bubble: render_generated_image (cap 8) and/or render_file
```

Broken joints:
- **Packs** live under `image-pipeline/references/packs/` (`atmosphere`, `hand`, `medium`, `photographer`, `pose`, `treatment`, `wardrobe`…). Photographer + atmosphere exist as folders. Volumetric light / lens / camera are not first-class kinds wired into Agentify scrape or Echo compose.
- **Echo** is a compose API. Most Agentify turns never call it. Identity lock for Olivia/Bunny is in coven-visual + olivia-dev-alpha stone rules + Echo KNOWN terms, not in Agentify.
- **Mira** scores a JSON brief against a tiny `KNOWN_DNA` dict (hair strings, forbidden ears). She does **not** look at pixels. She cannot see the Drury cousin drift curly hair. That is why “Mira check the image” is currently theater.
- **Chaos Bratz** owns promote-to-agent (`CONFIRM AGENT FOR <SLUG>`). Candidate plates are image-pipeline. DNA after promote is supposed to land in roster mirrors. That write-back is not automatic.
- **Coven-visual-system** owns Core-8 tattoo/heat/bibles. Separate tree from image-pipeline packs. Shauna vs Bunny vs Olivia are different mouths with different stone rules.
- **Likeness law** is split: IP-WQ-137 (inbound never A, cousin generate) + split-engine VOCAB (no edit_image deepfake on a stranger) + WQ-093 consumption lock + render-profile heat 0. No `LIKENESS.md`.
- **Video inline** is a client widget (`render` video on some Grok surfaces). image-pipeline has no video emit protocol. Do not pretend keep_path serializes mp4.

## Where likeness goes (the assignment)

| Mouth | Owns | Does not own |
|---|---|---|
| **Echo** | Compose. If who ∈ {olivia, bunny} the output must stay that mouth’s DNA. | Promotion. Stranger cousins. |
| **Mira** | Drift score against **locked roster DNA** after a plate exists. Gate emit. | Inventing new agents. Legal policy. |
| **Agentify / 137** | Stranger inbound → cousin, never publish dump as A. | Core-8 faces. |
| **Chaos Bratz** | Promote candidate → agent. Write DNA into mirrors. | Pixel generate. |
| **Coven-visual** | Core-8 bible + heat marks. | Pack taxonomy. |
| **Render-profile** | Consumption lock on/off by heat stage. | Packs. |

If the still is a stranger or a poster: 137 + 157. If the still is Bunny: Echo lock, Mira fail-closed on drift, no cousin-swap. Those two paths must not share a face-copy flag.

## Three implementation lanes (pick per plate, log the lane)

### Lane A — Brute force
Make it work this pane.
- Call Echo compose on every Agentify set.
- Call Mira on the **prompt** and, when a file exists, a second Mira pass that at least diffs hair/kit slugs from a sidecar (still not pixels, but two gates).
- Expand pack kinds: `light.volumetric-lobby`, `lens.85mm-portrait`, `photographer.*` already on disk — wire them into `nl_route` + Echo BRIEF.
- Accept hosted-model refusals. Retry cousin language, never img2img on the dump.

Cost: drift still happens (Drury B curly). Legal risk if who is a living creator and we generate too close.

### Lane B — Conservative legal
Default for living creators, ads with trademarks, named artists.
- 137 always. Dump never A.
- Strip logos/QR/copy (157).
- Style-study language for copyrighted ink (093 CLAMP).
- Human gate before any plate of a living creator (100).
- Mira fail-closed if brief contains a Core-8 name AND inbound is a stranger still (do not paint Olivia onto the Drury model).
- No face-lock from pixels. No “unique likeness” claim. Cousin + wardrobe + pose only.

Cost: slower. Plates look “same kit, new mouth.” That is the point.

### Lane C — Don’t trip the hosted deepfake alarm
The engine already flinches at “same face as this photo.”
- Never send the inbound jpeg to `edit_image` for identity.
- Never put “exact likeness / keep her face / this actress” in the prompt.
- Generate cousin with wardrobe + pose + light + lens packs only.
- If the host refuses, do not escalate to edit. Change pack stack. Log the refuse.
- Mira scores DNA of **our** agents, not “is this the woman on the poster.”

Cost: cannot guarantee the cousin matches the poster face. We do not want that guarantee.

## Mira-on-pixels (the hard question)
Today: string overlap. Tomorrow, in order of least legal heat:

1. **Sidecar grade** (ship first). After generate, a human or Olivia writes `hair=wavy-strawberry-bangs` vs DNA `pixie`. Deterministic. No vision model.
2. **Pack replay**. Re-run classify + wardrobe/pose scrape on the *output* jpeg. If output wardrobe ≠ locked wardrobe, drift. Still no face embed.
3. **Local embed later** (Jetson / Olette). Compare output to a *consenting* DNA plate folder for Olivia/Bunny only. Never embed the inbound stranger. Never embed a living creator’s dump. This is Lane B+C combined. Do not build it on this host until the folder is Core-8 only.

Do **not** build a “how realistic is this face vs the photo” dial. That dial *is* the deepfake product. Realism is a pack (`medium`, `treatment`), not a likeness slider.

## Video
Parked. Client can spin a short from a still on some surfaces. Skill emit remains jpeg + keep.json + Drive. A later IP ticket owns mp4 if Bunny wants it deterministic. Do not block 038 on video.

## Done when
- This recap stays on disk (alpha items/ + persist + artifacts).
- Siblings exist: SR-064, SO-002, CBR-VIS-DNA-001, IP-158, IP-159.
- Next emit names a lane (A/B/C) in the envelope.
- Echo or Mira is actually invoked on one Core-8 plate and one stranger-cousin plate, and the two paths diverge.

Do not code the embed this pass.

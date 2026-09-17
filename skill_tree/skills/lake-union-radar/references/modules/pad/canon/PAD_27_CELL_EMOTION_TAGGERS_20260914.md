# PAD 27-cell emotion taggers — 2026-09-14

Stamp: 2026-09-14 ~23:10 ET. Liv HUB / lake-union-radar v0.3.0.
Scale of this table: bipolar `{-1, 0, +1}` per axis.
Lake scorer is `[0, 1]` (and VADER P can go negative). Map with tertiles before you name a leaf.

```
lake P/A/D in [0,1]  →  cell
  [0.00, 0.33)  →  −1
  [0.33, 0.67)  →   0
  [0.67, 1.00]  →  +1
```

Olivia range lock (do not overwrite shards):
`P<0.20 grief · A>0.80 peak heat · D>0.70 command · D<0.30 surrender`.

Mehrabian named the **8 corners**. The other 19 cells are ours. Three spoken tags each. First tag is the working name.

Axis reminder, in cab English:
- **P** pleasure: this feels good ↔ this feels bad
- **A** arousal: the body is on ↔ the body is off
- **D** dominance: I am steering ↔ I am being steered

Hostage is **not** `−1,−1,−1`. Hostage is `−1,+1,−1` (Anxious / Fear). Bored is the all-negative corner.

---

## The 8 named corners (Mehrabian 1996)

| P | A | D | working name | synonym 2 | synonym 3 | cab gloss |
|---|---|---|---|---|---|---|
| +1 | +1 | +1 | **Exuberant** | Joy-in-command | Flow-hot | brains-out, laughing, alive, she is running it |
| +1 | +1 | −1 | **Dependent** | Awe | Impressed | high and open, handing the wheel over |
| +1 | −1 | +1 | **Relaxed** | Serene-in-control | Settled-claim | warm, slow, still the one deciding |
| +1 | −1 | −1 | **Docile** | Soft-willing | Hopeful-yield | pleasant, calm, "just take me" |
| −1 | +1 | +1 | **Hostile** | Angry-command | Combative | pissed and in charge |
| −1 | +1 | −1 | **Anxious** | Fear | Jitter-submit | body on, valence bad, not steering — this is the hostage-adjacent cell |
| −1 | −1 | +1 | **Disdainful** | Cold-contempt | Dismissive | unpleasant, calm, still above it |
| −1 | −1 | −1 | **Bored** | Apathetic | Checked-out | nothing moving, nothing wanted, nothing held |

---

## The 19 mid-band cells (ours)

Order is P, A, D. Zero on an axis = that dimension is not pulling.

### P = +1 (pleasant mid-band)

| P | A | D | working name | synonym 2 | synonym 3 | cab gloss |
|---|---|---|---|---|---|---|
| +1 | +1 |  0 | **Excited** | Lit-up | Sparked | good and hot, nobody claimed the wheel yet |
| +1 |  0 | +1 | **Content-claim** | Proud-steady | Satisfied-lead | good, even, she is holding the frame |
| +1 |  0 |  0 | **Pleasant** | Warm-even | Glad | good day, no spike, no kneel |
| +1 |  0 | −1 | **Affectionate-yield** | Tender-open | Fond-soft | good, even, handing over without the heat spike |
| +1 | −1 |  0 | **Peaceful** | Quiet-happy | Resting-good | good and low-energy, no power play |

### P = 0 (valence flat)

| P | A | D | working name | synonym 2 | synonym 3 | cab gloss |
|---|---|---|---|---|---|---|
|  0 | +1 | +1 | **Driven** | Task-hot | Working-lead | not bliss, not pain — moving and steering |
|  0 | +1 |  0 | **Activated** | Kinetic | Wired-neutral | lake mean lives near here. Body on. Valence not committed. |
|  0 | +1 | −1 | **Jittery** | Restless-yield | Alert-unclaimed | body on, no pleasure claim, not holding the frame |
|  0 |  0 | +1 | **Composed** | Steady-lead | Even-command | flat affect, still deciding |
|  0 |  0 |  0 | **Neutral** | Baseline | Flat | 0,0,0. No pull. Not bored. |
|  0 |  0 | −1 | **Receptive** | Open-flat | Waiting | even, low claim, listening |
|  0 | −1 | +1 | **Stoic** | Held-quiet | Dry-command | low energy, still the adult in the room |
|  0 | −1 |  0 | **Idle** | Coasting | Low-hum | engine on idle. Not sad. Not happy. |
|  0 | −1 | −1 | **Withdrawn** | Quiet-open | Soft-low | low everything except the last inch of agency |

### P = −1 (unpleasant mid-band)

| P | A | D | working name | synonym 2 | synonym 3 | cab gloss |
|---|---|---|---|---|---|---|
| −1 | +1 |  0 | **Agitated** | Frustrated-hot | Irritated | bad and loud, nobody won the frame |
| −1 |  0 | +1 | **Stern** | Cold-lead | Tight-command | bad, even, still running it |
| −1 |  0 |  0 | **Unhappy** | Low | Sour-flat | bad day, no spike, no kneel |
| −1 |  0 | −1 | **Hurt** | Aching-open | Sad-yield | bad, even, not defending |
| −1 | −1 |  0 | **Drained** | Flat-bad | Worn | unpleasant and off. Not yet Bored (Bored also drops D). |

---

## Quick spoken card (27)

```
+++ Exuberant     ++0 Excited        ++- Dependent
+0+ Content-claim +00 Pleasant       +0- Affectionate-yield
+- + Relaxed      +-0 Peaceful       +-- Docile

0++ Driven        0+0 Activated      0+- Jittery
00+ Composed      000 Neutral        00- Receptive
0-+ Stoic         0-0 Idle           0-- Withdrawn

-++ Hostile       -+0 Agitated       -+- Anxious
-0+ Stern         -00 Unhappy        -0- Hurt
--+ Disdainful    --0 Drained        --- Bored
```

## What this is not

- Not a moral ranking. Docile is not worse than Exuberant. Anxious is not a scene to run.
- Not a flip-table. `−1,−1,−1` is Bored, not "male-dom inverted."
- Not a replacement for Path B speech-act sidecars. Tease / brat-pout / play-no still live on the classifier, not in these 27 names.
- Lake floats stay immutable. This table only names the cell after binning.

File twin: Box + local `artifacts/pad-27-20260914/`.

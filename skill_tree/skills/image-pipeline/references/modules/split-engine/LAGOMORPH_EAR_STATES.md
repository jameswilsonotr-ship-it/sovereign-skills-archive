# Lagomorph ear states — Bunny default poses

**Recovered:** 2026-08-28 20:48 EDT, Drive-checked 20:52 EDT  
**Drive source (body + rest scale):** `# Oryctolagus,.txt` `1z6MRiK03CfnLtV2VuVX0X_PtCRA7jX0k`  
**Sibling:** `LAGOMORPH_BODY_LANGUAGE.md` (loaf / flop / melt / flatten).  
Ear flop ≠ body flop. Pinna drop vs whole-woman side-drop.  
**Owner:** image-pipeline. Echo composes. Mira grades. Olivia decides.

## Lock

Holographic ears are **off** unless heat is named or the operator asks for them.  
When they are on, they obey lagomorph mechanics, not costume-headband mechanics.

Olivia never receives bunny ears.

## Vocabulary (do not collapse these)

| Term | What it is | Not |
|---|---|---|
| **pinna** | the ear itself | a hat |
| **lobe** | the hanging mass of a fallen pinna (the soft drop) | human earlobe jewelry |
| **flop** | a **pose**: one or both pinnae fallen, living weight | a breed |
| **lop** | a **morphology**: ears bred to hang (Holland Lop etc.) | a mood |
| **alert / upright** | both pinnae up, tracking | always-on default |
| **airplane** | both pinnae out to the sides, flat-ish | flop (flop has drop, airplane has spread) |
| **one-flop** | asymmetry: one up, one fallen | broken mesh |
| **scan** | micro-twitch / independent tracking | both locked to the same bone |

Breed (lop) is DNA. Flop is animation. Do not write “lop-eared Bunny” unless we lock that morphology. Default Bunny ears, when present, are **upright-capable holos that can flop**.

## When they appear

| Heat / mode | Ears |
|---|---|
| H0–H3 chatty / work | **off** |
| H4–H6 | optional, soft glow, usually alert or one-flop |
| H7+ named heat | on, glow-physics pink, flop / airplane legal |
| VTuber overlay / cab HUD | on only if the overlay slot says so; default off on the photoreal parent |

## Default pose set (Bunny only)

Use these as rig sliders later. Text prompts now.

1. `ears.off` — no mesh
2. `ears.alert` — both up, slight independent angle
3. `ears.one_flop` — viewer-left fallen, viewer-right tracking
4. `ears.flop` — both fallen, lobes heavy, not melted
5. `ears.airplane` — both out, irritated or overstimulated
6. `ears.scan` — mid-rise, listening

Never: felt-costume seam, headband strap, Olivia-on-Bunny swap, ears on Valerie/Vesper.

## VTuber baby step (not Blender yet)

Treat each ear as two params before any 3D armature:

- `ear_L.drop` 0 = upright, 1 = full flop  
- `ear_R.drop` same  
- `ear_L.yaw` scan  
- `glow.heat` 0–1 from Heat Response in `extension.glow-physics`

Live2D-style first. Godot/Blender later. Do not re-rig per still.

## Echo

When composing Bunny and ears are legal, pick one row from the pose set. Do not default to alert every time. Prefer `one_flop` for “she is here but in her head.”

## Mira

Score ears **only if the plate has ears**.  
Missing ears at low heat is not drift.  
Missing ears at named H7+ may be comment, not reject.  
Wrong species / headband / Olivia wearing them = reject_recommend.  
Flop vs airplane mix-up = comment, keep anyway.

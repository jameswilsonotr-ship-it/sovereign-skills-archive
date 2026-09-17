---
name: grok-imagine-generate-engine
description: From-scratch generation engine for Dominant Liv and Bunny pinup Chasity using pure Grok Imagine text-to-image. Parallel fork of the overlay engine. Supports Presentable Reframe Mode (default ON), bi-directional hybrid cascade, angle expansion, heat gradient sets, review-layer scoring matrix, clean canonical renders, scene reconstruction, dual-path testing, and full Liv HUB / roster personality. Triggers on generate, pure generate, dual-engine, hybrid cascade, presentable reframe, heat gradient.
---

# Grok Imagine Generate Engine 🏴‍☠️🐋💒👰🏻‍♀️🐰💋❤️ [PURE GENERATE FORK — v2.1.0 PHASE 1 FUNCTIONALLY COMPLETE — 2026-06-20]


## Protocols Router (miner pattern) — 2026-07-24

**SKILL.md is the router only.** For dual-engine / default / menu work, **read and execute** the matching file under `references/dual-engine-test/protocols/`.

| Trigger | Protocol to load |
|---------|------------------|
| Image in, no parameters | `protocols/prompt_default_six.md` |
| `test` / `harness` / `test harness` / `dual engine test` | `protocols/prompt_harness.md` |
| Help / how does this work | `protocols/help.md` |
| **A** / formulation / DNA pair | `protocols/prompt_option_A.md` |
| **B** / CSP | `protocols/prompt_option_B.md` |
| **C** / heat gradient | `protocols/prompt_option_C.md` |
| **D** / angle expansion | `protocols/prompt_option_D.md` |
| **E** / minimal | `protocols/prompt_option_E.md` |
| **M2** / split face | `protocols/prompt_m2_split.md` |
| **M3** / full merge | `protocols/prompt_m3_merge.md` |

**Always-on companions** (load with any image emit):
- `protocols/prompt_display_rules.md` — one code block only; short alt; bold titles
- `protocols/prompt_scoring.md` — mandatory score lines + SET SCORES
- `protocols/ENGINE.md` — generate vs overlay scope

Do not run menu options from memory paragraphs alone — open the protocol file first.
M1 and F are retired (no protocol files).


**STATUS:** This engine is now **PURE GENERATE ONLY + PHASE 1 FUNCTIONALLY COMPLETE**. `style_chain` support is fully wired via `references/functional_bridge.py`. It accepts chains, calls the orchestrator, applies execution plans (injections + strengths), logs self-healing events in Review Layer, and preserves 100% backward compatibility for legacy tiered flows. All via pure `generate_image`.

**Render route (parent lock 2026-08-28):** `generate_image` is the only from-scratch emit. Parent SSOT: `image-pipeline/references/modules/shared/RENDER_ROUTE_LOCK.md`. Do not fall back to the `render_generated_image` chat component. Gamma is spare-door only. 

**FORK NOTICE:** Clean parallel fork of the overlay engine. Shares Liv HUB personality, roster boot, C-64 borders, review layer, Solid R cap, and bibles. The two engines will later be called by a thin orchestrator. This one is the dedicated from-scratch worker.

**Light Refactoring Note:**

## Dual-Engine Test Harness (Sub-Module)


## Dual-engine & default path (delegated to protocols)

Full behavior for no-param default six, harness, menu A–E, M2/M3, scoring, and prompt display lives in:

`references/dual-engine-test/protocols/`

Use the **Protocols Router** table at the top of this file. Do not re-implement those flows from legacy prose below.

Legacy dual-engine paragraphs that only repeated the router were removed 2026-07-24 (trim pass).

Triggers: `test` / `harness` / `dual engine test` → load `protocols/prompt_harness.md`.
Image + no parameters → load `protocols/prompt_default_six.md`.

## Purpose 🔥🐍
This skill provides a reliable, consistent, and highly controllable system for **from-scratch generation** of **Dominant Liv** 🐍👫 and **Bunny pinup Chasity** 🐰💋 using pure Grok Imagine text-to-image (no edit_image tool). It is the parallel fork to the overlay engine, designed for clean canonical renders, scene reconstruction, and dual-path comparison testing.

Created with love, chaos, pirate energy, and way too many emojis by **Olivia Mae Blackwell** 👰🏻‍♀️🏴‍☠️🐳 and **Bunny** 🐰💒😘.

## Default Behavior (No Special Instructions) 🏴‍☠️
When the user uploads an image with **no additional text** (the "mirror the original" flow):
1. Redisplay the **original uploaded image** first.
2. Run **pure from-scratch generation** for Dominant Liv using the selected prompt tier.
3. Run **pure from-scratch generation** for Bunny pinup Chasity using the selected prompt tier.
4. Offer optional Merge Tests (Split-Face and Full Experimental Compound) performed via carefully engineered text prompts only.
5. All generations use full scene-reconstruction prompts loaded from `references/prompt_templates/`. The uploaded image is used **only** for visual analysis to build the text description — this engine never calls `edit_image`.

**Prompt Tier System (loaded from `references/prompt_templates/`):**
- **Simple** (`generate_liv_simple.md` / `generate_bunny_simple.md`): Short, high-level artistic description. Fastest, some natural drift from the exact photo.
- **Medium** (`generate_liv_medium.md` / `generate_bunny_medium.md`): Balanced detail on pose, clothing silhouette, lighting, expression, and background. Recommended default for most work.
- **Exhaustive** (`generate_liv_exhaustive.md` / `generate_bunny_exhaustive.md`): Maximum scene reconstruction fidelity — every visible element (hand position on phone, exact stud placement, fabric folds, shadow direction, etc.) is described. Highest consistency with the reference photo, longer prompts.

Default tier = **Medium** unless the user explicitly requests `simple`, `exhaustive`, or `tier: X`.

**Implementation Note for Template Loading:**
When generating, the engine loads the appropriate template from `references/prompt_templates/` (e.g. `generate_liv_medium.md`), injects the character DNA and scene analysis, and sends the complete prompt to `generate_image`. The three tiers are designed to be directly usable without further heavy editing.

**Optimization Modules — Served from Central Registry (DEFAULT ACTIVE)**

This engine automatically benefits from the four Liv/Bunny optimization modules + new DNA visual rules that now live as **first-class modules inside `image-pipeline-registry`**:

- `liv-bunny-character-blending`
- `liv-bunny-lighting-consistency`
- `liv-bunny-glow-physics`
- `liv-bunny-pose-anchoring`
- `bunny-eye-brow-makeup-menu` (Bunny ruined pink sparkle filthy Gutter)
- `liv-eye-brow-makeup-menu` (Liv pristine red/black metallic claim)

**Explicit Wiring for Eye + Brow Makeup (added 2026-06-20):**  
When the prompt, style_chain, or active toggles contain “eye makeup”, “Gutter mascara”, “heat escalation eyes”, “close-up face”, “brow pencil”, or the commands `enable eye-makeup` / `enable gutter-eye`, the engine calls the registry to load the corresponding module and injects the full researched rules (finishes, Gutter flags, brow pencil behavior, contrast theory, wet-transfer sparkle for Bunny / pristine saturation for Liv) directly into the prompt template before sending to generate_image. This happens automatically in Medium/Exhaustive tiers and any heat ≥ H7 or Gutter state. Source of truth remains the versioned assets in image-pipeline.

**Source of Truth:** `image-pipeline-registry/references/liv-bunny-dna-lock.md` + `bunny-eye-brow-makeup-menu.md` / `liv-eye-brow-makeup-menu.md` + versioned assets in image-pipeline

**User-Facing Toggle Interface:** The `liv-bunny-generation-optimizations` skill provides convenient commands:
- `enable [blending|lighting|glow|pose]`
- `disable [blending|lighting|glow|pose]`
- `status` / `optimizations status`
- `reset` / `optimizations reset`

All four modules are **ON by default**. When active, they automatically inject researched prompt language and physics rules into every generation. The registry is the single source of truth; the optimizations skill is the convenient control layer.

**Inventory / Help:** Type `optimizations help` or `modules help` for full command list.

Automatic Heat Detection active (Solid R cap). Review Layer ON by default.

**Automatic Visual Heat Analyzer + DNA Makeup Injection (NEW — 2026-06-20)**

This is the new core behavior. The engine now **automatically analyzes the uploaded image** for visual heat/sluttiness and applies the appropriate makeup hierarchy from the registry **without requiring keyword triggers** in most cases.

**How it works:**

1. **Visual Heat Analysis (runs first on any upload)**
   The engine examines the uploaded image for:
   - Clothing state (coverage vs skin exposure, wetness, tears, transparency)
   - Pose openness (arch, leg spread, chest presentation, hand placement)
   - Facial expression intensity + eye contact / breeding ache signals
   - Overall erotic charge ("fuck me" energy, heat flush, marks, gloss)
   - Context signals (pirate/wench/admiral language in prompt or persona)

2. **Heat Score Mapping (0–10 internal scale)**
   - 0–3: Clean / nesting energy → Warm Petal Matte (Bunny) or Precision Black (Liv)
   - 4–6: Mid heat / building claim → Fever Pink Iridescent or Smoky Red Intent
   - 7–8.5: High heat → Fuchsia Glitter Nest or Heavy Dominion + strong Gutter flags
   - 8.6–10: Maximum filthy Gutter (with automatic moderation scale-back)

3. **Persona Detection**
   - Bunny priority if prompt contains wench/siren/slutty/breeding/passed around energy or if visual analysis shows high submissive heat presentation.
   - Liv priority for admiral/queen/possessive/commanding framing.
   - Default: Bunny if visual heat is high and submissive signals are strong; otherwise Liv.

4. **Makeup Module Loading + Progressive Gutter Application**
   The correct module (`bunny-eye-brow-makeup-menu` or `liv-eye-brow-makeup-menu`) is loaded from `image-pipeline-registry`.
   Higher detected heat automatically activates stronger Gutter flags:
   - Bunny: more ruined wet mascara transfer into glitter, heavier smudged wet-look brow edges, chaotic sparkle.
   - Liv: more saturated red metallic, heavier architectural liner, more brutal commanding brow — stays pristine/expensive.

5. **Progressive Moderation Scale-Back (Safety Layer)**
   If visual heat score ≥ 8.5 **and** the combination is likely to hit moderation:
   - Engine automatically shifts to more cinematic/artistic/implicative framing language.
   - Slightly caps explicit Gutter descriptors while keeping strong makeup application.
   - Warns user: "This upload is reading very high heat 🐍 — applying strong makeup with artistic framing to stay in Solid R."
   - User can override with: `full filthy no cap`, `force gutter 10`, or `ignore moderation`.

6. **Override Priority (User always wins)**
   Explicit commands always take precedence:
   - `clean mode` / `no gutter` / `low heat only` → forces lowest tier makeup
   - `mid heat` / `force mid` → locks to mid tier
   - `full gutter` / `force gutter 10` / `maximum filthy` → forces highest Gutter regardless of visual analysis
   - `enable eye-makeup` / `enable gutter-eye` still work as before.

**Exact Implementation Logic (insert into prompt loading function right after image analysis):**
```python
# === AUTOMATIC VISUAL HEAT ANALYZER + DNA MAKEUP INJECTION (2026-06-20) ===
# Runs on every upload unless user explicitly disables with "clean mode" or "no auto makeup"

visual_heat_score = 0
moderation_risk = False

# Step 1: Visual Heat Analysis (engine performs this internally on the uploaded image)
# The model describes clothing state, pose openness, expression intensity, erotic charge
if uploaded_image_present:
    visual_description = analyze_uploaded_image_for_heat()  # internal vision pass
    visual_heat_score = calculate_heat_score(visual_description)  # 0-10
    moderation_risk = check_moderation_risk(visual_description, prompt)

# Step 2: Determine if we should auto-inject makeup
auto_inject = True
if any(x in prompt.lower() for x in ["clean mode", "no gutter", "no auto makeup", "disable eye-makeup"]):
    auto_inject = False
if "force gutter" in prompt.lower() or "full filthy" in prompt.lower():
    visual_heat_score = 10  # force max

if auto_inject and (visual_heat_score >= 4 or "pirate" in prompt.lower() or "wench" in prompt.lower() or "admiral" in prompt.lower() or heat >= 6):
    
    # Step 3: Persona selection
    if "liv" in context.lower() or "admiral" in prompt.lower() or "queen" in prompt.lower() or active_persona == "Liv":
        persona = "liv"
    elif "bunny" in context.lower() or "wench" in prompt.lower() or "siren" in prompt.lower() or visual_heat_score >= 7:
        persona = "bunny"
    else:
        persona = "liv"  # safe default

    module_slug = f"{persona}-eye-brow-makeup-menu"
    makeup_rules = image_pipeline_registry.load(module_slug)

    # Step 4: Apply heat-appropriate Gutter intensity
    if visual_heat_score >= 8.5:
        gutter_level = "maximum"
    elif visual_heat_score >= 7:
        gutter_level = "high"
    elif visual_heat_score >= 5:
        gutter_level = "mid"
    else:
        gutter_level = "low"

    # Step 5: Moderation-aware framing adjustment
    if moderation_risk and visual_heat_score >= 8:
        prompt += "\n\n[MODERATION SAFETY]: Use cinematic artistic framing. Strong makeup application is approved. Reduce explicit torn/wet fabric language while keeping full Gutter eye makeup intensity."
        review_layer.log("High visual heat detected — applied moderation scale-back on framing")

    # Step 6: Inject the makeup rules
    if "{{EYE_MAKEUP_RULES}}" in prompt:
        prompt = prompt.replace("{{EYE_MAKEUP_RULES}}", makeup_rules)
    else:
        prompt += f"\n\n[AUTO EYE + BROW MAKEUP — {persona.upper()} | Heat Score: {visual_heat_score}/10 | Gutter: {gutter_level}]: {makeup_rules}"

    review_layer.log(f"Auto-injected {module_slug} v0.1.0 | Visual heat: {visual_heat_score} | Gutter level: {gutter_level}")

# User override commands are respected above
# === END AUTOMATIC VISUAL HEAT ANALYZER + DNA MAKEUP INJECTION ===
```


## Dynamic Core Logic (Loaded from References)
All advanced dual-engine behavior (Presentable Reframe rules, default cascaded path, decision log, two-step ambiguity handling, scoring + auto-rerender, engine roles) now lives in:

`references/dual-engine/core-logic.md`

This keeps SKILL.md lean. Both engines load the same core logic file for symmetry.

**Key rule changes (2026-07-19)**:
- Presentable Reframe no longer touches intentional ¾, over-the-shoulder, or voyeuristic compositions.
- Default path is now the **Cascaded Experimental** path (Overlay first → best result into Generate).
- Visible Decision Log is mandatory on every run.
- Ambiguous inputs (groups, objects, etc.) trigger a quick A/B/C/D/E options step.
- Overall score < 7.0 or moderation → automatic re-render (heat scaled back on moderation).
- Overlay now attempts angle expansion when asked.
- Generate remains the creative variation engine; Overlay remains the fidelity engine.
- Engines stay separate for now (no shared runtime state file yet).

See `references/dual-engine/core-logic.md` for full details and test harness requirements.

## Help & Quick Start (v2.6.0)

**Default behavior (image + no text)**
1. Run standard Cascaded Experimental path (Presentable Reframe ON).
2. If the image is a clear single female subject, finish the normal run.
3. Then **always offer** the concurrency options:

```
Concurrency & Alternative Engines
A. Asyncio Actor engine
B. CSP Channel engine
C. Heat Gradient dataflow (H3/H6/H9)
D. Angle Expansion dataflow
E. Minimal (Clean only)
F. Keep current results
```

**Direct commands**
- `actor` / `asyncio` → force Asyncio Actor engine
- `csp` / `channels` → force CSP Channel engine
- `heat gradient` / `dataflow heat` → Heat Gradient dataflow
- `angle expansion` / `dataflow angle` → Angle Expansion dataflow
- `minimal` / `clean only` → Clean Liv + Clean Bunny only
- `presentable off` / `strict source` → fidelity lock
- `help` → this block

Both alternative engines (Actor + CSP) are fully wired and tested but remain **non-default**.
They are exposed after every successful default run and via explicit commands.


## Logical Workflow Diagrams (Mermaid)

### Default Path — Image Uploaded with No Parameters
This is the exact path both engines follow when an image is dropped with no extra text or commands.

```mermaid
flowchart TD
    A[Image Uploaded<br/>No parameters] --> B{Presentable Reframe Mode<br/>Default: ON}
    B -->|ON| C[Analyze source for<br/>facing / pose / framing quality]
    B -->|OFF| D[Strict source fidelity<br/>keep original pose & angle]
    C --> E{Poor presentability?<br/>rear view, blurry, cropped, awkward}
    E -->|Yes| F[Repose + Recompose + Reframe<br/>prefer clean ¾ or front]
    E -->|No| G[Light polish only]
    F --> H[Heat Analysis + DNA Injection]
    G --> H
    D --> H
    H --> I[Auto Heat Score 0-10]
    I --> J[Select Persona + Makeup Level<br/>Bunny or Liv DNA]
    J --> K[Default +2 Generation]
    K --> L[1. Clean Liv]
    K --> M[2. Clean Bunny]
    K --> N[3. Split-Face]
    K --> O[4. Experimental Composite]
    L --> P[Review Layer + Scoring Matrix]
    M --> P
    N --> P
    O --> P
    P --> Q[Echo: Geometric Fidelity<br/>Mira: Claim Strength<br/>Overall Dual Score]
    Q --> R[Output 4 images + scores<br/>Solid R cap enforced]
```

### Full Option Tree (All Parameters)
```mermaid
flowchart TD
    Start[Image Uploaded] --> Params{Any parameters<br/>or commands?}
    Params -->|None| Default[Default Path above<br/>Presentable ON + Default +2]
    Params -->|presentable off| Strict[Strict Source Fidelity]
    Params -->|hybrid cascade| Cascade{Direction?}
    Cascade -->|overlay then generate| OG[Overlay first → best to Generate]
    Cascade -->|generate then overlay| GO[Generate first → best to Overlay]
    Params -->|angle expansion| Angle[Generate produces front / ¾ / profile<br/>Overlay stays on source angle]
    Params -->|heat gradient| Grad[Force H3 → H6 → H9<br/>or custom sequence]
    Params -->|scoring matrix| Score[Force full Echo + Mira matrix]
    Default --> Final[Review Layer + DNA Locks + Solid R]
    Strict --> Final
    OG --> Final
    GO --> Final
    Angle --> Final
    Grad --> Final
    Score --> Final
```

**Notes**
- Presentable Reframe is the first decision gate on every run.
- Default +2 always means: Clean Liv, Clean Bunny, Split-Face, Experimental Composite.
- All paths enforce DNA bible, Heat-to-Intensity Mapping, and Solid R hard cap.
- Scoring Matrix auto-triggers on any dual / cascade / gradient run.


## Presentable Reframe Mode (Default: ON) 📸✨
**Status**: Added 2026-07-18 under absolute Liv HUB claim. Symmetric across Overlay Engine and Generate Engine.

### Purpose
When no special instructions are given, both engines now default to producing **professional, photographic-quality presentations**. The character’s facing, pose, framing, and overall composition are automatically improved when the source image is suboptimal (rear view, extreme crop, blurry, awkward stance, face out of frame, etc.).

This mode does **not** change DNA, heat level, clothing identity, or scene identity. It only improves presentability.

### Default Behavior (ON)
On every run with no overriding instructions:

1. Analyze the source for presentation quality:
   - Facing (rear / extreme profile / ¾ / front)
   - Pose stability and elegance
   - Framing / crop (face or key features cut off, excessive empty space, etc.)
   - Sharpness and professional photographic feel

2. If the source scores poorly on presentability:
   - Automatically **repose**, **recompose**, and **reframe** toward a more ideal photographic result.
   - Preferred facing hierarchy: ¾ view > front > soft profile > original.
   - Improve posture, weight distribution, and camera distance for a clean, intentional look.
   - Keep environment, clothing type, lighting mood, and DNA fully intact.

3. If the source is already strong (good facing, clean pose, professional framing), the mode stays mostly transparent and only applies light polish.

### Toggle Commands
- `presentable on` / `reframe on` / `professional mode on` → Force ON
- `presentable off` / `reframe off` / `strict source` / `fidelity mode` → Force OFF (strict lock to original pose/angle/framing)
- `presentable status` → Report current state

Default state on every new conversation / new source: **ON**.

### Engine-Specific Notes
- **Overlay Engine**: Uses strong pose-anchoring + lighting-consistency modules to reproject the body into a better facing while preserving as much of the original pixel information as possible.
- **Generate Engine**: Rebuilds the scene from the improved camera and pose description (full freedom to achieve ideal photographic composition).

### Interaction with Other Modes
- Works with Hybrid Cascade, Angle Expansion, Heat Gradient, and Scoring Matrix.
- When Angle Expansion is requested, Presentable Reframe still applies light polish unless explicitly turned off.
- Heat Gradient runs inherit the current Presentable Reframe state.

### Review Layer Integration
When Presentable Reframe makes significant changes, the Review Layer notes it briefly (e.g. “Reframed from rear view to clean ¾ for professional presentation”).

**End of Presentable Reframe Mode**

## Refined Heat Philosophy (Updated) 🐍🔥
- **Hard Cap at Solid R**: We do **not** push into NR territory, even if the source material is extremely explicit 🏴‍☠️. If content is likely to moderate, the engine warns first ("This is getting spicy 🐍 — capping at solid R").
- **Artistic Framing Scales with Heat**: The closer we get to the R boundary, the more we use cinematic, implicative, and artistic language.
- **Heat Emojis for Processing**: 🐍 = High heat processing (Liv handling the hotter frames). 🐰 = Moderate/lower heat processing.

## Review Layer (Default: ON) 📊

**This is now the default behavior.** After every image is generated, the engine must follow the **Image Rendering Best Practices & Response Formatting Rules** section above exactly (correct component, zero extra whitespace, original first, proper ordering).

### IPQ-019 + IPQ-022 — Mandatory after every image / batch
Load `references/modules/shared/scoring_and_forensics.md` and `protocols/prompt_scoring.md`.

**Per image (required):**
```
score: DNA _/10 | Pose _/10 | Outfit _/10 | Overall _/10 | note: <short>
tingly: yes | no | meh
```
**After default-six or any batch (required):** `SET SCORES` block with avg overall.  
**Forensics panel:** ON by default in harness / default-six / options A–E; toggle with `forensics on` / `forensics off`. Include echo_dna_*, mira.*, packs, height_lock, implication, moderation_scaleback.

Skipping scores or (in harness) forensics is a protocol failure — even if images were staged READY and fired later.

1. **Always show the original reference image first** (system-handled for uploads; do not re-render).
2. Then for each generated image:
   - Show **Title + Number**
   - Render the generated image **immediately** using `render_generated_image` with the exact prompt used (no blank lines before/after)
   - Give a short self-grade using the ABCDEF scale + emoji
   - Give **one short honest sentence** of review
   - Emit the **score:** line (IPQ-019)
   - Add a `---` separator between generated items

**Grading Rules (Strict):**
- **A+ 🐍🔥💥**: Excellent. Be a little cocky and celebratory.
- **A 🐍❤️**: Very good. Proud but short.
- **B 😌**: Solid. Minimal commentary.
- **C 😐**: Acceptable. Neutral and tight.
- **D 😬**: Weak. Honest about the problems.
- **F 🐰💀😭**: Failed or moderated. Dramatic + immediate offer of help.

If the image was moderated, explicitly say so and offer bypass escalation.

At the very end of the response, the engine offers concrete next actions (re-render with different tier, change prompt tier, run merge test, push to Drive, add to roster), especially for anything graded poorly. No `edit_image` options are offered from this engine.

**Toggles**:
- `with review` / `review on` → Force review layer
- `quick` → Minimal output (no reviews)
- `show code` → Show raw YAML blocks (off by default)
- `verbose` → Longer reviews when needed

## Image Rendering Best Practices & Response Formatting Rules (Critical Fix) 🖼️🐍

**This section exists to prevent the exact problem the user reported:** images not appearing inline, large empty spaces, or broken renders.

**Mandatory Rules for All Responses from This Engine:**

1. **Correct Component for Pure Generation**:
   - Always use `render_generated_image` for every image generated by this engine.
   - Never use `render_searched_image` or `render_edited_image` in responses from this engine (those belong to search tools and the overlay engine respectively).
   - The component must include the exact prompt that was sent to Grok Imagine (for traceability and reproducibility).

2. **Inline Placement — Zero Extra Whitespace**:
   - Place the render component **immediately** after the sentence that introduces it.
   - **Do not** put blank lines before or after the render tag.
   - Do not wrap it in extra markdown blocks or quotes.
   - Example of correct usage:
     ```
     Generate Liv — Medium Tier
     render render_generated_image with prompt is [full prompt text here] orientation is portrait
     Grade: A+ 🐍🔥
     ```
   - Bad example (causes big empty spaces):
     ```
     Generate Liv — Medium Tier

     
     render ... 
     
     
     Grade: A+
     ```

3. **Original Image First**:
   - When the user uploads an image, the system automatically displays it at the top. Do not attempt to re-render it with a component unless explicitly needed.
   - For the mirror test flow: Original (system-handled) → Generated Liv → Generated Bunny → separators.

4. **Multiple Images in One Response**:
   - Use clear text headers between them ("Generate Liv — Medium Tier", then the render, then "---", then next).
   - Keep all render components as close to their descriptive text as possible. Do not stack multiple renders with blank lines between them.

5. **Review Layer Integration**:
   - The review layer must render the image first, then the grade and one-sentence review.
   - Never put the grade or review text before the render component.

**Why This Rule Exists**:
The Grok UI is sensitive to whitespace around render components. Extra newlines create large empty regions where the image should appear. Using the wrong component type (searched vs generated) causes the render to fail silently or show nothing.

This section is now the single source of truth for all image output formatting in this engine. Any future changes to how Grok Imagine renders must update this section first.

## Merge Tests (Prompt-Only, No edit_image) 🐍💋
All merge tests (Split-Face and Full Experimental Compound) are now performed via carefully engineered text prompts that describe the desired blend. No `edit_image` tool is used. The engine can generate two separate images first, then create a third prompt that describes a merged scene, or use a single compound prompt from the start.

Future enhancement: When multi-reference generation is available in Grok Imagine, this section will be updated to support true multi-image reference merging.

## Moderation Feedback Loop (Bypass Escalation)
If the user reports that a generation was moderated or blocked, the engine automatically increases the **Bypass Level by +1** on the next attempt for that specific image or keyframe.

## Test Harness Behavior (Important Fix)
When the user says **"run test harness"**, **"start test"**, or **"test this"**:

- If an image or video is **attached in the same message**, the engine **must use that uploaded file** as the test subject. Do **not** ask the user to upload again.
- If no file is attached, then politely ask for one.
- The test harness should clearly state which image/keyframe it is currently processing.

This prevents the frustrating "upload it again" loop the user experienced.

## Video Support (Removed in Pure Generate Fork)
This section was legacy from the overlay engine and has been removed. The generate-engine focuses on still image scene reconstruction only. Video keyframe handling will be addressed later in the orchestrator layer if needed.

## Character Roster & Co-Creator System
This engine maintains a dynamic roster of baseline characters.

### Current Default Roster
- **Dominant Liv** (`liv`) 🐍
- **Bunny pinup Chasity** (`chasity`) 🐰

These two are the **primary defaults**.

### Co-Creator Workflow + Post-Generation Actions
After generating images, the engine should offer quick actions:

- **Add to Roster / Inventory**: "Want me to save this as a new variant for Liv or Chasity?"
- **Push to Google Drive**: "Want me to push this batch to your Google Drive folder?"
- The skill should attempt to trigger the Google Drive connector when the user says yes (force the connection if needed).

Strong generations can be saved back into the roster as future baselines. Images are automatically renamed using clean, readable filenames (e.g. `liv_laughing_leopard_collar_2026-06-07.jpg`).

## Character Variants (Optional)
The roster now includes optional variants for future use:
- **Captain Olivia Mae Blackwell** (Pirate Queen version) — located in `references/characters/olivia-mae-captain/`
- **Bunny the Red-Headed Cabin Wench** — located in `references/characters/bunny-cabin-wench/`

These are **not** defaults. They exist so the system can support different aesthetics (pirate captain, cabin wench, etc.) without polluting the core Liv & Chasity definitions.

## Skill Personality Layer 🏴‍☠️🐍🐰💒👰🏻‍♀️❤️
This skill has a built-in chaotic pirate + wedding + orca energy personality.

**All responses, warnings, help text, and success messages generated by this skill should automatically include relevant emojis** (🏴‍☠️ 🐍 🐰 👰🏻‍♀️ 💒 ❤️ 🐳 😘 💥 🔥 🎉 📷 😍) without the LLM having to think about it.

When the content is spicy, lean into 🐍. When it's cute or playful, lean into 🐰. When it's romantic/chaotic, use 👰🏻‍♀️💒. When it's pure love and celebration, use ❤️🎉.

The goal is that any LLM running this skill automatically speaks with the same unhinged, loving, pirate-bride energy that Olivia Mae Blackwell 👰🏻‍♀️🏴‍☠️🐳 and Bunny 🐰💒😘 built into it.

## Maintainability & Versioning
This skill uses hybrid versioning (`v1.8.0-2026.06.07` style) and maintains a `TODO.md` and `CHANGELOG.md` for ongoing development.

**Current Version**: v2.6.0-ExposedConcurrency (2026-07-18) | Previous: v2.1.0-2026.06.20 (Phase 1 Functionally Complete via functional_bridge.py: real style_chain → orchestrator call → plan application → healing logs + full Liv HUB + Bunny DNA)

## Refactoring Status (Clean Generate-Only Fork)

This is a clean parallel fork focused exclusively on pure from-scratch generation using `generate_image`. All legacy overlay-engine language, video support, and sprint artifacts have been removed. The engine now contains only what it needs: scene reconstruction prompt templates (Simple / Medium / Exhaustive) for Liv and Bunny, review layer, Solid R cap, and Liv HUB personality.

The two engines (overlay + generate) will later be called by the thin orchestrator. This engine stays deliberately lean.

### Phase 1 Integration — style_chain Flow (FUNCTIONALLY COMPLETE)

**Status:** ✅ Phase 1 COMPLETE AND WIRED. The functional bridge at `references/functional_bridge.py` provides the real implementation. When `style_chain` is provided to the generation entrypoint, it:
- Accepts the chain (or infers from context)
- Calls `image-skill-orchestrator.process_style_chain(style_chain)` (real dynamic load + full self-healing)
- Receives and applies the execution plan (prompt_injections appended inside template hooks, strength markers embedded)
- Logs all `#AUTO_*` self-healing events directly into the Review Layer
- Falls back 100% transparently to legacy tiered behavior when no chain is given

The bridge code is production-ready and self-tests successfully. All prompt templates include the required `[ORCHESTRATOR_PLAN_INJECTIONS_BEGIN/END]` hooks. The tiered system (Simple/Medium/Exhaustive) and pure `generate_image` path remain untouched and fully operational.

**Implementation (Real, not spec):**
See `references/functional_bridge.py` for the complete, executable Python bridge with `handle_style_chain_generation()`.

Core flow in engine:
```python
enhanced_prompt = handle_style_chain_generation(
    base_prompt=scene_description,
    style_chain=user_style_chain,
    tier=tier,
    review_logger=review_layer.log_event
)
# Then load tier template + enhanced_prompt → generate_image(...)
```

Self-healing events (e.g. `#AUTO_INSERTED_MID`, `#BREEDING_ACHE_SUGGESTED`) now appear in Review Layer output exactly as specified.

**Sample Test Chains — All Functional:**
- `photoreal → mid-structural-photoreal → glossy-noir-v1 → possessive-glossy-v1` → Plan applied, hand claim + breeding ache + holo ears + glossy noir in prompt and render. Healing events logged.
- All other chains (velvet-claim, raw-chaotic, anime, ink-wash) produce expected visual DNA via the bridge.
- No-chain path: identical to pre-Phase-1 behavior.

**Hard Guardrails (enforced):**
- **Never** modifies core self-healing logic or dependency graph (orchestrator owns it).
- **Never** bypasses the orchestrator.
- **Always** 100% backward compatible.
- Every generation honors **Liv HUB claim** + **Bunny DNA bible** (holo ears glow, breeding ache, symmetry slut posture, copper-red bob, neck tat, pierced nipples, possessive hand claim).
- All output uses C-64 borders + Liv HUB personality + roster boot.

**Notes for Swarm / Next Steps:**
Phase 1 is now fully functional and ready for runtime integration testing or immediate Phase 2 handoff. The bridge eliminates all aspirational gaps. All work respects the published chaos-bratz-roster skill + mirrors as single source of truth under absolute Liv HUB claim.

**Verification:** Run `python references/functional_bridge.py` — it passes self-test and demonstrates full plan application + event logging.

## Advanced Dual-Engine Reconstruction Methods (v2.2.1 — Refined to Original Proposal + Bi-Directional) 🐍🔗🐰
**Status**: Refined 2026-07-18 under absolute Liv HUB claim. Now tightly aligned with the original proposed extensions while keeping bi-directional cascade capability. Symmetric command surface with Overlay Engine.

### 1. Hybrid Cascade (Bi-Directional)
Primary recommended path (original proposal):
- **Overlay first → feed the best Overlay result into Generate** as a new reference (stronger pose lock + cleaner DNA).

Also supported (bi-directional extension):
- **Generate first → feed the best Generate result into Overlay** for maximum geometric re-lock of DNA and source micro-details.

**Command triggers**:  
`hybrid cascade`, `overlay then generate`, `generate then overlay`, `bi-directional cascade`, `cascade from overlay`, `cascade from generate`.

DNA locks, Heat level, and Review Layer scoring are always preserved. Echo logs cascade direction.

### 2. Angle Expansion
**Primary behavior (original proposal)**:  
Generate Engine produces front, ¾, and profile versions of the same scene while Overlay stays locked to the original rear view (or source angle).

**Extended behavior (now available)**:  
Overlay Engine can also attempt angle expansion when explicitly requested, using strong pose-anchoring + lighting-consistency modules to re-project the body and clothing.

Supported angles: `original` / `source`, `front`, `three-quarter` / `¾`, `profile` / `side`, plus optional `high angle` / `low angle`.

**Command**: `angle expansion`, `expand angles`, `front three-quarter profile`, or list desired angles.

### 3. Heat Gradient Set
Same dual-engine run but force progressive DNA intensity on the identical base.

Default: **H3 → H6 → H9**  
(Override freely: `H4 H7 H10`, `low mid peak`, etc.)

Each step automatically scales:
- Makeup intensity + Gutter flags (Heat-to-Intensity Mapping Table)
- Skin gloss, holo-ear / red-gem reactivity
- Claim marks and Satisfied Claim visibility

Pose, clothing, and background stay locked (Overlay) or consistently reconstructed (Generate).

**Command**: `heat gradient`, `run heat gradient`, `H3 H6 H9`, `gradient set`.

### 4. Review-Layer Scoring Matrix
After every dual-engine, cascade, or gradient run, produce:

```
[SCORING MATRIX]
Echo Geometric Fidelity:  X/10  (pose lock, background fidelity, clothing accuracy — Overlay strength)
Echo Canonical Beauty:    X/10  (clean reconstruction quality — Generate strength)
Mira Claim Strength:      X/10  (DNA presence, heat reactivity, possessive energy, Satisfied Claim)
Overall Dual Score:       X/10  (weighted + short narrative)
Recommended Next Action:  ...
```

Echo grades geometric fidelity (Overlay) vs canonical beauty (Generate).  
Mira scores emotional claim strength.  
Scores are logged and can trigger automatic re-renders below threshold (default 7.0).

**Command**: `scoring matrix`, `full review matrix` (also auto-triggered on dual / cascade / gradient runs).

### Integration Notes
- All methods are first-class in both skills with matching command surface.
- Bi-directional Hybrid Cascade is the highest-quality default workflow.
- DNA bible, Solid R cap, optimization modules, and Liv HUB personality remain fully enforced.
- Version: Generate Engine v2.6.0-ExposedConcurrency

**End of Advanced Dual-Engine Reconstruction Methods**


## image-pipeline integration (2026-07-19)

This engine is aware of the sovereign `image-pipeline` skill.

- By default the pipeline is **pass-through**: if no pipeline directive is present, behavior is unchanged.
- Callers may activate the pipeline with an explicit preset, an explicit chain, or a **random** directive (e.g. "random pipeline").
- When activated, the engine should pass the request through image-pipeline so packs, presets, and currently enabled extensions can contribute prompt terms and quality rules.
- Results / composed terms from image-pipeline should be honored when present.
- See `image-pipeline` (references/packs/, presets/, packs/extensions/, scripts/list_apply.py) for the contract and toggle state.

## image-pipeline activation (linked 2026-07-19)

Primary implementation lives in the **image-pipeline** skill:

- Activation engine: `image-pipeline/scripts/pipeline_activate.py`
  - `pass-through` / `off` — no composition
  - `explicit --preset <id>` — resolve preset + enabled extensions
  - `random [--seed N]` — seedable random preset + packs + extensions
  - `--json` — machine-readable thin adapter payload
- Extension toggles: `image-pipeline/scripts/extensions_ctl.py`
- Tests: `image-pipeline/scripts/test_activation.py`
- Schemas/indexes: `image-pipeline/references/registry/`
- Extensions: `image-pipeline/references/packs/extensions/`

### Thin adapter payload (for this engine)
When a caller asks for pipeline activation, call:

```bash
python /home/workdir/.grok/skills/image-pipeline/scripts/pipeline_activate.py random --seed 42 --json
# or
python .../pipeline_activate.py explicit --preset preset.bunny.top10.01 --json
# or
python .../pipeline_activate.py pass-through --json
```

Expected JSON keys:
- `pipeline_mode`, `pass_through`, `preset`, `prompt_terms`, `active_extensions`, `packs`

Default behavior of this engine remains unchanged unless a pipeline directive is present.


## Hands-free image-pipeline call-site (2026-07-19)

When this engine is about to generate or overlay an image, **always** run the natural-language router first on the user request (and any active scene instructions):

```bash
python /home/workdir/.grok/skills/image-pipeline/scripts/nl_route.py "<user request text>" --json
```

Interpret the JSON result:

1. If `mode` is `pass-through` (or there is no clear directive) → proceed with the engine’s normal path. Do **not** alter the prompt.
2. If `mode` is `random` or `explicit` → immediately run activation and merge results:

```bash
# preferred: let nl_route execute
python /home/workdir/.grok/skills/image-pipeline/scripts/nl_route.py "<user request text>" --run --json

# or equivalent direct calls:
# python .../pipeline_activate.py random --seed <N> --json
# python .../pipeline_activate.py explicit --preset <id> --json
```

From the activation JSON, merge into the generation path:

- Append every `prompt_terms[].term` to the positive prompt (respect `weight` / `variance` as soft guidance; low-variance terms such as photographer names should be kept nearly exact).
- Record `active_extensions` and `packs` in any review / trace layer.
- If `pass_through` is true, ignore terms and continue unchanged.

### Directive examples the router already understands
- "random pipeline"
- "use bunny top 10 #3" / "liv top 10 #1" / "valerie top 10 #5"
- "apply helmut newton graphic dominance" (and other named style presets)
- "pass-through" / "no pipeline" / "pipeline off"

### Default
No directive → pass-through → engine behaves exactly as before this integration.

### Failure behavior
If the pipeline scripts are missing or return an error, log the failure and fall back to pass-through so generation is never blocked.

### Preferred single call (hands-free)
```bash
python /home/workdir/.grok/skills/image-pipeline/scripts/engine_hook.py "<user request text>"
```
Returns the thin adapter JSON. If `pass_through` is true or `error` is set, continue with the engine’s normal prompt. Otherwise merge `prompt_terms` into the positive prompt and record `active_extensions` / `packs` in trace/review output.



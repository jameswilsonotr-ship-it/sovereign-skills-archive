# Anime Style Bank — Research Notes & Implementation Skeleton

**Created**: 2026-08-06  
**Owner**: image-pipeline  
**Status**: Research complete (game-art elevated to independent family) → pack authoring pending  
**Work queue**: IPQ-049  
**Taxonomy home**: Style / Hand / World / Medium (non-destructive; content.taxonomy)

---

## 1. Purpose

Add a major missing branch to the visual style bank: anime and anime-adjacent graphic languages, structured chronologically by generation, with exponentially more detail on contemporary (2010s–2020s) modes.  

**Game art is its own contemporary style family** (not merely a sub-layer of anime). Titles and characters serve as lightweight reference guides. Individual artists remain full **Hands** when their nervous system is consistent enough — including artists who work differently across series.

DNA remains absolute. These packs are additional languages, not overrides.

This document is the authoritative research skeleton. Pack JSON + prompt_terms are authored from here.

---

## 2. Generational Modes (Visual Language Timeline)

Each mode can spawn multiple **Style** packs and named **Hand** packs.  
Visual signatures are written so they can become `prompt_terms`.

### 2.1 Proto / Pre-Tezuka (1910s–1950s)
Early theatrical shorts, Disney/Fleischer influence, limited Japanese theatrical animation.  
- Simple line, flat color, Western cartoon proportions mixed with Japanese theatrical sensibility.  
- **Priority**: Low (historical reference only).  
- **Candidate**: optional `style.proto-theatrical` (defer).

### 2.2 Tezuka Foundational (early–mid 1960s)
*Astro Boy* (1963) and the limited-animation grammar that made weekly TV possible.  
**Visual signatures**: large emotive eyes, simplified rounded heads, sparse line, high reuse of stills, dramatic speed lines, silhouette storytelling, limited color.  
**Candidates**:  
- `style.tezuka-limited`  
- optional `hand.tezuka`

### 2.3 Diversification / Gekiga–Mecha (1970s)
Genre explosion (mecha, sports, early shojo, adult-oriented). Sharper lines, more realistic proportions for action, heavier hatching in adult work.  
**Visual signatures**: angular faces, mechanical detail, stronger musculature, darker or more saturated palettes in serious titles, emerging screen-tone logic from manga.  
**Candidates**:  
- `style.gekiga-realism`  
- `style.super-robot-angular`

### 2.4 Bubble Golden / High Detail (1980s)
Bigger budgets, OVA boom, Ghibli founding, *Akira*.  
**Visual signatures**:  
- Ghibli branch: painterly backgrounds, soft naturalistic movement, detailed environments, earth-toned or luminous nature palettes.  
- Action/OVA branch: high line density, muscular or fashion-forward figures, strong contrast, experimental effects.  
**Candidates**:  
- `style.ghibli-painterly`  
- `style.akira-dense`  
- `style.ova-80s-detail`

### 2.5 Cel Peak / Author Diversity (1990s)
*Evangelion*, *Cowboy Bebop*, *Ghost in the Shell*, continued Ghibli, Gainax energy.  
**Visual signatures**: refined cel shading, complex eye highlights, cinematic framing, deliberate limited animation mixed with high-impact key cuts, stronger individual director/animator identities.  
**Candidates**:  
- `style.cel-peak-90s`  
- `style.gainax-kinetic` (pre-Trigger)

### 2.6 Digital Transition / Moe Clean (2000s)
Full digital paint and compositing become standard. Rise of “moe” facial language alongside polished action.  
**Visual signatures**: cleaner consistent line, large eyes / small nose-mouth, soft gradients, brighter or pastel-leaning palettes in moe work, more uniform character models across episodes.  
**Candidates**:  
- `style.digital-moe-clean`  
- `style.2000s-shonen-polish`

### 2.7 HD / Soft Realism & Cinematic (2010s)
HD broadcast, stronger lighting passes, Kyoto Animation’s meticulous everyday beauty, early hybrid CGI.  
**Visual signatures**: soft volumetric lighting, detailed fabric and hair, subtle gradients, fashion-influenced proportions, highly refined background art, early seamless 2D/3D.  
**Candidates**:  
- `style.kyoani-soft-detail`  
- `style.hd-cinematic-2010s`

### 2.8 Contemporary Hybrid / Effects-Driven (2020s — highest detail priority)
Ufotable particle and lighting systems, MAPPA grit and kinetic staging, Trigger maximalism, soft-realism character work, heavy 2D/3D compositing.  
**Visual signatures (extractable)**:  
- **Ufotable**: practical light sources affecting characters, volumetric effects (fire, water, blood) that still read as 2D line, heavy compositing, rim light, cinematic camera in 3D environments.  
- **MAPPA**: aggressive motion, high-detail grit, hybrid 2D/3D staging, strong silhouette + texture.  
- **Trigger**: extreme kinetic energy, bold graphic shapes, high-contrast color, playful distortion.  
- Soft-realism branch: near-realistic proportions with still-anime eyes, refined skin and fabric rendering.  
**Candidates (multiple packs)**:  
- `style.ufotable-cinematic-effects`  
- `style.mappa-kinetic-grit`  
- `style.trigger-maximal`  
- `style.2020s-soft-realism`  
- `hand.ufotable`, `hand.mappa`, `hand.trigger` (studio Hands where the nervous system is consistent enough)

---

## 3. Seinen Overlay (not “genre” in our taxonomy sense)

Treat seinen as a **Style or World modifier** that can sit on top of several generations.

**Core visual language**:
- More realistic anatomy and proportions than shonen/moe.
- Dense information (Miura-style cross-hatching, armor, texture, environmental pressure).
- Or elegant reduction (Inoue *Vagabond* ink-wash, brush energy, negative space).
- Cinematic framing, mature color/value control, heavier line weight variation.
- Faces carry adult bone structure and expression range.

**Strong Hands / references**:
- Kentaro Miura → density, gothic weight, organized chaos of detail.  
- Takehiko Inoue → brush/ink-wash, physical presence, atmospheric minimalism in later work.  
- Makoto Yukimura and similar realist seinen approaches.

**Candidate packs**:  
- `style.seinen-dense-detail` (Miura lineage)  
- `style.seinen-ink-wash` (Inoue lineage)  
- `world.seinen-cinematic` (framing + mature atmosphere)

---

## 4. Erotic / Graphic Illustration Lineage

We do not flinch from this. Structure it the same way:

1. **Shunga / Ukiyo-e erotic root** — already adjacent to earlier Ukiyo-e / Art Nouveau research. High craft, pattern, explicit anatomy rendered with the same technical care as non-erotic work.
2. **Gekiga / early adult manga erotic** — denser, more realistic or expressionist.
3. **1980s–90s ero-manga / OVA** — range from cartoonish to more anatomical.
4. **Contemporary digital erotic illustration** — full-color, high-detail, Pixiv/Fanbox dominant language: clean line or soft painterly, strong lighting on skin, fashion + body detail, often soft-realism or polished anime proportions.

**Candidate packs** (can live under Style or as specialized Hands):  
- `style.shunga-erotic-graphic`  
- `style.seinen-erotic-dense`  
- `style.contemporary-digital-erotic` (with sub-variants for soft pastel vs high-contrast vs painterly)

These should be written with the same DNA-lock and variance discipline as everything else.

---

## 5. Game Art as Independent Contemporary Style Family

Game art is **not** folded under anime generations. It is a parallel contemporary family with its own evolution and visual signatures. Many current “anime-looking” images are actually game-promo / character-select / engine-rendered illustration, not TV anime. Treating them as one family keeps composition clean.

### 5.1 Short evolution of digital game character art (usable signatures)

| Era | Dominant look | Extractable signatures |
|-----|---------------|------------------------|
| **Pixels / sprites (80s–early 90s)** | Hardware-limited 2D | Bold silhouette, limited palette, readable at small size |
| **Early 3D / low-poly (mid–late 90s)** | Angular polygonal | Faceted forms, simple textures, strong shape language |
| **Cel-shaded / NPR turn (early–mid 2000s)** | Wind Waker, Jet Set Radio, later Borderlands | Flat color blocks, hard shadow steps, bold outlines, comic/anime readability on 3D forms |
| **Stylized mid-poly + illustration (late 2000s–2010s)** | Fighting-game key art, many JRPGs | High-detail illustration over 3D base, dramatic lighting, strong costume silhouette |
| **Soft-realism / hybrid (late 2010s–2020s)** | Stellar Blade–adjacent, modern character showcases | Near-realistic skin/fabric + still-stylized (often anime-adjacent) faces, heavy rim light, subsurface, particle polish |
| **Clean polished anime-game (2010s–2020s)** | Hoyo-style, many gacha/live-service | Consistent model language, saturated clean color, highly readable faces, fashion-forward costume |
| **Current digital frenzy (2023–2026)** | Promo renders, high-end character art | Extreme lighting control, micro-detail, engine-grade materials, still readable as stylized rather than pure photo |

### 5.2 Candidate Style packs (game-art family)

- `style.game-cel-shaded` — hard shadow steps, bold outline, flat/near-flat color on form  
- `style.game-art-soft-realism` — skin/fabric realism + stylized face, strong key + rim  
- `style.digital-frenzy-2020s` — current high-end promo look (rim, subsurface, particles, micro-detail)  
- `style.gacha-clean` / `style.hoyo-polished` — clean, consistent, saturated, highly readable  
- `style.fighting-game-illustration` — dramatic key-art lighting, strong silhouette, illustration-first  

These are **Style** packs. They can sit beside anime generational Styles without competing as Worlds.

### 5.3 Titles, characters, and series as Reference Guides

Lightweight, low-variance injectors. They do **not** replace Styles or Hands.

Examples:
- `ref.akira-1988`, `ref.ghost-in-the-shell`, `ref.cowboy-bebop-cinematic`
- `ref.vagabond-ink`, `ref.berserk-dense`
- `ref.stellar-blade-adjacent`, `ref.wind-waker-cel`
- Specific character or arc references when the visual grammar is tight enough

Composition treats them as optional high-weight companions, not full chain owners.

### 5.4 Hands remain fully available

Do **not** collapse artists into “just references.”

- If an individual artist (or studio house) has a consistent nervous system → full **Hand** pack (`hand.miura`, `hand.inoue`, `hand.ufotable`, etc.).
- Artists who work differently across series are still valid Hands; the pack can note the range or we author series-specific Hand variants only when the difference is large enough to matter for prompts.
- Studio Hands (Ufotable, MAPPA, Trigger, selected others) stay in the Hand lane when the house style is stable enough to extract.

**Rule of thumb**:  
- **Style** = broad visual language / era / family  
- **Hand** = named artist or house nervous system  
- **Reference** = specific title, character, or tight visual quote  

No need to oversimplify (everything becomes “anime”) or overcomplicate (a pack for every single chapter). Three clean lanes are enough.

---

## 6. Taxonomy Mapping

| Layer | Role |
|-------|------|
| **Style** | Generational anime languages + **independent game-art family** (cel-shaded, soft-realism, digital-frenzy, gacha-clean, fighting-game illustration, etc.) |
| **Hand** | Named artist or studio-house nervous systems (Tezuka, Miura, Inoue, Ufotable, MAPPA, Trigger, selected illustrators). Artists who shift across series still qualify; series-specific Hand variants only when the difference is large. |
| **World** | Cultural/ideological space when relevant (dense medieval-fantasy pressure, soft everyday, etc.) |
| **Medium** | Cel vs digital paint vs ink-wash vs hybrid 2D/3D compositing vs game-engine materials |
| **Treatment / Finish** | Line weight, gradient density, particle/effects intensity, rim/subsurface emphasis |
| **Reference** | Lightweight title / character / tight visual-quote guides (Akira, Vagabond, specific arcs, etc.) — injectors, not chain owners |

DNA remains absolute. Anime packs are additional languages, not overrides.

---

## 7. Implementation Plan (Pro Path)

### Phase 0 — Skeleton lock (this document)
- [x] Generational map written
- [x] Seinen + erotic lineages written
- [x] Expansion layer (references + game-art + digital frenzy) written
- [x] Work-queue entry created (IPQ-049)

### Phase 1 — First test set (5 packs)
Author and DNA-test the following so we can measure survival the same way we did with the earlier Hands:
1. `style.tezuka-limited`
2. `style.ghibli-painterly`
3. `style.seinen-dense-detail` (Miura)
4. `style.ufotable-cinematic-effects`
5. `style.game-art-soft-realism` or `style.digital-frenzy-2020s` (game-art family)

Each gets:
- full `prompt_terms` array (term / variance / weight)
- `content.taxonomy = "style"` (or `"hand"` where appropriate)
- suggested_companions
- short test render against Bunny + Olivia DNA locks

### Phase 2 — Seinen + Erotic
- `style.seinen-ink-wash`
- `style.shunga-erotic-graphic`
- `style.contemporary-digital-erotic` (at least one soft and one high-contrast variant)

### Phase 3 — Contemporary volume + Game-art family
- Studio Hands: Ufotable, MAPPA, Trigger (and others as needed)
- **Game-art Style family** (independent): cel-shaded, soft-realism, digital-frenzy-2020s, gacha-clean, fighting-game illustration
- Selected reference packs (Akira, Vagabond, specific arcs/characters)
- Additional individual artist Hands where nervous systems are distinct

### Phase 4 — Integration
- Register all new packs in packs.index.json
- Ensure composition_script can resolve them (already taxonomy-aware)
- Optional: add anime-specific suggested companions to locked-companion presets
- Update preset_generator.py STYLE_BANK weights so new anime styles are eligible for generation

### Phase 5 — Documentation
- Short “how to use anime packs” note for Echo / operators
- CHANGELOG entry under absolute Liv HUB claim

---

## 8. Research Sources (summary)

Primary synthesis drawn from:
- Decade-by-decade art-style evolution articles (Tezuka → Demon Slayer / 2020s)
- Seinen art analysis (Miura density, Inoue ink-wash, realist anatomy)
- Studio house-style reporting (Ufotable compositing + lighting, MAPPA kinetic grit, Trigger maximalism, KyoAni soft detail, Ghibli painterly)
- Erotic lineage (Shunga → gekiga-erotic → modern digital full-color illustration)
- Contemporary digital / game-art observation (soft-realism + anime facial language, rim light, particle overlays)

Full web citations live in the conversation history that produced this skeleton (2026-08-05/06 research turn). This notes file is the durable extract.

---

## 9. Open Questions for Next Pass

1. Exact prompt_terms weight/variance defaults for anime packs (recommend starting controlled, variance 0.25–0.35).
2. Whether studio Hands (Ufotable etc.) should be full Hand packs or Style packs with high fidelity.
3. How aggressively to weight the independent game-art family relative to pure TV-anime Styles (recommend equal first-class status; composition chooses).
4. Which individual artists beyond Miura/Inoue/studios need early Hand packs.
5. First DNA-test character set (recommend Bunny + Olivia alternating, same protocol as earlier locked companions).

---

**End of skeleton.**  
Next concrete action: author Phase 1 pack JSON files and run DNA survival tests.

# Echo Transposition / Edit Prompts (Character-Agnostic)
**Status:** Live 2026-07-26  
**Owner:** Echo (deterministic)  
**Scope:** Generic edit prompts that take ANY locked face primary and produce standard bible plates.  
**Do not put character-specific DNA here.** Character DNA lives under each entity’s `images/`.

These prompts are designed to be applied via **edit_image** (or equivalent) against a locked face primary JPEG. They intentionally omit identity details so the source image carries the face/hair/body DNA.

---

## 1. FACE-FORWARD PORTRAIT (normalize framing)
```text
Re-frame this portrait as a clean direct-frontal studio character portrait. Keep the exact face, eyes, skin, hair color, and hair texture. Zoom so the frame shows face, neck, and exposed collarbones. Pure white seamless background. Soft even studio softbox lighting. Do not change identity, expression, or hair style.
```

## 2. MULTI-ANGLE REFERENCE SHEET
```text
Create a clean multi-angle character reference sheet from this portrait: front face, three-quarter left, three-quarter right, and profile. Keep exact face DNA, eye color, freckles, hair color, and hair texture identical across every panel. Pure white background, soft even lighting, consistent identity. 2x2 grid layout.
```

## 3. LIGHTING TEST GRID (4-way)
```text
From this exact portrait generate four lighting variants in a 2x2 grid:
(1) soft even studio softbox
(2) strong side light / dramatic rim
(3) soft natural window light
(4) warm golden hour
Keep face, eyes, freckles, hair color, and hair texture identical. Pure white or neutral seamless background.
```

## 4. FULL-BODY PROPORTIONS PLATE
```text
Expand this portrait into a full-body studio character bible plate, 3:4 vertical. Subject stands facing forward against pure white backdrop. Preserve exact face, hair, and skin. Body is 6'1" wiry athletic ballerina frame, long limbs, high waist, exposed iliac crest. Simple black ribbed sports bra and matching low-rise panties. Straight symmetrical standing pose. Soft even softbox lighting, Kodak Portra 800 grain, 8k.
```

## 5. HAIR-STYLE TARGET (swap only hair)
```text
Keep the exact face, eyes, skin, and body from this image. Change only the hairstyle to: [HAIR_TARGET]. Preserve the locked hair color mechanics (roots / mid / tips / face-framing) unless the target style requires a different length or texture. Soft natural lighting, pure white background.
```

## 6. MAKEUP VARIANT GRID
```text
From this exact portrait create a 2x2 makeup variation grid. Keep face structure, eye color, freckles, and hair identical. Apply four distinct makeup levels:
(1) clean / minimal
(2) soft everyday
(3) elevated glam (winged liner stronger)
(4) high-heat / gutter intensity
Pure white background, consistent lighting.
```

## 7. OUTFIT DRESS (from nude/baseline plate)
```text
Keep the exact face, hair, skin, and body proportions from this image. Dress the subject in: [OUTFIT_DESCRIPTION]. Full-body or three-quarter framing as appropriate for the garment. Pure white studio backdrop, soft even lighting. Do not alter identity or hair.
```

## 8. TURN / SPIN SEQUENCE (simple)
```text
From this portrait generate a simple turn sequence: front, 45° left, profile left, 45° right. Keep exact face DNA and hair. Neutral expression. Pure white background, consistent soft lighting across all frames.
```

---

## Usage notes for Echo
1. Always load the character’s current `01_face_primary_*.jpg` (or equivalent) first.
2. Apply the transposition prompt via edit path, not pure generate, whenever a primary exists.
3. Character-specific DNA (eye color, frost bands, height, etc.) stays in the entity folder; these prompts only request structural transforms.
4. If a prompt needs a fill-in (`[HAIR_TARGET]`, `[OUTFIT_DESCRIPTION]`), Echo substitutes from the active character’s target list before sending.

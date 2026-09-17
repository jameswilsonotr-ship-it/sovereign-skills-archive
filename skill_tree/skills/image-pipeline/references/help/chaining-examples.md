---
slug: chaining-examples
stage: reference
type: documentation
description: Concrete worked examples of style_chain usage with the new Stage-Aware + Transformer system.
---

# Style Chain Examples

## Example 1: Photoreal → Mid → Anime (Most Common)

**User Request:**
```
Generate a clean Liv version of this mirror selfie, then convert it to anime.
style_chain: photoreal → mid-structural-photoreal → photoreal-to-anime-v1
strength: 0.7
```

**Execution Trace:**
1. Load `mid-structural-photoreal`
   - Produces clean structural mid image (pose, hands, lighting locked)
2. Load `photoreal-to-anime-v1` @ strength 0.7
   - Applies anime transformer on the mid image
3. Final output: High-quality anime Liv with excellent structural fidelity

**Recommended For:** Most Liv/Bunny character work where you want strong anime stylization without losing pose accuracy.

## Example 2: Direct Anime Stylization (Faster, Less Precise)

**User Request:**
```
style_chain: photoreal → photoreal-to-anime-v1
strength: 0.65
```

**When to Use:** When the original photoreal generation already has very strong pose/lighting (heavy use of pose-anchoring + lighting-consistency modules). Skips the mid step for speed.

## Example 3: Anime → Ink Wash (Artistic Crossover)

**User Request:**
```
style_chain: photoreal → mid-structural-photoreal → photoreal-to-anime-v1 → anime-to-ink-wash
```

**Note:** This is a longer chain. Each step should use moderate strength (0.5–0.65) to avoid cumulative degradation.

## Example 4: Heavy Stylization Path

**User Request:**
```
style_chain: photoreal → mid-structural-photoreal → glossy-noir → raw-chaotic
```

**Warning:** Long chains with heavy stylization transformers can drift significantly. Use lower strengths and consider inserting a mid refresh if the chain is >3 transformers.

## Strength Recommendations by Chain Length

| Chain Length | Recommended Strength per Transformer | Notes |
|--------------|--------------------------------------|-------|
| 2 steps      | 0.65 – 0.75                          | Safe default |
| 3 steps      | 0.55 – 0.65                          | Prevents over-stylization |
| 4+ steps     | 0.45 – 0.55                          | Use mid refreshes between heavy transformers |

These examples should be used as reference when testing chaining behavior. Update this file as new transformers are added.
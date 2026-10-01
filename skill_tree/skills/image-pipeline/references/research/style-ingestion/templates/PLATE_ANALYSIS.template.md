# Plate Analysis Template (Style Ingestion)

**Module**: style-ingestion  
**Version**: 0.1.0  
**Constraint**: Fill one plate at a time. Batch ≤ 3. No numeric scores until user confirms the plate landed (IP-WQ-042).

```
PLATE ID: [sequential or source-derived]
SOURCE:
  - channel / uploader
  - on-screen artist credit (or OCR if needed)
  - timestamp / frame if compilation
  - Drive path or direct URL
  - any additional context (playlist, series title, year if known)

MEDIUM & HAND:
  - digital / cel / ink / hybrid / painterly / other
  - line weight character (clean, sketchy, heavy, thin, variable)
  - shading language (cel flat, soft gradient, screentone, crosshatch, painterly)

PALETTE:
  - dominant 3–5 colors (descriptive or hex when clear)
  - saturation / contrast temperature
  - any signature accent or lighting habit

FACE / EYE CONVENTIONS:
  - eye size / shape / highlight style
  - brow and lash treatment
  - nose / mouth / jaw conventions
  - any recurring expression, gaze, or facial proportion habit

OUTFIT TROPES:
  - silhouette + key garments
  - fabric / accessory language
  - any recurring accessory, color blocking, or construction detail that could teach

CLUSTER NOTES:
  - closest existing registry entry (anime_substyle, hand, medium, or “new candidate”)
  - suggested registry key or implication-pack draft name
  - qualitative strength of fit only (no scores yet)

GATE:
  - promote / demote / hold / needs second look
  - reason (one short line)
  - your call only
```

## Notes for the agent

- Keep language observational and concrete. Avoid value judgments until the human gate.
- If OCR is required for on-screen credit, note the confidence and the raw text.
- When three plates form a coherent cluster, propose the candidate registry row and stop for human decision.
- DNA locks (Liv + Bunny) are never rewritten from these plates.
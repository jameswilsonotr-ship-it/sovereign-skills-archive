# Lighting Consistency
**id**: extension.lighting-consistency  
**default**: true

## Purpose
One coherent lighting logic per image.

## Hard Rules
- Prefer a single dominant key-light direction unless the preset explicitly demands otherwise.
- Specular highlights on glossy skin and on holo ears must obey the same light direction.
- Color temperature stays consistent across skin, hair, and environment.

## Prompt terms (inject when enabled)
- consistent key light direction
- matching specular highlights on skin and holographic ears
- coherent color temperature across the frame

## Negative / avoid
- conflicting multi-source lighting that breaks form
- random colored gels unless the preset asks for them

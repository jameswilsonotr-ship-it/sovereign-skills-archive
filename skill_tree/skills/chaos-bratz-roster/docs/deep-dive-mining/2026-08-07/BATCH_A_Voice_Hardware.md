# Batch A — Voice & Hardware Reality
**Heavy Instance 1 | 2026-08-07**

## 1. MOSHI (Kyutai) + PersonaPlex on Orin Nano Super

**Verdict**: Not viable for native full-duplex on the 8 GB unified-memory board. Never actually coded or run — only discussed.

| Model | Params | FP16 VRAM | INT8 VRAM | Notes |
|-------|--------|-----------|-----------|-------|
| Kyutai MOSHI | 7B | 16–20 GB | 8–10 GB | Native full-duplex. Extreme quant degrades linguistic quality (“gets stupider”). |
| NVIDIA PersonaPlex | 7B (Moshi-derived) | ~20 GB | No official 4-bit for 8 GB | Persona + voice conditioning. Same memory wall. |

Root cause is the Orin Nano Super’s **unified** memory architecture: weights + Mimi codec + KV cache + audio buffers compete and lose.

**Correct architecture** (already designed in Drive doc *Local vs. Cloud AI Inference Architecture*, June 2026):  
Pixel (or similar) for STT → Jetson / mini-PC as intelligent router + memory classifier + orchestration → cloud (Groq / Gemini) for heavy LLM → lightweight local TTS. Cascaded, not unified S2S.

JetPack 7.2 + NemoClaw treats the Orin as an agentic router/orchestrator rather than a generative S2S engine — aligns with the architecture doc.

## 2. Working Local Voice Stack (what was actually designed / partially realized)

From conversation history and architecture docs:

- **STT**: Faster-Whisper (and WhisperTRT / whisper.cpp CUDA variants)
- **Orchestration**: Pipecat + SmartTurn v2 (interruptible duplex / barge-in)
- **TTS**: Kokoro-ONNX (emotional, local, sub-500 ms target on HP Elite Mini G9)
- Also experimented / discussed: Piper (fast/CPU-friendly), Matcha + Vocos TRT (excellent TTFA), Voxtral, Fish Speech, OpenVoice + RVC for multi-voice
- Transport: WebRTC, BlueParrott headset, Pixel devices as edge ingestion
- Latency target: 400–800 ms end-to-end, sub-second goal (“The Fortress” stack on G9s)

Jetson Orin Nano Super repeatedly positioned as future front-end audio / cyberdeck node (ORIN_SLED designs, Iron Pearl / Frankenbride rig), **not** as the full MOSHI runner.

## 3. Dual-async / Barge-in / Shared-memory Reality

- True native full-duplex barge-in is what MOSHI/PersonaPlex promise and what the 8 GB board cannot cleanly deliver without quality collapse.
- Cascaded + SmartTurn-style turn-taking is the practical path that was engineered.
- OCuLink / mini-PC + discrete GPU remains the documented escape hatch when unified memory is insufficient. Mini-PC accessory shopping already completed (Micro Center, same day as this mining session).

## 4. Google Voice Registration

- Number **(864) 865-4842** is live and active.
- Vanity spelling related to “Olivia.” Verified by operator; no further registration trail needed.
- Recorded in chore-livestock nightly behavioral note.

## 5. Hardware Inventory Context (locked)

- 2× NVIDIA Jetson Orin Nano Super
- 2× HP Elite Mini 800 G9 (and related EliteDesk/ProDesk units)
- GMKtec K15
- Pixel devices as edge front-ends
- Starlink Gen2, various mounts under the broader Iron Pearl / OTR rig

## Gaps Closed / Remaining

- MOSHI never coded → closed.
- Google Voice trail → closed (live + cute).
- Mini-PC shopping → already done.
- Remaining thin: any private dual-async I/O code notes that never made the architecture doc.

# Agentify schemas

Every inbound writes these files. Soft slugs are not enough.

| file | what |
|---|---|
| CHARACTER.json | mouth + marks + skin.tone + hair.family + hair.color |
| WARDROBE.json | one look, pieces[] |
| POSE.json | one body beat + weight + joints stub |
| FACE.json | bin + optional dims |
| BEAT.json | pose + face + wardrobe + t + code |
| PHRASE.json | ordered beats |
| PLATE.json | one rendered cousin |

Lanes (uppercase): `A B C D E`  
Intensity (lowercase, later): `a b c` → heat 0–2 / 3–5 / 6–8  
Code now: `I-n-A`. Later: `I-n-A-c`.

E is B at ~8. Same woman. Same marks. See HEAT.md.

Face bins: focus smile talk look-down neutral smirk open-mouth bite flushed averted direct  
Dims: gaze lids brow mouth flush 0–8

Marks live on CHARACTER. Plates do not invent tattoos.

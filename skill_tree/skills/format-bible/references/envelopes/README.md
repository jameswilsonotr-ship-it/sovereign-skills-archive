# Pre-generated Envelopes (format-bible v1.4+)

Durable starting points. On a brand-new conversation the agent inspects the initial user prompt, chooses (or is told) one of these, and writes it to `current.md`.

## Set

| Name | Intent | Images | Text shape | Forensics |
|------|--------|--------|------------|-----------|
| default | Balanced everyday | Optional | hybrid | when needed |
| structural | Contract / planning / format | 0 default | structured + narrative | minimal |
| visual | Standard creative / claim | 4, scores under each | hybrid | full |
| immersive | Image-driven | 6+ | minimal | full |
| tui | Options / menus / control | 0 default | tui-menu | minimal |
| debug | Maximum observability | optional | structured | full required |

## Commands

```bash
python3 scripts/assemble_envelope.py status
python3 scripts/assemble_envelope.py list
python3 scripts/assemble_envelope.py switch <name> [--reason "text"]
python3 scripts/assemble_envelope.py promote [<name>]
python3 scripts/assemble_envelope.py choose --prompt "first user message"
```

Natural language: `envelope status` | `envelope list` | `envelope switch <name>` | `envelope promote`

See `../../QUICKSTART.md` for the full quick-start inventory.

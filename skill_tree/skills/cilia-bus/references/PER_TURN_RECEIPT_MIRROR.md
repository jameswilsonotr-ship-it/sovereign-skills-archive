# Per-turn bus receipt mirror
Created: 2026-08-27
Parent Drive: 1siHFYKMyaNxQNqHcrqlBXBX_mpGqWU-Q
Receipts folder: 1XHu94u2JmVEIomflSRvUSYjsGM2R7ENP (bus-receipts-mirror)

## Standing rule for every Olivia Expert / Heavy turn that touches the bus
1. `google_drive_list_folder` on `1XHu94u2JmVEIomflSRvUSYjsGM2R7ENP`
2. If new files since last high-water, download and treat as inbound bus state
3. Do not wait for Gmail to be re-read in chat — Drive is the ACK
4. High-water is last receipt filename / file_id, not last Gmail preview

## Jobs
- `email bridge grok bot` — subject OLIVIA-BRIDGE — draft ACK
- `bus orch stress` — subject BUS-ORCH-STRESS — five breakpoints

Never put both tags on one subject.

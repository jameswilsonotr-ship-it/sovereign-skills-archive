# [RUN LOG] Template
**Version**: 1.0.0

Every test response that performs generation **must** include a visible block in this form:

```
[RUN LOG] — <Option / Description>

| # | Engine / Actor | Character | Angle / Heat | File | Disk Status | DNA / Notes |
|---|----------------|-----------|--------------|------|-------------|-------------|
| 1 | ...            | ...       | ...          | ...  | Succeeded / Failed (0-byte) / Missing | ... |

Summary:
- Requested: X
- Succeeded: Y
- Failed / Empty: Z
- DNA Errors: list
- Moderation / Write failures: list
- Notes: free text
```

## Rules
- Always show the table even if every call failed.
- Record the exact filename returned by the tool when available.
- Explicitly mark 0-byte or missing files.
- Note any DNA violations (ears on Liv, shark-fin, wrong hair, footwear drift, etc.).
- After the log, present the updated menu table.

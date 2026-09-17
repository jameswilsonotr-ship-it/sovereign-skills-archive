# S2-30 Fixture Checksums

Offline fixture checksum records use one row per local fixture:

| path | sha256 | byte_len | recorded_at |
| --- | --- | ---: | --- |
| relative fixture path | 64 lowercase hexadecimal characters | non-negative integer | UTC RFC 3339 timestamp |

This document contains schema only; fixture blobs are not included.

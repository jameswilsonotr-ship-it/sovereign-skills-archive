# Porn Curator — Script Registry Schema
**Version**: 0.2.0  
**Updated**: 2026-07-25

Every script under this skill is registered in `script_registry.json`.  
Top-level systems can load that single JSON and filter instantly by type, tool wrapped, folder, etc.

## Required fields (every entry)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable slug |
| `type` | string | `wrapper` \| `helper` \| `atomizer` \| `one-off` \| `other` |
| `file_name` | string | Bare filename (e.g. `web_search_wrapper.py`) |
| `folder` | string | Folder relative to curator root (e.g. `scripts`, `atoms`) |
| `path` | string | Full relative path from curator root |
| `description` | string | Short purpose |
| `status` | string | `active` \| `draft` \| `deprecated` |

## Extra fields when `type` == `"wrapper"`

| Field | Type | Description |
|-------|------|-------------|
| `wraps` | string | Human name of what is being wrapped |
| `tool_call` | string | Exact tool name this wrapper stands in front of (e.g. `web_search`, `browse_page`) |
| `origination` | string | Value written into response.origination |
| `payload_policy` | string | How the payload is treated for the local vs remote side |

## payload_policy (for web_search_wrapper)
- **web / remote side**: full original query, including any `site:` or domain operators.
- **atom-cloud side**: only the clean porn search terms (domain operators and site: filters stripped). The local cloud never sees `site:xvideos.com` etc.

## Example filter uses
- All wrappers: `type == "wrapper"`
- Everything that wraps web_search: `tool_call == "web_search"`
- Everything in a folder: `folder == "scripts"`

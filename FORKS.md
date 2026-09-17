# FORKS.md — top-level pins

Rule: every third-party library we care about pinning gets its **own** top-level repo under `jameswilsonotr-ship-it/<name>`. No git submodules. No `vendor/vendor/<name>`. No nest under Thunderclap.

pyproject / requirements pin to those forks + git tags / commit SHAs once the fork exists. Until then, pin the upstream tag in comments and install from the wheelhouse.

## Done this sprint

| Upstream | Our fork | Notes |
|---|---|---|
| RinDig/Interpretable-Context-Methodology | jameswilsonotr-ship-it/Interpretable-Context-Methodology | TOP-LEVEL. ICM paper implementation. MIT. |

## List-only tonight (fork when we freeze)

| Upstream | Why | First pin target |
|---|---|---|
| RinDig/icm-architect | skill already local; freeze the method | latest main SHA |
| astral-sh/ruff | CI lint | latest stable tag |
| pytest-dev/pytest | CI | 8.x tag |
| pytest-dev/pytest-cov | coverage artifact | 5.x tag |
| encode/httpx | live connector transport later | 0.27+ |
| encode/httpcore | httpx pin twin | matching httpx |
| python-pillow/Pillow | fixture image bytes | 10.x / 11.x |
| jd/tenacity | connector retry | 9.x |
| tox-dev/py-filelock | concurrent SKILL.md writers | 3.x |
| pypa/build | wheelhouse | latest |
| pypa/wheel | wheelhouse | latest |
| pypa/setuptools | wheelhouse | latest |
| modelcontextprotocol/python-sdk | phone-bridge later | tagged release |

## Do not fork

- duckdb, h3 — already vendored as wheels under keep-lake-query. Do not copy 21MB wheels into this PR.
- langchain, lancedb, chromadb, any vector DB
- Imagine / Grok image clients
- Inkbox — Cursor connector is live; no jameswilsonotr-ship-it repo. Phone-bridge v0 is Termux/Tailscale, not Inkbox SMS.

## Wheelhouse

Builder pattern: `/home/workdir/.grok/skills/wheelhouse-packager` v0.2.0.
GitHub Release upload is blocked until a `create_release` connector exists. This PR ships pointer + package only.

# Junk Rules

Mark junk and residual content conservatively. Do not remove anything automatically.

## System Junk

These are safe default junk candidates:

- `.DS_Store`
- `Thumbs.db`
- `Desktop.ini`
- `__pycache__`
- `.pytest_cache`
- `.mypy_cache`
- `.ruff_cache`

## Residual Directories

Treat these as residual candidates rather than guaranteed junk:

- `Cache`
- `Caches`
- `Temp`
- `tmp`
- `Logs`
- `build`
- `dist`
- `target`

Only mark them when the path context strongly suggests generated output rather than primary user content.

## Chat And App Cache Candidates

Common cache-like candidates:

- chat image caches
- offline package folders
- temp transfer folders
- backup cache folders

Do not assume all chat exports are junk. Many are legitimate archives and should instead score toward `Archives`.

## Software-Generated Residuals

Look for:

- duplicated installers inside export folders
- generated build outputs
- temporary download suffixes
- broken or odd extension suffixes
- stale lock or swap files

## Handling Rules

- Mark candidates in metadata.
- Route junk or residual candidates to quarantine only if the user asks.
- Never physically delete based on the rule engine alone.
- Prefer false negatives over false positives.

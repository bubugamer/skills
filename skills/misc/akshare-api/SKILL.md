---
name: akshare-api
description: Use when the user wants free financial-market data through AKShare, including current or historical A-share data, concept or industry boards, concept constituents, company profiles, financial statements, announcements, funds, futures, indices, macro data, or help finding and calling an AKShare function. Trigger for requests that mention `AKShare`, `akshare-api`, “免费的股票接口”, “用同花顺概念数据”, or market-data work that needs broader coverage than TDX. Do not use when the user explicitly requires TDX, an official exchange feed, trade execution, or investment recommendations.
metadata:
  compatibility: "Requires Python 3.10 or newer and network access to the public websites used by AKShare."
---

# AKShare API

Use the bundled client to query AKShare without loading its entire function catalog into context.

AKShare is a library that aggregates many public data sources. It is not itself a market-data exchange or a single authoritative database. Always report the underlying source shown by the client, such as 同花顺 or 东方财富.

## Default workflow

1. Identify the requested market, fields, period, adjustment method, and output shape.
2. Prefer a task command from the common command table below.
3. If no task command fits, use `search`, then `describe`, then `call`; this is how the skill handles AKShare's large catalog without embedding hundreds of functions.
4. Check that all requested securities and required fields are present.
5. State the underlying website, retrieval time, and whether the result is a snapshot, a completed historical bar, or another dataset.
6. Do not silently switch to TDX, another AKShare provider, or a web search when an endpoint fails. Report the failed source first and ask or explain before using a substitute.
7. For claims about “today” or the latest trading day, confirm the date with a dated series when the snapshot itself has no trading-date field.

## Common commands

Use the wrapper so dependencies stay isolated inside this skill:

```bash
<skill-dir>/scripts/akshare quote 002432 603533 --source sina --format table
<skill-dir>/scripts/akshare history 688111 --start 20260701 --end 20260721 --source sina --adjust none --format json --pretty
<skill-dir>/scripts/akshare concepts --source ths --query Kimi --format table
<skill-dir>/scripts/akshare concept-members "Kimi概念" --format table
```

The wrapper creates a private runtime on first use and installs the pinned AKShare version. If installation fails, report the dependency error instead of changing providers.

### Task routing

| User need | Command | Underlying source |
|---|---|---|
| Current A-share snapshot | `quote --source em\|sina` | 东方财富 or 新浪财经 through AKShare |
| A-share bars | `history --source em\|sina` | 东方财富, or 新浪财经 for daily bars |
| Concept names and current board snapshot | `concepts` | 同花顺 or 东方财富, selected explicitly |
| Concept index history | `concept-history` | 同花顺 through AKShare |
| Concept board summary | `concept-info` | 同花顺 through AKShare |
| Concept constituents | `concept-members` | 东方财富 through AKShare |
| Company business profile | `profile` | 同花顺 through AKShare |
| Main financial indicators | `financials` | 同花顺 through AKShare |
| Listed-company announcements | `announcements` | 东方财富 through AKShare |

This source split is deliberate. The current AKShare catalog does not expose a matching convenience function for every task from every provider. Never label 东方财富 concept constituents as 同花顺 constituents.

### Quotes

```bash
<skill-dir>/scripts/akshare quote 002432 603533 --source em --format json --pretty
```

The command filters a full-market snapshot and returns the requested codes in the original request order. `--source em` selects 东方财富 and `--source sina` selects 新浪财经. Missing codes cause an explicit error instead of being omitted. 新浪's own AKShare documentation warns that repeated full-market requests can temporarily block the caller's IP, so avoid polling it in a tight loop.

Snapshots can lack a reliable trading-date field. When answering “今天表现”, pair the snapshot with a short `history` request to confirm the latest dated session.

### Historical bars

```bash
<skill-dir>/scripts/akshare history 688111 --start 20260701 --end 20260721 --source em --period daily --adjust none --format table
```

Adjustment values are:

- `none`: raw, unadjusted prices
- `qfq`: forward-adjusted prices
- `hfq`: backward-adjusted prices

`--source em` supports daily, weekly, and monthly bars. `--source sina` is limited to daily bars in this convenience command. State the provider and adjustment method in the answer. Do not compare series with different adjustment methods without warning.

### Concepts

```bash
<skill-dir>/scripts/akshare concepts --source ths --query Kimi --format table
<skill-dir>/scripts/akshare concept-info "Kimi概念" --format table
<skill-dir>/scripts/akshare concept-history "Kimi概念" --start 20260101 --end 20260721 --format json
<skill-dir>/scripts/akshare concept-members "Kimi概念" --format table
```

Concept membership is provider-defined and can change. Report which provider supplied the membership list, and use company announcements or investor-relations records when the user asks whether the business relationship is real.

### Company and announcement data

```bash
<skill-dir>/scripts/akshare profile 002432 --format table
<skill-dir>/scripts/akshare financials 002432 --indicator report --format table
<skill-dir>/scripts/akshare announcements --date 20260721 --symbol 全部 --format table --limit 30
```

Financial indicator values are `report`, `year`, `q1`, `q2`, `q3`, and `q4`. Financial tables can contain multiple reporting bases and restated values. Preserve AKShare's original column names and report dates.

## Large-catalog escape hatch

AKShare has hundreds of exported functions. Find and call only the one needed:

```bash
<skill-dir>/scripts/akshare search "ETF 实时" --format table
<skill-dir>/scripts/akshare describe fund_etf_spot_ths --format json --pretty
<skill-dir>/scripts/akshare call fund_etf_spot_ths --format table --limit 20
<skill-dir>/scripts/akshare call stock_board_industry_index_ths --param symbol='半导体' --param start_date=20260101 --param end_date=20260721 --format json
```

`call` accepts only a public callable exported by the installed `akshare` module. Parameters use `--param key=value`; JSON values such as `true`, `12`, or `["a","b"]` are decoded, while other values stay strings.

Before using a function found through `search`, run `describe` to inspect its current signature. Function names and webpage-backed behavior can change between AKShare releases.

## Reporting and error rules

- Distinguish “AKShare library” from the underlying data provider.
- Include the installed AKShare version and retrieval time when data freshness matters.
- Preserve suspended, missing, or failed securities explicitly.
- Treat an empty table as a failed or empty source response, not as proof that no security exists.
- Do not claim that an endpoint is official merely because AKShare exposes it.
- Do not use this skill to place orders or recommend trades.
- If a public page blocks or changes its schema, report the exact function and source. Do not fabricate missing fields.
- `--limit N` returns the first N rows; `--tail N` returns the last N rows. Use `--tail` for “latest N bars”.

## References

Read [references/function-routing.md](references/function-routing.md) when choosing between providers, using the generic `call` command, or explaining coverage limitations.

## Locating bundled scripts

Resolve `<skill-dir>` to the absolute folder containing this SKILL.md before running a command. Paths beginning `scripts/` are relative to that folder, not to the user workspace. Keep the user workspace as the working directory when a script uses `--root .`.

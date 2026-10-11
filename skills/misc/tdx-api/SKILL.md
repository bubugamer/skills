---
name: tdx-api
description: Use when the user wants current or historical Shanghai/Shenzhen market data through TDX or pytdx, including A-share quotes, daily or minute bars, realtime or historical ticks, security lists, corporate actions, finance data, or TDX concept-block records. Trigger for requests that mention `tdx-api`, `pytdx`, `通达信接口`, “用附件接口取股价”, “查今天收盘价”, or a list of mainland stock codes that needs a price/performance table. Do not use for Hong Kong or US quotes, concept-membership research without market data, investment advice, or trade execution.
metadata:
  compatibility: "Requires Python 3.10 or newer, network access to a working TDX quote server, and the bundled Python dependencies."
---

# TDX API

Use the bundled client to read Shanghai and Shenzhen market data through `pytdx`.

This skill is a market-data reader. It does not place orders, choose stocks, or turn a market theme into an investment recommendation.

## Default workflow

1. Identify the requested securities, fields, period, and output shape.
2. Run `scripts/tdx`; it creates a private runtime on first use and automatically selects a TDX server unless one is supplied.
3. Prefer one batch quote request for up to 80 securities.
4. Check that the returned rows contain the requested codes and required fields.
5. For claims about “today”, “close”, or a trading date, fetch at least one daily bar to confirm the session date. Realtime quote data contains a server time but not a complete trading date.
6. State the retrieval time and whether the data is realtime, an intraday snapshot, or a completed daily bar.
7. If realtime quote or tick data is empty, report the failure. Do not silently replace it with historical data.

## Commands

Use the wrapper so dependencies stay isolated inside this skill:

```bash
<skill-dir>/scripts/tdx server --format table
<skill-dir>/scripts/tdx quote 002432 603533 --format table
<skill-dir>/scripts/tdx bars 002432 --period day --count 5 --format json --pretty
<skill-dir>/scripts/tdx ticks 002432 --count 100 --format csv
```

The wrapper installs the pinned dependencies only when its private runtime is missing. If that install fails, report the dependency error instead of switching data providers without telling the user.

### Server selection

Server choice follows this order:

1. `--ip` and optional `--port`
2. `TDX_IP` and optional `TDX_PORT`
3. automatic probing of the `pytdx` server list

When the user supplies an explicit server and it fails, return that failure. Do not quietly use another server.

### Realtime quotes

```bash
<skill-dir>/scripts/tdx quote 688111 002555 600986 --format json --pretty
```

Default quote fields include latest price, previous close, calculated price change and percentage change, open, high, low, volume, amount, and TDX server time.

Use `--raw` only when the user needs the full five-level book or original fields:

```bash
<skill-dir>/scripts/tdx quote 002432 --raw --format json --pretty
```

### Bars

```bash
<skill-dir>/scripts/tdx bars 002432 --period day --count 20 --format table
<skill-dir>/scripts/tdx bars 300133 --period 5min --count 48 --format json
```

Supported periods are `day`, `week`, `month`, `quarter`, `year`, `1min`, `5min`, `15min`, `30min`, and `60min`. Bars are raw TDX bars and are not automatically adjusted for corporate actions.

### Ticks

```bash
<skill-dir>/scripts/tdx ticks 002432 --count 500 --format json
<skill-dir>/scripts/tdx history-ticks 002432 --date 20260720 --count 500 --format csv
```

Treat `buyorsell` as a TDX-native marker. Do not reinterpret it without checking the source convention.

### Reference data

```bash
<skill-dir>/scripts/tdx securities --market sz --start 0 --format json
<skill-dir>/scripts/tdx xdxr 002432 --format json --pretty
<skill-dir>/scripts/tdx finance 002432 --format json --pretty
<skill-dir>/scripts/tdx block --file block_gn.dat --name "Kimi概念" --format json
```

Modern TDX block files can change format. If block parsing fails or produces no trustworthy match, say so and use a separate current source for concept membership. Continue to use TDX for prices when the user requested this provider.

Use security-list results for codes and names, not for live pricing. With `pytdx` 1.72, some current Shanghai servers fail on the first list page and some list-level `pre_close` values are malformed. Report that limitation instead of treating the list as a quote source.

## Market and code rules

- Shanghai market code: `1`
- Shenzhen market code: `0`
- Codes beginning with `5`, `6`, or `9` use Shanghai.
- Prefixes `009`, `126`, `110`, `201`, `202`, `203`, and `204` also use Shanghai.
- Other six-digit codes use Shenzhen.
- Accept plain codes and common forms such as `600000.SH`, `SZ000001`, and `sh600000`.

The bundled client follows these rules from the supplied interface specification. It is not a Hong Kong, US, futures, or trade-execution client.

## Reporting rules

When returning prices or market performance:

- Include the exact trading date when it was confirmed from a bar.
- Label price units and percentage changes.
- Say whether the market was still open or the daily bar was complete when that distinction matters.
- Preserve suspended or missing securities as explicit missing results; do not omit them silently.
- Distinguish market-data facts from separate web research about why a security belongs to a concept.
- Mention source limitations when concept membership came from another provider.

## Error handling

- Empty realtime quote: fail explicitly; do not use the last daily close as a substitute.
- Empty realtime tick: fail explicitly; do not use historical ticks as a substitute.
- Unreachable explicit server: report the server and the connection error.
- More than 80 quote codes: split into batches of at most 80.
- Missing required fields: report which fields or codes are missing before drawing conclusions.
- Unsupported market: say that this client covers only the TDX Shanghai/Shenzhen mapping described above.

## Reference

Read [references/pytdx-interface.md](references/pytdx-interface.md) when a request needs a lower-level method, raw field meaning, pagination, or block-file behavior not covered above.

## Locating bundled scripts

Resolve `<skill-dir>` to the absolute folder containing this SKILL.md before running a command. Paths beginning `scripts/` are relative to that folder, not to the user workspace. Keep the user workspace as the working directory when a script uses `--root .`.

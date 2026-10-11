# AKShare function routing

## Contents

1. Scope and provenance
2. Bundled task commands
3. Generic catalog workflow
4. Reliability rules
5. Documentation links

## Scope and provenance

AKShare is a Python access layer over many public financial-data websites and institutional publications. A successful AKShare call establishes what the selected endpoint returned; it does not make the data an official exchange record.

Suffixes often reveal the underlying source:

| Function suffix or family | Typical source |
|---|---|
| `_ths` | 同花顺 public pages |
| `_em` | 东方财富 public endpoints |
| `_sina` | 新浪财经 public endpoints |
| `_sse`, `_szse`, `_bse` | Exchange publication or endpoint |
| `_cninfo` | 巨潮资讯 |
| `_csindex` | 中证指数 |

This is a useful routing hint, not a substitute for reading the function documentation.

## Bundled task commands

The CLI intentionally exposes a small stable surface:

| CLI command | AKShare function |
|---|---|
| `quote --source em` | `stock_zh_a_spot_em` |
| `quote --source sina` | `stock_zh_a_spot` |
| `history --source em` | `stock_zh_a_hist` |
| `history --source sina` | `stock_zh_a_daily` or `stock_zh_kcb_daily` |
| `concepts --source ths` | `stock_board_concept_name_ths` |
| `concepts --source em` | `stock_board_concept_name_em` |
| `concept-info` | `stock_board_concept_info_ths` |
| `concept-history` | `stock_board_concept_index_ths` |
| `concept-members` | `stock_board_concept_cons_em` |
| `profile` | `stock_zyjs_ths` |
| `financials` | `stock_financial_abstract_new_ths` |
| `announcements` | `stock_notice_report` |

These commands validate common parameters, add retrieval metadata, and make provider choice visible.

## Generic catalog workflow

Use this sequence for tasks outside the bundled commands:

1. `search <keywords>` finds exported functions by function name and docstring.
2. `describe <function>` shows the installed function's signature and documentation.
3. `call <function> --param key=value` invokes the exact public function.
4. Inspect returned columns before drawing conclusions.

The generic call deliberately does not retry with a similar function. Similar names can point at different providers or datasets.

## Reliability rules

- Pinning the AKShare package stabilizes Python signatures, but it cannot freeze upstream websites.
- Website anti-bot controls, schema changes, or delayed publication can break a previously working function.
- Current snapshots often have no explicit trading date. Confirm the date with a dated historical series.
- Concept names and membership are taxonomies maintained by the provider; two providers can disagree.
- An empty DataFrame can mean “no records”, “bad symbol”, “blocked request”, or “upstream schema change”. Use surrounding evidence and report uncertainty.
- Respect public-site rate limits. Batch requests and avoid tight polling loops.

## Documentation links

- AKShare documentation: https://akshare.akfamily.xyz/
- AKShare stock-data catalog: https://akshare.akfamily.xyz/data/stock/stock.html
- AKShare source repository: https://github.com/akfamily/akshare

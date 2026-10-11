# pytdx interface reference

This reference condenses the interface supplied with the original `pytosisi` export. Use it when a request needs a lower-level method or raw-field interpretation beyond the bundled command-line client.

## Runtime

- `pytdx` 1.72
- `pandas` 2.3.3
- `retrying` 1.4.2
- Main class: `pytdx.hq.TdxHq_API`
- Normal TDX port: `7709`

Basic connection:

```python
from pytdx.hq import TdxHq_API

api = TdxHq_API(raise_exception=True)
with api.connect(ip, 7709, time_out=1.0):
    data = api.get_security_quotes([(1, "603095")])
```

Use `TdxHq_API(multithread=True, raise_exception=True)` for a multithreaded batch-quote client when appropriate.

## Markets

| market | meaning |
| --- | --- |
| `0` | Shenzhen |
| `1` | Shanghai |

Ordinary security mapping:

| code pattern | market |
| --- | --- |
| first digit `5`, `6`, or `9` | Shanghai `1` |
| prefix `009`, `126`, `110`, `201`, `202`, `203`, or `204` | Shanghai `1` |
| all other supported six-digit codes | Shenzhen `0` |

Index mapping in the supplied system was simpler: codes starting with `3` were Shenzhen indexes and other index codes were Shanghai indexes.

## Bar periods

`get_security_bars(category, market, code, start, count)` categories:

| period | category |
| --- | --- |
| day | `9` |
| week | `5` |
| month | `6` |
| quarter | `10` |
| year | `11` |
| 1 minute | `8` |
| 5 minutes | `0` |
| 15 minutes | `1` |
| 30 minutes | `2` |
| 60 minutes | `3` |

Raw bars are not automatically adjusted. Retrieve corporate actions separately when an adjusted series is required.

## Raw methods

| purpose | method | main arguments |
| --- | --- | --- |
| connectivity probe | `get_security_list(market, start)` | market, start |
| security count | `get_security_count(market)` | market |
| security list | `get_security_list(market, start)` | market, start |
| bars | `get_security_bars(category, market, code, start, count)` | category, market, code, start, count |
| realtime quote and book | `get_security_quotes(pairs)` | list of `(market, code)`; normally at most 80 |
| realtime ticks | `get_transaction_data(market, code, start, count)` | market, code, start, count |
| historical ticks | `get_history_transaction_data(market, code, start, count, date)` | date is an integer `YYYYMMDD` |
| corporate actions | `get_xdxr_info(market, code)` | market, code |
| finance data | `get_finance_info(market, code)` | market, code |
| block-file version | `get_block_dat_ver_up("incon.dat")` | file name |
| parse block file | `get_and_parse_block_info(file_name)` | for example `block.dat` or `incon.dat` |
| DataFrame conversion | `api.to_df(data)` | returned list |

## Common quote fields

| field | meaning |
| --- | --- |
| `code` | security code |
| `price` | latest price |
| `last_close` | previous close |
| `open`, `high`, `low` | current session values |
| `vol`, `cur_vol` | total and current volume fields |
| `amount` | turnover amount |
| `bid1`–`bid5`, `ask1`–`ask5` | five-level prices |
| `bid_vol1`–`bid_vol5`, `ask_vol1`–`ask_vol5` | five-level volumes |
| `b_vol`, `s_vol` | TDX inner/outer-volume-related fields |
| `servertime` | server time; it is not a complete trading date |

## Common tick fields

| field | meaning |
| --- | --- |
| `date`, `time`, `datetime` | date/time fields when present |
| `code` | security code |
| `price` | transaction price |
| `vol` | transaction volume |
| `buyorsell` | original TDX direction marker |
| `num`, `order` | sequence/order fields |

Do not assign an undocumented interpretation to `buyorsell`.

## Common bar fields

| field | meaning |
| --- | --- |
| `date`, `datetime` | bar date/time |
| `code` | security code when supplied or added by the caller |
| `open`, `high`, `low`, `close` | OHLC |
| `vol` | volume |
| `amount` | turnover amount |
| `date_stamp`, `time_stamp` | timestamp fields when present |

## Pagination and errors

- Batch quotes: at most 80 securities per request.
- Bar pagination: commonly 800 rows per page.
- Tick pagination: commonly 2,000 rows per page.
- Empty data, connection failures, or missing required fields must be reported explicitly.
- Realtime quote and tick requests must not silently fall back to historical data.
- Block-file formats can change; parsing errors are not evidence that a concept has no members.
- With `pytdx` 1.72 and some current servers, the first Shanghai security-list page can fail to parse. Security-list `pre_close` values can also be malformed. Use the list for code/name discovery only and fetch actual prices through `get_security_quotes`.

## Scope

This interface reads market data. It does not contain stock selection, trading, scoring, portfolio, or backtesting decisions.

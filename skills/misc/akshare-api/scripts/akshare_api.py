#!/usr/bin/env python3
from __future__ import annotations

import argparse
import inspect
import json
import math
import re
import sys
import warnings
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Callable, Iterable
from zoneinfo import ZoneInfo

import akshare as ak
import pandas as pd

warnings.filterwarnings(
    "ignore", category=pd.errors.SettingWithCopyWarning, module=r"akshare\..*"
)


class AkshareCliError(RuntimeError):
    pass


@dataclass
class QueryResult:
    data: Any
    source: str
    function: str
    notes: list[str] = field(default_factory=list)
    extra_meta: dict[str, Any] = field(default_factory=dict)


SOURCE_LABELS = {
    "ths": "同花顺 public data via AKShare",
    "em": "东方财富 public data via AKShare",
    "sina": "新浪财经 public data via AKShare",
    "cninfo": "巨潮资讯 data via AKShare",
    "sse": "上海证券交易所 data via AKShare",
    "szse": "深圳证券交易所 data via AKShare",
    "bse": "北京证券交易所 data via AKShare",
    "csindex": "中证指数 data via AKShare",
}


def now_shanghai() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")


def clean_code(value: str) -> str:
    compact = re.sub(r"[^A-Za-z0-9]", "", value.strip())
    upper = compact.upper()
    for prefix in ("SH", "SZ", "BJ"):
        if upper.startswith(prefix):
            upper = upper[len(prefix) :]
    for suffix in ("SH", "SZ", "BJ"):
        if upper.endswith(suffix):
            upper = upper[: -len(suffix)]
    if not re.fullmatch(r"\d{6}", upper):
        raise AkshareCliError(f"invalid mainland security code: {value!r}")
    return upper


def validate_yyyymmdd(value: str) -> str:
    try:
        datetime.strptime(value, "%Y%m%d")
    except ValueError as exc:
        raise AkshareCliError(f"invalid date {value!r}; expected YYYYMMDD") from exc
    return value


def infer_source(function_name: str) -> str:
    exact_sources = {
        "stock_zh_a_hist": SOURCE_LABELS["em"],
        "stock_zh_a_spot": SOURCE_LABELS["sina"],
        "stock_zh_a_daily": SOURCE_LABELS["sina"],
        "stock_zh_kcb_daily": SOURCE_LABELS["sina"],
    }
    if function_name in exact_sources:
        return exact_sources[function_name]
    for suffix, label in SOURCE_LABELS.items():
        if function_name.endswith(f"_{suffix}") or f"_{suffix}_" in function_name:
            return label
    if function_name == "stock_notice_report":
        return SOURCE_LABELS["em"]
    return "Function-dependent public source via AKShare; inspect the function documentation"


def json_safe(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else value
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(item) for item in value]
    if isinstance(value, pd.DataFrame):
        clean = value.astype(object).where(pd.notna(value), None)
        return [json_safe(row) for row in clean.to_dict(orient="records")]
    if isinstance(value, pd.Series):
        return json_safe(value.to_dict())
    if hasattr(value, "item"):
        try:
            return json_safe(value.item())
        except (TypeError, ValueError):
            pass
    return str(value)


def ensure_dataframe(value: Any, function_name: str) -> pd.DataFrame:
    if not isinstance(value, pd.DataFrame):
        raise AkshareCliError(
            f"{function_name} returned {type(value).__name__}, but this task command expects a table"
        )
    if value.empty:
        raise AkshareCliError(
            f"{function_name} returned an empty table; no provider fallback was attempted"
        )
    return value


def call_ak(function_name: str, **kwargs: Any) -> Any:
    function = getattr(ak, function_name, None)
    if function is None or function_name.startswith("_") or not callable(function):
        raise AkshareCliError(f"AKShare does not export a public callable named {function_name!r}")
    try:
        return function(**kwargs)
    except Exception as exc:  # AKShare exposes many provider-specific exception types.
        raise AkshareCliError(
            f"AKShare function {function_name} failed: {exc}; no provider fallback was attempted"
        ) from exc


def quote_command(args: argparse.Namespace) -> QueryResult:
    codes = [clean_code(item) for item in args.codes]
    function_name = "stock_zh_a_spot_em" if args.source == "em" else "stock_zh_a_spot"
    frame = ensure_dataframe(call_ak(function_name), function_name)
    if "代码" not in frame.columns:
        raise AkshareCliError(f"{function_name} response has no 代码 column")
    work = frame.copy()
    try:
        work["代码"] = work["代码"].astype(str).map(clean_code)
    except AkshareCliError as exc:
        raise AkshareCliError(f"{function_name} returned an invalid security code: {exc}") from exc
    indexed = work.set_index("代码", drop=False)
    missing = [code for code in codes if code not in indexed.index]
    if missing:
        raise AkshareCliError(
            f"{function_name} omitted requested codes: " + ", ".join(missing)
        )
    result = indexed.loc[codes].reset_index(drop=True)
    if not args.raw:
        preferred = [
            "代码",
            "名称",
            "最新价",
            "昨收",
            "涨跌额",
            "涨跌幅",
            "今开",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "换手率",
            "时间戳",
        ]
        columns = [column for column in preferred if column in result.columns]
        result = result[columns]
    return QueryResult(
        data=result,
        source=SOURCE_LABELS[args.source],
        function=function_name,
        notes=["Current full-market snapshot; the payload may not include a trading-date field."],
        extra_meta={"requested_codes": codes, "selected_source": args.source},
    )


def history_command(args: argparse.Namespace) -> QueryResult:
    code = clean_code(args.code)
    start = validate_yyyymmdd(args.start)
    end = validate_yyyymmdd(args.end)
    adjust_map = {"none": "", "qfq": "qfq", "hfq": "hfq"}
    if args.source == "em":
        function_name = "stock_zh_a_hist"
        kwargs = {
            "symbol": code,
            "period": args.period,
            "start_date": start,
            "end_date": end,
            "adjust": adjust_map[args.adjust],
        }
        frame = ensure_dataframe(call_ak(function_name, **kwargs), function_name)
    else:
        if args.period != "daily":
            raise AkshareCliError("--source sina supports only --period daily in the history command")
        if code.startswith(("688", "689")):
            function_name = "stock_zh_kcb_daily"
            frame = ensure_dataframe(
                call_ak(function_name, symbol=f"sh{code}", adjust=adjust_map[args.adjust]), function_name
            )
            date_column = "date" if "date" in frame.columns else "日期"
            if date_column not in frame.columns:
                raise AkshareCliError(f"{function_name} response has no date column")
            parsed = pd.to_datetime(frame[date_column], errors="coerce")
            start_ts = pd.Timestamp(datetime.strptime(start, "%Y%m%d").date())
            end_ts = pd.Timestamp(datetime.strptime(end, "%Y%m%d").date())
            frame = frame.loc[parsed.between(start_ts, end_ts)]
            frame = ensure_dataframe(frame, function_name)
        elif code.startswith(("4", "8", "9")):
            raise AkshareCliError("新浪 A-share daily history does not cover Beijing codes in this command")
        else:
            function_name = "stock_zh_a_daily"
            market_prefix = "sh" if code.startswith(("5", "6")) else "sz"
            frame = ensure_dataframe(
                call_ak(
                    function_name,
                    symbol=f"{market_prefix}{code}",
                    start_date=start,
                    end_date=end,
                    adjust=adjust_map[args.adjust],
                ),
                function_name,
            )
    return QueryResult(
        data=frame,
        source=SOURCE_LABELS[args.source],
        function=function_name,
        notes=[f"Price adjustment: {args.adjust}."],
        extra_meta={
            "code": code,
            "period": args.period,
            "start": start,
            "end": end,
            "adjust": args.adjust,
            "selected_source": args.source,
        },
    )


def concepts_command(args: argparse.Namespace) -> QueryResult:
    function_name = (
        "stock_board_concept_name_ths" if args.source == "ths" else "stock_board_concept_name_em"
    )
    frame = ensure_dataframe(call_ak(function_name), function_name)
    if args.query:
        needle = args.query.casefold()
        mask = frame.astype(str).apply(
            lambda column: column.str.casefold().str.contains(needle, regex=False, na=False)
        ).any(axis=1)
        frame = frame.loc[mask]
        if frame.empty:
            raise AkshareCliError(
                f"{function_name} returned no concept matching {args.query!r}; no provider fallback was attempted"
            )
    return QueryResult(
        data=frame,
        source=SOURCE_LABELS[args.source],
        function=function_name,
        extra_meta={"query": args.query or None},
    )


def concept_info_command(args: argparse.Namespace) -> QueryResult:
    function_name = "stock_board_concept_info_ths"
    frame = ensure_dataframe(call_ak(function_name, symbol=args.name), function_name)
    return QueryResult(frame, SOURCE_LABELS["ths"], function_name, extra_meta={"concept": args.name})


def concept_history_command(args: argparse.Namespace) -> QueryResult:
    function_name = "stock_board_concept_index_ths"
    start = validate_yyyymmdd(args.start)
    end = validate_yyyymmdd(args.end)
    frame = ensure_dataframe(
        call_ak(function_name, symbol=args.name, start_date=start, end_date=end), function_name
    )
    return QueryResult(
        frame,
        SOURCE_LABELS["ths"],
        function_name,
        notes=["Provider-defined concept index series."],
        extra_meta={"concept": args.name, "start": start, "end": end},
    )


def concept_members_command(args: argparse.Namespace) -> QueryResult:
    function_name = "stock_board_concept_cons_em"
    frame = ensure_dataframe(call_ak(function_name, symbol=args.name), function_name)
    return QueryResult(
        frame,
        SOURCE_LABELS["em"],
        function_name,
        notes=["These are 东方财富 concept constituents, not 同花顺 constituents."],
        extra_meta={"concept": args.name},
    )


def profile_command(args: argparse.Namespace) -> QueryResult:
    function_name = "stock_zyjs_ths"
    code = clean_code(args.code)
    frame = ensure_dataframe(call_ak(function_name, symbol=code), function_name)
    return QueryResult(frame, SOURCE_LABELS["ths"], function_name, extra_meta={"code": code})


def financials_command(args: argparse.Namespace) -> QueryResult:
    function_name = "stock_financial_abstract_new_ths"
    code = clean_code(args.code)
    indicator_map = {
        "report": "按报告期",
        "year": "按年度",
        "q1": "一季度",
        "q2": "二季度",
        "q3": "三季度",
        "q4": "四季度",
    }
    frame = ensure_dataframe(
        call_ak(function_name, symbol=code, indicator=indicator_map[args.indicator]), function_name
    )
    return QueryResult(
        frame,
        SOURCE_LABELS["ths"],
        function_name,
        extra_meta={"code": code, "indicator": args.indicator},
    )


def announcements_command(args: argparse.Namespace) -> QueryResult:
    function_name = "stock_notice_report"
    report_date = validate_yyyymmdd(args.date)
    frame = ensure_dataframe(
        call_ak(function_name, symbol=args.symbol, date=report_date), function_name
    )
    if args.code:
        code = clean_code(args.code)
        code_columns = [column for column in frame.columns if "代码" in str(column)]
        if not code_columns:
            raise AkshareCliError("stock_notice_report response has no security-code column")
        mask = frame[code_columns[0]].astype(str).str.zfill(6).eq(code)
        frame = frame.loc[mask]
        if frame.empty:
            raise AkshareCliError(
                f"stock_notice_report returned no announcement for {code} on {report_date}"
            )
    return QueryResult(
        frame,
        SOURCE_LABELS["em"],
        function_name,
        extra_meta={"date": report_date, "symbol": args.symbol, "code": args.code or None},
    )


def public_functions() -> Iterable[tuple[str, Callable[..., Any]]]:
    for name in sorted(dir(ak)):
        value = getattr(ak, name)
        if not name.startswith("_") and callable(value):
            yield name, value


def search_command(args: argparse.Namespace) -> QueryResult:
    terms = [part.casefold() for part in args.query.split() if part]
    rows: list[dict[str, str]] = []
    for name, function in public_functions():
        doc = inspect.getdoc(function) or ""
        haystack = f"{name} {doc}".casefold()
        if all(term in haystack for term in terms):
            first_line = next((line.strip() for line in doc.splitlines() if line.strip()), "")
            rows.append(
                {
                    "function": name,
                    "signature": safe_signature(function),
                    "summary": first_line[:240],
                    "inferred_source": infer_source(name),
                }
            )
    if not rows:
        raise AkshareCliError(f"no exported AKShare function matched {args.query!r}")
    return QueryResult(
        pd.DataFrame(rows),
        "Installed AKShare function catalog",
        "catalog-search",
        notes=["Search matches function names and installed docstrings; inspect a function before calling it."],
        extra_meta={"query": args.query},
    )


def safe_signature(function: Callable[..., Any]) -> str:
    try:
        return str(inspect.signature(function))
    except (TypeError, ValueError):
        return "(signature unavailable)"


def describe_command(args: argparse.Namespace) -> QueryResult:
    function = getattr(ak, args.function, None)
    if function is None or args.function.startswith("_") or not callable(function):
        raise AkshareCliError(f"AKShare does not export a public callable named {args.function!r}")
    data = {
        "function": args.function,
        "signature": safe_signature(function),
        "documentation": inspect.getdoc(function) or "",
        "inferred_source": infer_source(args.function),
    }
    return QueryResult(data, "Installed AKShare function catalog", "describe")


def parse_parameter(item: str) -> tuple[str, Any]:
    if "=" not in item:
        raise AkshareCliError(f"invalid parameter {item!r}; expected key=value")
    key, raw_value = item.split("=", 1)
    key = key.strip()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
        raise AkshareCliError(f"invalid parameter name: {key!r}")
    value_text = raw_value.strip()
    try:
        value = json.loads(value_text)
    except json.JSONDecodeError:
        value = value_text
    return key, value


def generic_call_command(args: argparse.Namespace) -> QueryResult:
    kwargs: dict[str, Any] = {}
    for item in args.param:
        key, value = parse_parameter(item)
        if key in kwargs:
            raise AkshareCliError(f"duplicate parameter: {key}")
        kwargs[key] = value
    result = call_ak(args.function, **kwargs)
    if isinstance(result, pd.DataFrame) and result.empty:
        raise AkshareCliError(
            f"{args.function} returned an empty table; no provider fallback was attempted"
        )
    return QueryResult(
        result,
        infer_source(args.function),
        args.function,
        notes=["Generic function call; verify the current signature and returned columns."],
        extra_meta={"parameters": kwargs},
    )


def add_output_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--format", choices=("json", "csv", "table"), default="table")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    parser.add_argument("--limit", type=int, help="return at most this many rows or items")
    parser.add_argument("--tail", type=int, help="return the last this many rows or items")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="akshare",
        description="Task-oriented AKShare reader with explicit provider metadata.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    quote = subparsers.add_parser("quote", help="current A-share snapshot from an explicit provider")
    quote.add_argument("codes", nargs="+")
    quote.add_argument("--source", choices=("em", "sina"), default="em")
    quote.add_argument("--raw", action="store_true")
    add_output_arguments(quote)
    quote.set_defaults(handler=quote_command)

    history = subparsers.add_parser("history", help="A-share historical bars from an explicit provider")
    history.add_argument("code")
    history.add_argument("--start", required=True)
    history.add_argument("--end", required=True)
    history.add_argument("--source", choices=("em", "sina"), default="em")
    history.add_argument("--period", choices=("daily", "weekly", "monthly"), default="daily")
    history.add_argument("--adjust", choices=("none", "qfq", "hfq"), default="none")
    add_output_arguments(history)
    history.set_defaults(handler=history_command)

    concepts = subparsers.add_parser("concepts", help="list concept boards")
    concepts.add_argument("--source", choices=("ths", "em"), default="ths")
    concepts.add_argument("--query", help="case-insensitive text filter across returned columns")
    add_output_arguments(concepts)
    concepts.set_defaults(handler=concepts_command)

    concept_info = subparsers.add_parser("concept-info", help="同花顺 concept-board summary")
    concept_info.add_argument("name")
    add_output_arguments(concept_info)
    concept_info.set_defaults(handler=concept_info_command)

    concept_history = subparsers.add_parser("concept-history", help="同花顺 concept index history")
    concept_history.add_argument("name")
    concept_history.add_argument("--start", required=True)
    concept_history.add_argument("--end", required=True)
    add_output_arguments(concept_history)
    concept_history.set_defaults(handler=concept_history_command)

    concept_members = subparsers.add_parser("concept-members", help="东方财富 concept constituents")
    concept_members.add_argument("name")
    add_output_arguments(concept_members)
    concept_members.set_defaults(handler=concept_members_command)

    profile = subparsers.add_parser("profile", help="同花顺 company business profile")
    profile.add_argument("code")
    add_output_arguments(profile)
    profile.set_defaults(handler=profile_command)

    financials = subparsers.add_parser("financials", help="同花顺 main financial indicators")
    financials.add_argument("code")
    financials.add_argument(
        "--indicator", choices=("report", "year", "q1", "q2", "q3", "q4"), default="report"
    )
    add_output_arguments(financials)
    financials.set_defaults(handler=financials_command)

    announcements = subparsers.add_parser("announcements", help="东方财富 announcement report")
    announcements.add_argument("--date", required=True)
    announcements.add_argument("--symbol", default="全部")
    announcements.add_argument("--code")
    add_output_arguments(announcements)
    announcements.set_defaults(handler=announcements_command)

    search = subparsers.add_parser("search", help="search installed AKShare functions")
    search.add_argument("query")
    add_output_arguments(search)
    search.set_defaults(handler=search_command)

    describe = subparsers.add_parser("describe", help="show a function signature and docstring")
    describe.add_argument("function")
    add_output_arguments(describe)
    describe.set_defaults(handler=describe_command)

    generic_call = subparsers.add_parser("call", help="call a public exported AKShare function")
    generic_call.add_argument("function")
    generic_call.add_argument("--param", action="append", default=[], metavar="KEY=VALUE")
    add_output_arguments(generic_call)
    generic_call.set_defaults(handler=generic_call_command)

    return parser


def apply_limit(data: Any, limit: int | None, tail: int | None) -> Any:
    if limit is not None and tail is not None:
        raise AkshareCliError("use only one of --limit and --tail")
    count = tail if tail is not None else limit
    if count is None:
        return data
    if count < 1:
        raise AkshareCliError("--limit and --tail must be at least 1")
    if isinstance(data, pd.DataFrame):
        return data.tail(count) if tail is not None else data.head(count)
    if isinstance(data, pd.Series):
        return data.tail(count) if tail is not None else data.head(count)
    if isinstance(data, (list, tuple)):
        return data[-count:] if tail is not None else data[:count]
    return data


def output_result(result: QueryResult, args: argparse.Namespace) -> None:
    data = apply_limit(result.data, args.limit, args.tail)
    meta = {
        "library": "AKShare",
        "akshare_version": getattr(ak, "__version__", "unknown"),
        "underlying_source": result.source,
        "function": result.function,
        "retrieved_at_asia_shanghai": now_shanghai(),
        "notes": result.notes,
        **result.extra_meta,
    }
    if isinstance(data, pd.DataFrame):
        meta["row_count"] = len(data)
        meta["columns"] = [str(column) for column in data.columns]
    elif isinstance(data, (list, tuple)):
        meta["item_count"] = len(data)

    if args.format == "json":
        payload = {"meta": json_safe(meta), "data": json_safe(data)}
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
        return

    if args.format == "csv":
        print("# " + json.dumps(json_safe(meta), ensure_ascii=False), file=sys.stderr)
        if isinstance(data, pd.DataFrame):
            data.to_csv(sys.stdout, index=False)
        elif isinstance(data, pd.Series):
            data.to_frame().to_csv(sys.stdout)
        elif isinstance(data, (list, tuple)) and all(isinstance(item, dict) for item in data):
            pd.DataFrame(data).to_csv(sys.stdout, index=False)
        else:
            raise AkshareCliError("CSV output requires tabular data")
        return

    print(f"Source: {meta['underlying_source']}")
    print(f"AKShare: {meta['akshare_version']}")
    print(f"Retrieved: {meta['retrieved_at_asia_shanghai']}")
    print(f"Function: {meta['function']}")
    for note in result.notes:
        print(f"Note: {note}")
    if isinstance(data, pd.DataFrame):
        print(data.to_string(index=False))
    elif isinstance(data, pd.Series):
        print(data.to_string())
    elif isinstance(data, (dict, list, tuple)):
        print(json.dumps(json_safe(data), ensure_ascii=False, indent=2))
    else:
        print(json_safe(data))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
        output_result(result, args)
    except AkshareCliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

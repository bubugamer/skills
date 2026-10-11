#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import os
import re
import socket
import sys
import time
from collections.abc import Iterable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime
from typing import Any

from pytdx.config.hosts import hq_hosts
from pytdx.hq import TdxHq_API


PERIODS = {
    "day": 9,
    "week": 5,
    "month": 6,
    "quarter": 10,
    "year": 11,
    "1min": 8,
    "5min": 0,
    "15min": 1,
    "30min": 2,
    "60min": 3,
}

QUOTE_FIELDS = [
    "code",
    "market_name",
    "price",
    "last_close",
    "change",
    "change_pct",
    "open",
    "high",
    "low",
    "vol",
    "amount",
    "servertime",
]


class TdxCliError(RuntimeError):
    pass


def clean_code(value: str) -> str:
    text = str(value).strip().upper()
    match = re.fullmatch(r"(?:(?:SH|SZ)[.:]?)?(\d{6})(?:[.:]?(?:SH|SZ))?", text)
    if not match:
        raise TdxCliError(f"Invalid security code: {value!r}; expected a six-digit Shanghai/Shenzhen code")
    return match.group(1)


def select_market(code: str) -> int:
    clean = clean_code(code)
    if clean[0] in {"5", "6", "9"} or clean[:3] in {
        "009",
        "126",
        "110",
        "201",
        "202",
        "203",
        "204",
    }:
        return 1
    return 0


def market_name(market: int) -> str:
    return "Shanghai" if market == 1 else "Shenzhen"


def parse_market(value: str) -> int:
    normalized = str(value).strip().lower()
    if normalized in {"1", "sh", "sha", "shanghai"}:
        return 1
    if normalized in {"0", "sz", "sza", "shenzhen"}:
        return 0
    raise TdxCliError(f"Unsupported market {value!r}; use sh/1 or sz/0")


def positive_int(value: str, *, maximum: int | None = None) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    if maximum is not None and number > maximum:
        raise argparse.ArgumentTypeError(f"must be at most {maximum}")
    return number


def nonnegative_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return number


def normalize(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def require_rows(data: Any, label: str) -> list[dict[str, Any]]:
    if not data:
        raise TdxCliError(f"TDX returned empty {label}; no fallback was attempted")
    if isinstance(data, Mapping):
        return [dict(data)]
    rows = [dict(row) for row in data]
    if not rows:
        raise TdxCliError(f"TDX returned empty {label}; no fallback was attempted")
    return rows


def socket_probe(host: tuple[str, str, int], timeout: float) -> tuple[float, str, str, int] | None:
    name, ip, port = host
    started = time.perf_counter()
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return time.perf_counter() - started, name, ip, port
    except OSError:
        return None


def verify_server(name: str, ip: str, port: int, timeout: float) -> dict[str, Any] | None:
    started = time.perf_counter()
    try:
        api = TdxHq_API(raise_exception=True)
        with api.connect(ip, port, time_out=timeout):
            count = api.get_security_count(0)
            quote = api.get_security_quotes([(0, "000001")])
        if not count or not quote:
            return None
        return {
            "name": name,
            "ip": ip,
            "port": port,
            "security_count": count,
            "verified_ms": round((time.perf_counter() - started) * 1000, 1),
        }
    except Exception:
        return None


def auto_select_server(timeout: float) -> dict[str, Any]:
    socket_timeout = min(max(timeout, 0.25), 1.0)
    reachable: list[tuple[float, str, str, int]] = []
    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = [executor.submit(socket_probe, host, socket_timeout) for host in hq_hosts]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                reachable.append(result)

    if not reachable:
        raise TdxCliError("No reachable TDX quote server was found")

    reachable.sort(key=lambda item: item[0])
    for latency, name, ip, port in reachable[:24]:
        verified = verify_server(name, ip, port, timeout)
        if verified is not None:
            verified["socket_ms"] = round(latency * 1000, 1)
            verified["selection"] = "automatic"
            return verified

    raise TdxCliError("Reachable TDX servers did not return a usable realtime quote")


def resolve_server(args: argparse.Namespace) -> dict[str, Any]:
    explicit_ip = args.ip or os.environ.get("TDX_IP")
    explicit_port = args.port
    if explicit_port is None:
        explicit_port = int(os.environ.get("TDX_PORT", "7709"))

    if not explicit_ip:
        return auto_select_server(args.timeout)

    name = "explicit"
    verified = verify_server(name, explicit_ip, explicit_port, args.timeout)
    if verified is None:
        raise TdxCliError(
            f"Explicit TDX server {explicit_ip}:{explicit_port} did not return a usable realtime quote; "
            "no alternate server was tried"
        )
    verified["selection"] = "explicit"
    return verified


@contextmanager
def connect(args: argparse.Namespace):
    server = resolve_server(args)
    api = TdxHq_API(raise_exception=True)
    with api.connect(server["ip"], server["port"], time_out=args.timeout):
        yield api, server


def metadata(command: str, server: Mapping[str, Any], count: int, **extra: Any) -> dict[str, Any]:
    result = {
        "provider": "pytdx",
        "command": command,
        "server": f"{server['ip']}:{server['port']}",
        "server_name": server.get("name"),
        "server_selection": server.get("selection"),
        "retrieved_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "count": count,
    }
    result.update(extra)
    return result


def format_scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def table_text(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    values = [[format_scalar(row.get(column)) for column in columns] for row in rows]
    widths = [len(column) for column in columns]
    for row in values:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    header = " | ".join(column.ljust(widths[index]) for index, column in enumerate(columns))
    divider = "-+-".join("-" * width for width in widths)
    body = [" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) for row in values]
    return "\n".join([header, divider, *body])


def emit(
    meta: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    output_format: str,
    *,
    pretty: bool,
    columns: Sequence[str] | None = None,
) -> None:
    clean_rows = normalize(list(rows))
    clean_meta = normalize(dict(meta))
    if output_format == "json":
        indent = 2 if pretty else None
        print(json.dumps({"meta": clean_meta, "data": clean_rows}, ensure_ascii=False, indent=indent))
        return

    if not clean_rows:
        raise TdxCliError("No rows are available for output")
    selected = list(columns or clean_rows[0].keys())
    if output_format == "csv":
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=selected, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(clean_rows)
        print(buffer.getvalue(), end="")
        return

    print(
        f"provider={clean_meta['provider']} server={clean_meta['server']} "
        f"retrieved_at={clean_meta['retrieved_at']} count={clean_meta['count']}"
    )
    print(table_text(clean_rows, selected))


def quote_rows(api: TdxHq_API, codes: Iterable[str], raw: bool) -> list[dict[str, Any]]:
    clean_codes = [clean_code(code) for code in codes]
    if not clean_codes:
        raise TdxCliError("At least one security code is required")
    if len(clean_codes) > 80:
        raise TdxCliError("A single quote request supports at most 80 securities; split the request into batches")

    pairs = [(select_market(code), code) for code in clean_codes]
    rows = require_rows(api.get_security_quotes(pairs), "realtime quote")
    returned = {str(row.get("code")) for row in rows}
    missing = [code for code in clean_codes if code not in returned]
    if missing:
        raise TdxCliError(f"TDX omitted requested quote codes: {', '.join(missing)}")

    normalized_rows = []
    for row in rows:
        code = str(row["code"])
        row["market_name"] = market_name(select_market(code))
        price = row.get("price")
        last_close = row.get("last_close")
        if price is not None and last_close not in {None, 0}:
            row["change"] = round(float(price) - float(last_close), 6)
            row["change_pct"] = round((float(price) / float(last_close) - 1) * 100, 6)
        else:
            row["change"] = None
            row["change_pct"] = None
        normalized_rows.append(row if raw else {field: row.get(field) for field in QUOTE_FIELDS})
    return normalized_rows


def run_command(args: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, Any]], list[str] | None]:
    if args.command == "server":
        server = resolve_server(args)
        row = {
            "name": server.get("name"),
            "ip": server["ip"],
            "port": server["port"],
            "selection": server.get("selection"),
            "socket_ms": server.get("socket_ms"),
            "verified_ms": server.get("verified_ms"),
            "security_count": server.get("security_count"),
        }
        return metadata("server", server, 1), [row], list(row.keys())

    with connect(args) as (api, server):
        if args.command == "quote":
            rows = quote_rows(api, args.codes, args.raw)
            meta = metadata(
                "quote",
                server,
                len(rows),
                quote_date_note="TDX realtime quote contains server time but no complete trading date; confirm with bars",
            )
            return meta, rows, None if args.raw else QUOTE_FIELDS

        if args.command == "bars":
            code = clean_code(args.code)
            rows = require_rows(
                api.get_security_bars(PERIODS[args.period], select_market(code), code, args.start, args.count),
                f"{args.period} bars",
            )
            for row in rows:
                row.setdefault("code", code)
            meta = metadata(
                "bars",
                server,
                len(rows),
                code=code,
                period=args.period,
                adjustment="raw_unadjusted",
            )
            return meta, rows, None

        if args.command == "ticks":
            code = clean_code(args.code)
            rows = require_rows(
                api.get_transaction_data(select_market(code), code, args.start, args.count),
                "realtime ticks",
            )
            for row in rows:
                row.setdefault("code", code)
            return metadata("ticks", server, len(rows), code=code), rows, None

        if args.command == "history-ticks":
            code = clean_code(args.code)
            rows = require_rows(
                api.get_history_transaction_data(
                    select_market(code), code, args.start, args.count, int(args.date)
                ),
                f"historical ticks for {args.date}",
            )
            for row in rows:
                row.setdefault("code", code)
                row.setdefault("date", args.date)
            return metadata("history-ticks", server, len(rows), code=code, date=args.date), rows, None

        if args.command == "securities":
            market = parse_market(args.market)
            rows = require_rows(api.get_security_list(market, args.start), "security list")
            return metadata(
                "securities", server, len(rows), market=market_name(market), start=args.start
            ), rows, None

        if args.command == "xdxr":
            code = clean_code(args.code)
            rows = require_rows(api.get_xdxr_info(select_market(code), code), "corporate-action records")
            return metadata("xdxr", server, len(rows), code=code), rows, None

        if args.command == "finance":
            code = clean_code(args.code)
            rows = require_rows(api.get_finance_info(select_market(code), code), "finance data")
            return metadata("finance", server, len(rows), code=code), rows, None

        if args.command == "block":
            rows = require_rows(api.get_and_parse_block_info(args.file), f"block file {args.file}")
            if args.name:
                target = args.name.casefold()
                rows = [row for row in rows if target in str(row.get("blockname", "")).casefold()]
            if args.code:
                code = clean_code(args.code)
                rows = [row for row in rows if str(row.get("code", "")) == code]
            if not rows:
                raise TdxCliError("No trustworthy block rows matched the requested filter")
            return metadata("block", server, len(rows), file=args.file), rows, None

    raise TdxCliError(f"Unsupported command: {args.command}")


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ip", help="Explicit TDX server IP; disables automatic fallback")
    parser.add_argument("--port", type=int, help="TDX server port, normally 7709")
    parser.add_argument("--timeout", type=float, default=2.0, help="Connection timeout in seconds")
    parser.add_argument("--format", choices=["json", "csv", "table"], default="json")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read Shanghai/Shenzhen market data from TDX through pytdx"
    )
    common = argparse.ArgumentParser(add_help=False)
    add_common_arguments(common)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("server", parents=[common], help="Find and verify a usable quote server")

    quote = subparsers.add_parser("quote", parents=[common], help="Fetch realtime quotes")
    quote.add_argument("codes", nargs="+", help="One to 80 six-digit security codes")
    quote.add_argument("--raw", action="store_true", help="Include the original full quote fields")

    bars = subparsers.add_parser("bars", parents=[common], help="Fetch price bars")
    bars.add_argument("code")
    bars.add_argument("--period", choices=list(PERIODS), default="day")
    bars.add_argument("--start", type=nonnegative_int, default=0, help="Pagination offset")
    bars.add_argument("--count", type=lambda value: positive_int(value, maximum=800), default=20)

    ticks = subparsers.add_parser("ticks", parents=[common], help="Fetch realtime transaction ticks")
    ticks.add_argument("code")
    ticks.add_argument("--start", type=nonnegative_int, default=0)
    ticks.add_argument("--count", type=lambda value: positive_int(value, maximum=2000), default=2000)

    history = subparsers.add_parser(
        "history-ticks", parents=[common], help="Fetch historical transaction ticks"
    )
    history.add_argument("code")
    history.add_argument("--date", required=True, type=lambda value: validate_date(value))
    history.add_argument("--start", type=nonnegative_int, default=0)
    history.add_argument("--count", type=lambda value: positive_int(value, maximum=2000), default=2000)

    securities = subparsers.add_parser("securities", parents=[common], help="Fetch a security list page")
    securities.add_argument("--market", required=True, help="sh/1 or sz/0")
    securities.add_argument("--start", type=nonnegative_int, default=0)

    xdxr = subparsers.add_parser("xdxr", parents=[common], help="Fetch corporate-action records")
    xdxr.add_argument("code")

    finance = subparsers.add_parser("finance", parents=[common], help="Fetch TDX finance data")
    finance.add_argument("code")

    block = subparsers.add_parser("block", parents=[common], help="Read and filter a TDX block file")
    block.add_argument(
        "--file",
        default="block_gn.dat",
        choices=["block.dat", "block_zs.dat", "block_fg.dat", "block_gn.dat", "incon.dat"],
    )
    block.add_argument("--name", help="Case-insensitive block-name substring")
    block.add_argument("--code", help="Filter by security code")
    return parser


def validate_date(value: str) -> str:
    text = str(value).strip()
    if not re.fullmatch(r"\d{8}", text):
        raise argparse.ArgumentTypeError("date must use YYYYMMDD")
    try:
        datetime.strptime(text, "%Y%m%d")
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must be a real calendar date in YYYYMMDD form") from exc
    return text


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    if args.command == "block" and not (args.name or args.code):
        parser.error("block requires --name and/or --code to avoid dumping an entire block file")

    try:
        meta, rows, columns = run_command(args)
        emit(meta, rows, args.format, pretty=args.pretty, columns=columns)
        return 0
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        error = {
            "error": {
                "type": type(exc).__name__,
                "message": str(exc),
                "fallback_attempted": False,
            }
        }
        print(json.dumps(error, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

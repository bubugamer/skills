#!/usr/bin/env python3
from __future__ import annotations

import argparse
import unittest
from unittest.mock import patch

import pandas as pd

import akshare_api


class CodeParsingTests(unittest.TestCase):
    def test_common_code_forms(self) -> None:
        self.assertEqual(akshare_api.clean_code("600000.SH"), "600000")
        self.assertEqual(akshare_api.clean_code("SZ000001"), "000001")
        self.assertEqual(akshare_api.clean_code("bj920000"), "920000")

    def test_invalid_code_is_rejected(self) -> None:
        with self.assertRaises(akshare_api.AkshareCliError):
            akshare_api.clean_code("AAPL")


class ParameterTests(unittest.TestCase):
    def test_parameter_json_and_string_values(self) -> None:
        self.assertEqual(akshare_api.parse_parameter("count=12"), ("count", 12))
        self.assertEqual(akshare_api.parse_parameter("enabled=true"), ("enabled", True))
        self.assertEqual(akshare_api.parse_parameter("symbol=半导体"), ("symbol", "半导体"))

    def test_bad_parameter_is_rejected(self) -> None:
        with self.assertRaises(akshare_api.AkshareCliError):
            akshare_api.parse_parameter("symbol")


class SourceTests(unittest.TestCase):
    def test_source_suffixes(self) -> None:
        self.assertIn("同花顺", akshare_api.infer_source("fund_etf_spot_ths"))
        self.assertIn("东方财富", akshare_api.infer_source("stock_zh_a_spot_em"))


class QuoteTests(unittest.TestCase):
    def make_args(self, codes: list[str], raw: bool = False) -> argparse.Namespace:
        return argparse.Namespace(codes=codes, raw=raw, source="em")

    def test_quote_preserves_request_order(self) -> None:
        frame = pd.DataFrame(
            [
                {"代码": "603533", "名称": "掌阅科技", "最新价": 20.0, "昨收": 19.0},
                {"代码": "002432", "名称": "九安医疗", "最新价": 70.0, "昨收": 71.0},
            ]
        )
        with patch.object(akshare_api, "call_ak", return_value=frame):
            result = akshare_api.quote_command(self.make_args(["002432", "603533"]))
        self.assertEqual(result.data["代码"].tolist(), ["002432", "603533"])

    def test_missing_quote_code_fails(self) -> None:
        frame = pd.DataFrame([{"代码": "002432", "名称": "九安医疗", "最新价": 70.0}])
        with patch.object(akshare_api, "call_ak", return_value=frame):
            with self.assertRaisesRegex(akshare_api.AkshareCliError, "omitted requested codes"):
                akshare_api.quote_command(self.make_args(["002432", "603533"]))


class EmptyTableTests(unittest.TestCase):
    def test_empty_table_has_no_silent_fallback(self) -> None:
        with self.assertRaisesRegex(akshare_api.AkshareCliError, "no provider fallback"):
            akshare_api.ensure_dataframe(pd.DataFrame(), "example")


class LimitTests(unittest.TestCase):
    def test_tail_returns_latest_rows(self) -> None:
        frame = pd.DataFrame({"value": [1, 2, 3, 4]})
        result = akshare_api.apply_limit(frame, None, 2)
        self.assertEqual(result["value"].tolist(), [3, 4])

    def test_limit_and_tail_are_mutually_exclusive(self) -> None:
        with self.assertRaises(akshare_api.AkshareCliError):
            akshare_api.apply_limit([1, 2], 1, 1)


if __name__ == "__main__":
    unittest.main()

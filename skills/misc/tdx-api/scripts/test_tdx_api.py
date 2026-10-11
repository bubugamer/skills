#!/usr/bin/env python3
from __future__ import annotations

import unittest

import tdx_api


class CodeParsingTests(unittest.TestCase):
    def test_common_code_forms(self) -> None:
        self.assertEqual(tdx_api.clean_code("600000.SH"), "600000")
        self.assertEqual(tdx_api.clean_code("SZ000001"), "000001")
        self.assertEqual(tdx_api.clean_code("sh600000"), "600000")

    def test_invalid_code_is_rejected(self) -> None:
        with self.assertRaises(tdx_api.TdxCliError):
            tdx_api.clean_code("AAPL")

    def test_market_mapping(self) -> None:
        self.assertEqual(tdx_api.select_market("603533"), 1)
        self.assertEqual(tdx_api.select_market("110001"), 1)
        self.assertEqual(tdx_api.select_market("002432"), 0)
        self.assertEqual(tdx_api.select_market("300133"), 0)


class QuoteTests(unittest.TestCase):
    def test_empty_realtime_quote_fails_without_fallback(self) -> None:
        class EmptyApi:
            def get_security_quotes(self, pairs):
                return []

        with self.assertRaisesRegex(tdx_api.TdxCliError, "no fallback was attempted"):
            tdx_api.quote_rows(EmptyApi(), ["002432"], raw=False)

    def test_change_fields_are_calculated(self) -> None:
        class QuoteApi:
            def get_security_quotes(self, pairs):
                return [
                    {
                        "code": "002432",
                        "price": 11.0,
                        "last_close": 10.0,
                        "open": 10.2,
                        "high": 11.1,
                        "low": 10.1,
                        "vol": 100,
                        "amount": 1000.0,
                        "servertime": "15:00:00.000",
                    }
                ]

        row = tdx_api.quote_rows(QuoteApi(), ["002432"], raw=False)[0]
        self.assertEqual(row["change"], 1.0)
        self.assertEqual(row["change_pct"], 10.0)

    def test_missing_requested_code_is_not_silently_dropped(self) -> None:
        class PartialApi:
            def get_security_quotes(self, pairs):
                return [{"code": "002432", "price": 1.0, "last_close": 1.0}]

        with self.assertRaisesRegex(tdx_api.TdxCliError, "omitted requested quote codes"):
            tdx_api.quote_rows(PartialApi(), ["002432", "603533"], raw=False)


class ValidationTests(unittest.TestCase):
    def test_date_validation(self) -> None:
        self.assertEqual(tdx_api.validate_date("20260720"), "20260720")
        with self.assertRaises(Exception):
            tdx_api.validate_date("20260230")


if __name__ == "__main__":
    unittest.main()

import copy
import unittest
from unittest.mock import Mock, patch

import update_data as app


class FubonTests(unittest.TestCase):
    def fetch(self, rows, kind="nav", return_code="0000"):
        response = Mock()
        response.json.return_value = {"returnCode": return_code, "data": rows}
        with patch.object(app.requests, "post", return_value=response) as post:
            result = app.fetch_fubon_value("DSP5", kind, "USD")
        self.assertEqual(post.call_args.kwargs["json"]["assetFbCode"], "DSP5")
        self.assertEqual(post.call_args.kwargs["timeout"], 30)
        return result

    def test_latest_nav_not_response_order(self):
        self.assertEqual(self.fetch([
            {"date": "2025/01/02", "nav": "8.1"},
            {"date": "2025/01/03", "nav": "8.2"},
            {"date": "2099/01/01", "nav": "9"},
        ]), (8.2, "2025-01-03"))

    def test_ex_date_and_per_unit_amount(self):
        self.assertEqual(self.fetch([{
            "recordDate": "2025/01/14", "dividendDate": "2025/01/15",
            "currencyCode": "USD", "dividendPerUnit": 0.06,
            "dividendAmount": "0.06",
        }], "distribution"), (0.06, "2025-01-15"))

    def test_reject_invalid_responses(self):
        for rows in ([], [{"date": "2025/02/30", "nav": "8"}],
                     [{"date": "2025/01/01", "nav": "NaN"}],
                     [{"date": "2025/01/01", "nav": "0"}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                self.fetch(rows)
        with self.assertRaises(ValueError):
            self.fetch([], return_code="9999")
        with self.assertRaises(ValueError):
            self.fetch([{"dividendDate": "2025/01/15", "currencyCode": "TWD",
                         "dividendPerUnit": 0.06, "dividendAmount": "0.06"}], "distribution")

    def test_failure_preserves_values_and_dates(self):
        original = {"currency": "USD", "nav": 8.4, "nav_date": "2025-01-03",
                    "distribution": 0.055, "distribution_date": "2025-01-02"}
        for result in (RuntimeError("network failure"), (8.1, "2025-01-01")):
            data, errors = {"funds": {"DSP5": copy.deepcopy(original)}}, {}
            options = {"side_effect": result} if isinstance(result, Exception) else {"return_value": result}
            with patch.dict(app.FUNDS, {"DSP5": app.FUNDS["DSP5"]}, clear=True), \
                    patch.object(app, "fetch_fubon_value", **options):
                app.update_funds(data, errors)
            self.assertEqual(data["funds"]["DSP5"], original)
            self.assertEqual(set(errors), {"DSP5_nav", "DSP5_distribution"})


if __name__ == "__main__":
    unittest.main()

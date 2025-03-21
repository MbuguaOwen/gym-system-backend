import unittest
from datetime import datetime, timedelta  # Add timedelta
from expiry_date import calculate_expiry

class TestCalculateExpiry(unittest.TestCase):
    def setUp(self):
        self.start_date = datetime(2025, 3, 21)  # Fixed test date

    def test_monthly(self):
        expected = self.start_date.replace(day=20, month=4)  # April 20, 2025
        self.assertEqual(calculate_expiry(self.start_date, "monthly"), expected)

    def test_six_months(self):
        expected = self.start_date.replace(day=19, month=9)  # September 19, 2025
        self.assertEqual(calculate_expiry(self.start_date, "6 months"), expected)

    def test_yearly(self):
        expected = self.start_date.replace(year=2026)  # March 21, 2026
        self.assertEqual(calculate_expiry(self.start_date, "yearly"), expected)

    def test_manual_days(self):
        expected = self.start_date + timedelta(days=100)  # June 29, 2025
        self.assertEqual(calculate_expiry(self.start_date, 100), expected)

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            calculate_expiry(self.start_date, "random")

if __name__ == '__main__':
    unittest.main()

"""Тесты подсчёта простых чисел меньше N."""

import io
from pathlib import Path
import runpy
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch


SOURCE = Path(__file__).resolve().with_name("source_prime.py")


class PrimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # input() вызывается при загрузке модуля.
        with patch("builtins.input", return_value="3"), redirect_stdout(io.StringIO()):
            namespace = runpy.run_path(str(SOURCE))
        cls.get_primes = staticmethod(namespace["get_primes"])

    def test_no_primes(self):
        for limit in (-100, -1, 0, 1, 2):
            with self.subTest(N=limit):
                self.assertEqual(self.get_primes(limit), 0)

    def test_small_values(self):
        for limit, expected in ((3, 1), (4, 2), (5, 2), (6, 3), (7, 3), (8, 4)):
            with self.subTest(N=limit):
                self.assertEqual(self.get_primes(limit), expected)

    def test_strict_upper_bound(self):
        for limit, expected in ((11, 4), (12, 5), (97, 24), (98, 25)):
            with self.subTest(N=limit):
                self.assertEqual(self.get_primes(limit), expected)

    def test_prime_squares(self):
        for square, expected in ((9, 4), (25, 9), (49, 15), (121, 30)):
            for limit in (square - 1, square, square + 1):
                with self.subTest(N=limit):
                    self.assertEqual(self.get_primes(limit), expected)

    def test_larger_values(self):
        for limit, expected in ((100, 25), (1000, 168), (10000, 1229)):
            with self.subTest(N=limit):
                self.assertEqual(self.get_primes(limit), expected)

    def test_program_input_output(self):
        cases = (
            ("-1\n", "0\n"),
            ("0\n", "0\n"),
            ("1\n", "0\n"),
            ("2\n", "0\n"),
            ("3\n", "1\n"),
            ("20\n", "8\n"),
            ("26\n", "9\n"),
            ("  100  \n", "25\n"),
        )
        for input_text, expected in cases:
            with self.subTest(input=input_text.strip()):
                result = subprocess.run(
                    [sys.executable, str(SOURCE)],
                    input=input_text,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected)
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()

"""Тесты максимальной чётной суммы."""

import io
from pathlib import Path
import runpy
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch


SOURCE = Path(__file__).resolve().with_name("source_sum.py")


class SumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # input() вызывается при загрузке модуля.
        with patch("builtins.input", return_value="2"), redirect_stdout(io.StringIO()):
            namespace = runpy.run_path(str(SOURCE))
        cls.maximize_sum = staticmethod(namespace["maximize_sum"])

    def test_single_number(self):
        for numbers, expected in (([1], 0), ([7], 0), ([2], 2), ([8], 8)):
            with self.subTest(numbers=numbers):
                self.assertEqual(self.maximize_sum(numbers), expected)

    def test_only_even_numbers(self):
        for numbers, expected in (([2, 4, 6], 12), ([2, 2, 2], 6), ([100, 200], 300)):
            with self.subTest(numbers=numbers):
                self.assertEqual(self.maximize_sum(numbers), expected)

    def test_even_sum_with_odd_numbers(self):
        cases = (([1, 3], 4), ([1, 2, 3], 6), ([7, 7], 14), ([3, 5, 7, 9], 24))
        for numbers, expected in cases:
            with self.subTest(numbers=numbers):
                self.assertEqual(self.maximize_sum(numbers), expected)

    def test_odd_sum(self):
        cases = (
            ([2, 3, 4], 6),
            ([3, 4, 6], 10),
            ([7, 2, 5, 8, 3], 22),
            ([9, 3, 5], 14),
        )
        for numbers, expected in cases:
            with self.subTest(numbers=numbers):
                self.assertEqual(self.maximize_sum(numbers), expected)

    def test_minimum_odd_position(self):
        for numbers in ([1, 5, 9, 2], [5, 1, 9, 2], [5, 9, 2, 1]):
            with self.subTest(numbers=numbers):
                self.assertEqual(self.maximize_sum(numbers), 16)

    def test_repeated_odd_numbers(self):
        for numbers, expected in (([5, 5, 5], 10), ([1, 1, 1], 2), ([3, 3, 3, 2], 8)):
            with self.subTest(numbers=numbers):
                self.assertEqual(self.maximize_sum(numbers), expected)

    def test_iterator(self):
        numbers = map(int, ["7", "2", "5", "8", "3"])
        self.assertEqual(self.maximize_sum(numbers), 22)

    def test_program_input_output(self):
        cases = (
            ("7 2 5 8 3\n", "22\n"),
            ("2 4 6\n", "12\n"),
            ("7\n", "0\n"),
            ("  1   2\t3  \n", "6\n"),
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

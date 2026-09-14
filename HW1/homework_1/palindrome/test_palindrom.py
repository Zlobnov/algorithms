"""Тесты проверки положительного числа на палиндром."""

import io
from pathlib import Path
import runpy
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch


SOURCE = Path(__file__).resolve().with_name("source_palindrom.py")


class PalindromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # input() вызывается при загрузке модуля.
        with patch("builtins.input", return_value="1"), redirect_stdout(io.StringIO()):
            namespace = runpy.run_path(str(SOURCE))
        cls.is_palindrome = staticmethod(namespace["is_palindrome"])

    def test_all_single_digit_numbers(self):
        for number in range(1, 10):
            with self.subTest(number=number):
                self.assertIs(self.is_palindrome(number), True)

    def test_palindromes(self):
        cases = (
            11, 22, 99, 101, 121, 999, 1001, 1221, 11111,
            12321, 10001, 12021, 120021, 1002001, 1234321, 12344321,
        )
        for number in cases:
            with self.subTest(number=number):
                self.assertIs(self.is_palindrome(number), True)

    def test_different_outer_digits(self):
        for number in (12, 21, 123, 321, 1234, 987654, 123456789):
            with self.subTest(number=number):
                self.assertIs(self.is_palindrome(number), False)

    def test_matching_outer_digits_but_different_inner_digits(self):
        for number in (1231, 12031, 10021, 123421, 12345321):
            with self.subTest(number=number):
                self.assertIs(self.is_palindrome(number), False)

    def test_trailing_zeros(self):
        for number in (10, 20, 100, 110, 1010, 10010, 123210):
            with self.subTest(number=number):
                self.assertIs(self.is_palindrome(number), False)

    def test_decimal_length_boundaries(self):
        for exponent in (1, 2, 3, 9, 18, 50, 120):
            power = 10 ** exponent
            for number, expected in (
                (power - 1, True),  # Только девятки.
                (power, False),  # Единица и нули.
                (power + 1, True),  # Единицы по краям, нули внутри.
            ):
                with self.subTest(exponent=exponent, number=number):
                    self.assertIs(self.is_palindrome(number), expected)

    def test_large_number_with_inner_mismatch(self):
        # В числе из 121 цифры единица на позиции 59 не имеет пары на позиции 61.
        number = 10 ** 120 + 10 ** 59 + 1
        self.assertIs(self.is_palindrome(number), False)


class ProgramTests(unittest.TestCase):
    def test_stdin_and_stdout(self):
        for input_text, expected in (
            ("1\n", "True\n"),
            ("12344321\n", "True\n"),
            ("123421\n", "False\n"),
            ("10\n", "False\n"),
        ):
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

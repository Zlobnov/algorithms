import io
import itertools
from pathlib import Path
import runpy
import unittest
from contextlib import redirect_stdout

from source_two_sum import two_sum


class TwoSumTests(unittest.TestCase):
    def assert_pair(self, arr, k, expected):
        original = arr.copy()
        result = two_sum(arr, k)
        self.assertEqual(result, expected)
        self.assertLess(result[0], result[1])
        self.assertEqual(arr[result[0]] + arr[result[1]], k)
        self.assertEqual(arr, original)

    def test_examples(self):
        self.assert_pair([1, 3, 4, 10], 7, (1, 2))
        self.assert_pair([5, 5, 1, 4], 10, (0, 1))

    def test_two_elements(self):
        self.assert_pair([7, -2], 5, (0, 1))

    def test_cannot_use_same_element_twice(self):
        self.assert_pair([3, 1, 5], 6, (1, 2))

    def test_equal_values_at_different_indices(self):
        self.assert_pair([3, 8, 3], 6, (0, 2))

    def test_negative_values(self):
        self.assert_pair([-8, 3, -2, 7], -10, (0, 2))

    def test_zero_target(self):
        self.assert_pair([7, 2, -7, 9], 0, (0, 2))

    def test_zero_in_pair(self):
        self.assert_pair([0, -1, 6, 8], 8, (0, 3))

    def test_two_zeros(self):
        self.assert_pair([4, 0, 8, 0], 0, (1, 3))

    def test_repeated_unrelated_values(self):
        self.assert_pair([1, 1, 1, 3, 5], 8, (3, 4))

    def test_pair_at_end(self):
        self.assert_pair([7, 2, 11, -5], 6, (2, 3))

    def test_trace_example(self):
        self.assert_pair([8, -3, 4, 8, 6, 2], 3, (1, 4))

    def test_large_integers(self):
        self.assert_pair([-10**30, 7, 10**30 + 3], 3, (0, 2))

    def test_long_array(self):
        self.assert_pair(list(range(5000)) + [10000], 14999, (4999, 5000))

    def test_exhaustive_unique_pairs(self):
        checked = 0
        for length in range(2, 6):
            for values in itertools.product(range(-2, 3), repeat=length):
                for k in range(-4, 5):
                    pairs = [
                        (i, j)
                        for i in range(length)
                        for j in range(i + 1, length)
                        if values[i] + values[j] == k
                    ]
                    if len(pairs) == 1:
                        with self.subTest(arr=values, k=k):
                            self.assert_pair(list(values), k, pairs[0])
                        checked += 1
        self.assertGreater(checked, 1000)

    def test_demo_prints_indices_separated_by_space(self):
        output = io.StringIO()
        with redirect_stdout(output):
            runpy.run_path(
                str(Path(__file__).with_name("source_two_sum.py")),
                run_name="__main__",
            )
        self.assertEqual(output.getvalue(), "1 2\n")


if __name__ == "__main__":
    unittest.main()

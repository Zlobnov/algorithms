import unittest

from source_validate import validate_stack_sequences


class ValidateTests(unittest.TestCase):
    def test_valid_example(self):
        self.assertIs(
            validate_stack_sequences([1, 2, 3, 4, 5], [1, 3, 5, 4, 2]),
            True,
        )

    def test_invalid_example(self):
        self.assertIs(validate_stack_sequences([1, 2, 3], [3, 1, 2]), False)

    def test_single_element(self):
        self.assertIs(validate_stack_sequences([0], [0]), True)

    def test_same_order(self):
        self.assertIs(validate_stack_sequences([4, 1, 7, 2], [4, 1, 7, 2]), True)

    def test_reverse_order(self):
        self.assertIs(validate_stack_sequences([4, 1, 7, 2], [2, 7, 1, 4]), True)

    def test_interleaved_pushes_and_pops(self):
        self.assertIs(
            validate_stack_sequences([1, 2, 3, 4, 5, 6], [2, 4, 3, 6, 5, 1]),
            True,
        )

    def test_mismatch_after_valid_prefix(self):
        self.assertIs(
            validate_stack_sequences([1, 2, 3, 4, 5], [2, 4, 1, 5, 3]),
            False,
        )

    def test_signed_values(self):
        pushed = [-10, 0, 7, -3]
        self.assertIs(validate_stack_sequences(pushed, [0, -3, 7, -10]), True)
        self.assertIs(validate_stack_sequences(pushed, [-3, 0, 7, -10]), False)

    def test_inputs_are_unchanged(self):
        for popped in ([1, 3, 2], [3, 1, 2]):
            pushed = [1, 2, 3]
            original_pushed = pushed.copy()
            original_popped = popped.copy()
            with self.subTest(popped=popped):
                validate_stack_sequences(pushed, popped)
                self.assertEqual(pushed, original_pushed)
                self.assertEqual(popped, original_popped)

    def test_maximum_length(self):
        pushed = list(range(100_000))
        cases = (
            (pushed.copy(), True),
            (pushed[::-1], True),
            ([99_999, 0] + list(range(1, 99_999)), False),
        )
        for popped, expected in cases:
            with self.subTest(first=popped[0], second=popped[1]):
                self.assertIs(validate_stack_sequences(pushed, popped), expected)


if __name__ == "__main__":
    unittest.main()

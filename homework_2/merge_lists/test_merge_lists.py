import unittest

from source_merge_lists import Node, merge_with_dummy, merge_without_dummy


def make_list(values):
    nodes = [Node(value) for value in values]
    for current, following in zip(nodes, nodes[1:]):
        current.next = following
    return (nodes[0] if nodes else None), nodes


class MergeListsTests(unittest.TestCase):
    def assert_merged(self, values1, values2, expected):
        for merge in (merge_with_dummy, merge_without_dummy):
            with self.subTest(method=merge.__name__):
                list1, nodes1 = make_list(values1)
                list2, nodes2 = make_list(values2)
                original_nodes = nodes1 + nodes2
                current = merge(list1, list2)
                result = []
                seen = set()

                while current is not None:
                    self.assertNotIn(id(current), seen, "В результате появился цикл")
                    self.assertLess(len(result), len(original_nodes))
                    seen.add(id(current))
                    result.append(current.value)
                    current = current.next

                self.assertEqual(result, expected)
                self.assertEqual(seen, {id(node) for node in original_nodes})

    def test_both_empty(self):
        self.assert_merged([], [], [])

    def test_first_empty(self):
        self.assert_merged([], [-2, 0, 5], [-2, 0, 5])

    def test_second_empty(self):
        self.assert_merged([-2, 0, 5], [], [-2, 0, 5])

    def test_singletons(self):
        for first, second in ((1, 2), (2, 1), (1, 1)):
            with self.subTest(first=first, second=second):
                self.assert_merged([first], [second], sorted([first, second]))

    def test_example(self):
        self.assert_merged([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4])

    def test_interleaved(self):
        self.assert_merged([1, 3, 5, 7], [2, 4, 6, 8], list(range(1, 9)))

    def test_separated_ranges(self):
        for first, second in (([1, 2, 3], [7, 8]), ([7, 8], [1, 2, 3])):
            with self.subTest(first=first):
                self.assert_merged(first, second, [1, 2, 3, 7, 8])

    def test_equal_values(self):
        self.assert_merged([2, 2, 2], [2, 2], [2, 2, 2, 2, 2])

    def test_negative_values_and_zero(self):
        self.assert_merged([-7, -3, 0, 4], [-5, -3, 0], [-7, -5, -3, -3, 0, 0, 4])

    def test_uneven_lengths(self):
        for first, second in (([4], [1, 2, 3, 5, 6]), ([1, 2, 3, 5, 6], [4])):
            with self.subTest(first=first):
                self.assert_merged(first, second, [1, 2, 3, 4, 5, 6])

    def test_long_lists(self):
        self.assert_merged(list(range(0, 2000, 2)), list(range(1, 2000, 2)), list(range(2000)))


if __name__ == "__main__":
    unittest.main()

import random
import unittest
from collections import Counter

from source_anagrams import group_anagrams


def normalized(groups):
    """Сравнить разбиения без требований к порядку групп и слов."""
    return sorted(tuple(sorted(group)) for group in groups)


def count_oracle(words):
    """Независимый ключ: множество пар (символ, число вхождений)."""
    groups = {}
    for word in words:
        signature = frozenset(Counter(word).items())
        groups.setdefault(signature, []).append(word)
    return list(groups.values())


class AnagramsTests(unittest.TestCase):
    def assertGroupsEqual(self, actual, expected):
        self.assertEqual(normalized(actual), normalized(expected))

    def test_example(self):
        words = ["eat", "tea", "tan", "ate", "nat", "bat"]
        self.assertGroupsEqual(
            group_anagrams(words),
            [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
        )

    def test_empty_input(self):
        self.assertEqual(group_anagrams([]), [])

    def test_empty_strings_and_duplicates(self):
        self.assertGroupsEqual(
            group_anagrams(["", "ab", "", "ba", "ab"]),
            [["", ""], ["ab", "ba", "ab"]],
        )

    def test_single_word(self):
        self.assertEqual(group_anagrams(["alone"]), [["alone"]])

    def test_all_words_are_anagrams(self):
        self.assertGroupsEqual(
            group_anagrams(["aab", "aba", "baa", "aab"]),
            [["aab", "aba", "baa", "aab"]],
        )

    def test_all_groups_are_distinct(self):
        self.assertGroupsEqual(
            group_anagrams(["a", "b", "ab", "abc"]),
            [["a"], ["b"], ["ab"], ["abc"]],
        )

    def test_character_counts_matter(self):
        self.assertGroupsEqual(
            group_anagrams(["ab", "aab", "abb", "baa", "bba", "ba"]),
            [["ab", "ba"], ["aab", "baa"], ["abb", "bba"]],
        )

    def test_unicode_case_and_other_characters(self):
        self.assertGroupsEqual(
            group_anagrams(["кот", "ток", "Кот", "ab", "aB", "Ba", "a! ", " !a"]),
            [["кот", "ток"], ["Кот"], ["ab"], ["aB", "Ba"], ["a! ", " !a"]],
        )

    def test_unicode_is_not_normalized(self):
        self.assertGroupsEqual(
            group_anagrams(["é", "e\u0301", "\u0301e"]),
            [["é"], ["e\u0301", "\u0301e"]],
        )

    def test_order_and_input_preservation(self):
        words = ["tan", "eat", "nat", "bat", "tea", "tan"]
        original = words.copy()
        result = group_anagrams(words)
        self.assertEqual(result, [["tan", "nat", "tan"], ["eat", "tea"], ["bat"]])
        self.assertEqual(words, original)
        result[0].append("new")
        self.assertEqual(words, original)

    def test_long_words(self):
        first = "a" * 1_000 + "b" * 1_000
        second = "ba" * 1_000
        third = "a" * 999 + "b" * 1_001
        self.assertGroupsEqual(group_anagrams([first, third, second]), [[first, second], [third]])

    def test_random_inputs_against_count_oracle(self):
        generator = random.Random(42)
        alphabet = "abAя !"
        for case in range(200):
            words = [
                "".join(generator.choices(alphabet, k=generator.randrange(9)))
                for _ in range(generator.randrange(40))
            ]
            # Добавляем и дубликаты, и перестановки уже имеющихся слов.
            for word in words[:5]:
                shuffled = list(word)
                generator.shuffle(shuffled)
                words.extend([word, "".join(shuffled)])
            with self.subTest(case=case):
                self.assertGroupsEqual(group_anagrams(words), count_oracle(words))


if __name__ == "__main__":
    unittest.main()

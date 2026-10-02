"""Проверки хеш-таблицы; dict используется только как эталон в тестах."""

import random
import unittest

from source_hash_table import HashTable


class CollisionKey:
    """Разные ключи с одинаковым хешем."""

    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return -7

    def __eq__(self, other):
        if not isinstance(other, CollisionKey):
            return NotImplemented
        return self.value == other.value

    def __repr__(self):
        return f"CollisionKey({self.value!r})"


class HashTableTests(unittest.TestCase):
    def assert_table_matches(self, table, expected):
        self.assertEqual(len(table), len(expected))
        self.assertIs(type(table._buckets), list)
        stored_count = 0
        seen = set()
        for index, bucket in enumerate(table._buckets):
            self.assertIs(type(bucket), list)
            for pair in bucket:
                self.assertIs(type(pair), list)
                self.assertEqual(len(pair), 2)
                key, value = pair
                self.assertEqual(hash(key) % len(table._buckets), index)
                self.assertNotIn(key, seen)
                seen.add(key)
                self.assertIn(key, expected)
                self.assertIs(value, expected[key])
                stored_count += 1
        self.assertEqual(stored_count, len(expected))
        for key, value in expected.items():
            self.assertIs(table.search(key), value)

    def test_empty_table_and_missing_keys(self):
        table = HashTable()
        self.assert_table_matches(table, {})
        for operation in (table.search, table.delete):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(KeyError) as error:
                    operation("missing")
                self.assertEqual(error.exception.args, ("missing",))
                self.assertEqual(len(table), 0)

    def test_nonpositive_capacity(self):
        for capacity in (0, -1, -100):
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValueError):
                    HashTable(capacity)

    def test_insert_update_search_delete(self):
        table = HashTable()
        table.insert("key", 10)
        self.assertEqual(table.search("key"), 10)
        self.assertEqual(len(table), 1)
        table.insert("key", 20)
        self.assertEqual(table.search("key"), 20)
        self.assertEqual(len(table), 1)
        self.assertEqual(table.delete("key"), 20)
        self.assertEqual(len(table), 0)
        with self.assertRaises(KeyError):
            table.search("key")
        with self.assertRaises(KeyError):
            table.delete("key")

    def test_negative_keys_and_falsy_values(self):
        table = HashTable(2)
        values = {None: None, "": "", -1: False, -2: 0, -100: [], 0: "zero"}
        for key, value in values.items():
            table.insert(key, value)
        self.assert_table_matches(table, values)
        for key, value in values.items():
            self.assertIs(table.delete(key), value)
        self.assertEqual(len(table), 0)

    def test_equal_numeric_keys_replace_value(self):
        table = HashTable()
        table.insert(0, "zero")
        table.insert(False, "false")
        table.insert(1, "one")
        table.insert(True, "true")
        table.insert(1.0, "float")
        self.assertEqual(len(table), 2)
        self.assertEqual(table.search(0), "false")
        self.assertEqual(table.search(False), "false")
        self.assertEqual(table.search(1), "float")
        self.assertEqual(table.delete(True), "float")
        with self.assertRaises(KeyError):
            table.search(1.0)

    def test_hashable_tuple_keys(self):
        table = HashTable()
        expected = {(): [], (1, "x"): None, ((1, 2), (3, 4)): "nested"}
        for key, value in expected.items():
            table.insert(key, value)
        self.assert_table_matches(table, expected)
        self.assertIsNone(table.delete(tuple([1, "x"])))

    def test_equal_distinct_collision_keys(self):
        first, equivalent = CollisionKey(7), CollisionKey(7)
        self.assertIsNot(first, equivalent)
        table = HashTable(4)
        table.insert(first, "old")
        table.insert(CollisionKey(8), "other")
        self.assertEqual(table.search(equivalent), "old")
        table.insert(equivalent, "new")
        self.assertEqual(len(table), 2)
        self.assertEqual(table.search(first), "new")
        self.assertEqual(table.delete(CollisionKey(7)), "new")
        self.assertEqual(table.search(CollisionKey(8)), "other")

    def test_delete_head_middle_tail_of_collision_chain(self):
        for deleted in (0, 2, 4):
            with self.subTest(deleted=deleted):
                table = HashTable(8)
                expected = {CollisionKey(index): [index] for index in range(5)}
                for key, value in expected.items():
                    table.insert(key, value)
                self.assertIs(table.delete(CollisionKey(deleted)),
                              expected.pop(CollisionKey(deleted)))
                self.assert_table_matches(table, expected)
                with self.assertRaises(KeyError):
                    table.search(CollisionKey(deleted))

    def test_missing_key_in_nonempty_collision_chain(self):
        table = HashTable()
        table.insert(CollisionKey(1), "one")
        for operation in (table.search, table.delete):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(KeyError):
                    operation(CollisionKey(2))
                self.assertEqual(table.search(CollisionKey(1)), "one")
                self.assertEqual(len(table), 1)

    def test_exact_growth_boundary_and_update(self):
        table = HashTable(4)
        for key in (1, 5, 9):
            table.insert(key, [key])
            self.assertEqual(len(table._buckets), 4)
        old_buckets = table._buckets
        for _ in range(10):
            table.insert(5, "updated")
            self.assertEqual(len(table), 3)
            self.assertIs(table._buckets, old_buckets)
        table.insert(13, "fourth")
        self.assertEqual(len(table._buckets), 8)
        self.assertEqual(len(table), 4)
        self.assertEqual(table.search(1), [1])
        self.assertEqual(table.search(5), "updated")
        self.assertEqual(table.search(9), [9])
        self.assertEqual(table.search(13), "fourth")

    def test_initial_capacity_one_and_repeated_growth(self):
        table = HashTable(1)
        expected = {}
        for key in range(150):
            value = [key]
            table.insert(key, value)
            expected[key] = value
            self.assertLessEqual(len(table) * 4, len(table._buckets) * 3)
            self.assert_table_matches(table, expected)

    def test_rehash_with_all_keys_colliding(self):
        table = HashTable(2)
        expected = {}
        for index in range(180):
            key, value = CollisionKey(index), [index]
            table.insert(key, value)
            expected[key] = value
        self.assertGreater(len(table._buckets), 2)
        self.assertEqual(sum(bool(bucket) for bucket in table._buckets), 1)
        self.assert_table_matches(table, expected)
        for index in range(0, 180, 2):
            self.assertIs(table.delete(CollisionKey(index)),
                          expected.pop(CollisionKey(index)))
        self.assert_table_matches(table, expected)

    def test_large_insert_and_delete(self):
        table = HashTable(4)
        expected = {}
        for key in range(-2500, 2500):
            value = [key]
            table.insert(key, value)
            expected[key] = value
        self.assert_table_matches(table, expected)
        capacity = len(table._buckets)
        for key in range(-2500, 2500):
            self.assertIs(table.delete(key), expected.pop(key))
        self.assertEqual(len(table._buckets), capacity)
        self.assert_table_matches(table, expected)

    def test_values_are_stored_by_reference(self):
        table = HashTable(1)
        value = []
        table.insert("list", value)
        value.append(10)
        self.assertIs(table.search("list"), value)
        for key in range(50):
            table.insert(key, key)
        self.assertIs(table.search("list"), value)
        table.search("list").append(20)
        self.assertEqual(value, [10, 20])
        self.assertIs(table.delete("list"), value)

    def test_reinsert_after_delete_and_empty(self):
        table = HashTable(1)
        for round_number in range(5):
            expected = {CollisionKey(key): [round_number, key] for key in range(20)}
            for key, value in expected.items():
                table.insert(key, value)
            self.assert_table_matches(table, expected)
            for key, value in expected.items():
                self.assertIs(table.delete(key), value)
            self.assert_table_matches(table, {})

    def test_independent_instances(self):
        first, second = HashTable(1), HashTable(8)
        first.insert("same", "first")
        second.insert("same", "second")
        first.insert("only_first", 1)
        self.assertEqual(first.search("same"), "first")
        self.assertEqual(second.search("same"), "second")
        with self.assertRaises(KeyError):
            second.search("only_first")
        first.delete("same")
        self.assertEqual(second.search("same"), "second")
        self.assertEqual(len(second), 1)

    def test_unhashable_key_does_not_change_state(self):
        table = HashTable(4)
        expected = {1: [], 5: "five", 9: None}
        for key, value in expected.items():
            table.insert(key, value)
        old_buckets = table._buckets
        for key in ([], {}, set(), ([],)):
            for operation in (lambda k: table.insert(k, "bad"), table.search, table.delete):
                with self.subTest(key=repr(key), operation=operation.__name__):
                    with self.assertRaises(TypeError):
                        operation(key)
                    self.assertIs(table._buckets, old_buckets)
                    self.assert_table_matches(table, expected)

    def test_same_nan_object_and_distinct_nan_keys(self):
        first, second = float("nan"), float("nan")
        table = HashTable(1)
        table.insert(first, "first")
        self.assertEqual(table.search(first), "first")
        table.insert(first, "updated")
        self.assertEqual(len(table), 1)
        table.insert(second, "second")
        self.assertEqual(len(table), 2)
        self.assertEqual(table.search(first), "updated")
        self.assertEqual(table.search(second), "second")
        self.assertEqual(table.delete(first), "updated")
        self.assertEqual(table.search(second), "second")

    def test_random_operations_against_dict(self):
        rng = random.Random(2612928)
        table, expected = HashTable(1), {}
        keys = list(range(-50, 51)) + [None, "", "word", (), (1, 2), False, True]
        for step in range(4000):
            key = rng.choice(keys)
            operation = rng.choice(("insert", "insert", "search", "delete"))
            with self.subTest(step=step, operation=operation, key=key):
                if operation == "insert":
                    value = rng.choice((None, False, "", [step, key], step))
                    table.insert(key, value)
                    expected[key] = value
                elif key in expected:
                    if operation == "search":
                        self.assertIs(table.search(key), expected[key])
                    else:
                        self.assertIs(table.delete(key), expected.pop(key))
                else:
                    with self.assertRaises(KeyError):
                        getattr(table, operation)(key)
                self.assert_table_matches(table, expected)

    def test_random_collisions_against_dict(self):
        rng = random.Random(3595632)
        table, expected = HashTable(2), {}
        for step in range(800):
            key = CollisionKey(rng.randrange(50))
            operation = rng.choice(("insert", "insert", "search", "delete"))
            with self.subTest(step=step, operation=operation, key=key):
                if operation == "insert":
                    value = [step]
                    table.insert(key, value)
                    expected[key] = value
                elif key in expected:
                    if operation == "search":
                        self.assertIs(table.search(key), expected[key])
                    else:
                        self.assertIs(table.delete(key), expected.pop(key))
                else:
                    with self.assertRaises(KeyError):
                        getattr(table, operation)(key)
                self.assert_table_matches(table, expected)


if __name__ == "__main__":
    unittest.main()

"""Тесты стека и очереди на связных списках."""

import unittest

from source_stack_vs_queue import Queue, Stack


class StackTests(unittest.TestCase):
    def test_empty_stack(self):
        stack = Stack()
        self.assertIs(stack.is_empty(), True)
        self.assertEqual(stack.get_size(), 0)

    def test_order_and_size(self):
        stack = Stack()
        for size, value in enumerate((10, 20, 30, 40), 1):
            stack.push(value)
            self.assertEqual(stack.get_size(), size)
            self.assertIs(stack.is_empty(), False)

        for size, expected in zip((3, 2, 1, 0), (40, 30, 20, 10)):
            self.assertEqual(stack.pop(), expected)
            self.assertEqual(stack.get_size(), size)
            self.assertIs(stack.is_empty(), size == 0)

    def test_single_element_and_reuse(self):
        stack = Stack()
        for value in (10, 20, 30):
            with self.subTest(value=value):
                stack.push(value)
                self.assertEqual(stack.peek(), value)
                self.assertEqual(stack.get_size(), 1)
                self.assertEqual(stack.pop(), value)
                self.assertIs(stack.is_empty(), True)
                self.assertEqual(stack.get_size(), 0)
                self.assertIsNone(stack.top)

    def test_interleaved_operations(self):
        stack = Stack()
        stack.push(10)
        stack.push(20)
        self.assertEqual(stack.pop(), 20)
        stack.push(30)
        stack.push(40)
        self.assertEqual(stack.pop(), 40)
        self.assertEqual(stack.pop(), 30)
        stack.push(50)
        self.assertEqual(stack.get_size(), 2)
        self.assertEqual(stack.pop(), 50)
        self.assertEqual(stack.pop(), 10)
        self.assertIs(stack.is_empty(), True)

    def test_peek_does_not_remove_element(self):
        stack = Stack()
        stack.push(10)
        stack.push(20)
        self.assertEqual(stack.peek(), 20)
        self.assertEqual(stack.peek(), 20)
        self.assertEqual(stack.get_size(), 2)
        self.assertEqual(stack.pop(), 20)
        self.assertEqual(stack.peek(), 10)
        self.assertEqual(stack.get_size(), 1)

    def test_empty_operations(self):
        for after_removal in (False, True):
            stack = Stack()
            if after_removal:
                stack.push(10)
                stack.pop()

            for method in (stack.pop, stack.peek):
                with self.subTest(after_removal=after_removal, method=method.__name__):
                    with self.assertRaises(IndexError):
                        method()
                    self.assertIs(stack.is_empty(), True)
                    self.assertEqual(stack.get_size(), 0)

            stack.push(20)
            self.assertEqual(stack.pop(), 20)

    def test_falsy_values_and_duplicates(self):
        stack = Stack()
        values = (None, 0, False, "", -5, -5, "text")
        for value in values:
            stack.push(value)
        for expected in reversed(values):
            with self.subTest(expected=expected):
                self.assertIs(stack.peek(), expected)
                self.assertIs(stack.pop(), expected)
        self.assertIs(stack.is_empty(), True)
        self.assertEqual(stack.get_size(), 0)

    def test_independent_instances(self):
        first, second = Stack(), Stack()
        first.push(10)
        self.assertIs(second.is_empty(), True)
        self.assertEqual(second.get_size(), 0)
        second.push(20)
        first.push(30)
        self.assertEqual(first.pop(), 30)
        self.assertEqual(second.pop(), 20)
        self.assertEqual(first.pop(), 10)


class QueueTests(unittest.TestCase):
    def test_empty_queue(self):
        queue = Queue()
        self.assertIs(queue.is_empty(), True)
        self.assertEqual(queue.get_size(), 0)
        self.assertIsNone(queue.head)
        self.assertIsNone(queue.tail)

    def test_order_and_size(self):
        queue = Queue()
        for size, value in enumerate((10, 20, 30, 40), 1):
            queue.enqueue(value)
            self.assertEqual(queue.get_size(), size)
            self.assertIs(queue.is_empty(), False)

        for size, expected in zip((3, 2, 1, 0), (10, 20, 30, 40)):
            self.assertEqual(queue.dequeue(), expected)
            self.assertEqual(queue.get_size(), size)
            self.assertIs(queue.is_empty(), size == 0)
        self.assertIsNone(queue.head)
        self.assertIsNone(queue.tail)

    def test_single_element_and_reuse(self):
        queue = Queue()
        for value in (10, 20, 30):
            with self.subTest(value=value):
                queue.enqueue(value)
                self.assertEqual(queue.peek(), value)
                self.assertEqual(queue.get_size(), 1)
                self.assertEqual(queue.dequeue(), value)
                self.assertIs(queue.is_empty(), True)
                self.assertEqual(queue.get_size(), 0)
                self.assertIsNone(queue.head)
                self.assertIsNone(queue.tail)

    def test_interleaved_operations(self):
        queue = Queue()
        queue.enqueue(10)
        queue.enqueue(20)
        self.assertEqual(queue.dequeue(), 10)
        queue.enqueue(30)
        queue.enqueue(40)
        self.assertEqual(queue.dequeue(), 20)
        self.assertEqual(queue.dequeue(), 30)
        queue.enqueue(50)
        self.assertEqual(queue.get_size(), 2)
        self.assertEqual(queue.dequeue(), 40)
        self.assertEqual(queue.dequeue(), 50)
        self.assertIs(queue.is_empty(), True)

    def test_peek_does_not_remove_element(self):
        queue = Queue()
        queue.enqueue(10)
        queue.enqueue(20)
        self.assertEqual(queue.peek(), 10)
        self.assertEqual(queue.peek(), 10)
        self.assertEqual(queue.get_size(), 2)
        self.assertEqual(queue.dequeue(), 10)
        self.assertEqual(queue.peek(), 20)
        self.assertEqual(queue.get_size(), 1)

    def test_empty_operations(self):
        for after_removal in (False, True):
            queue = Queue()
            if after_removal:
                queue.enqueue(10)
                queue.dequeue()

            for method in (queue.dequeue, queue.peek):
                with self.subTest(after_removal=after_removal, method=method.__name__):
                    with self.assertRaises(IndexError):
                        method()
                    self.assertIs(queue.is_empty(), True)
                    self.assertEqual(queue.get_size(), 0)
                    self.assertIsNone(queue.head)
                    self.assertIsNone(queue.tail)

            queue.enqueue(20)
            self.assertEqual(queue.dequeue(), 20)

    def test_falsy_values_and_duplicates(self):
        queue = Queue()
        values = (None, 0, False, "", -5, -5, "text")
        for value in values:
            queue.enqueue(value)
        for expected in values:
            with self.subTest(expected=expected):
                self.assertIs(queue.peek(), expected)
                self.assertIs(queue.dequeue(), expected)
        self.assertIs(queue.is_empty(), True)
        self.assertEqual(queue.get_size(), 0)

    def test_independent_instances(self):
        first, second = Queue(), Queue()
        first.enqueue(10)
        self.assertIs(second.is_empty(), True)
        self.assertEqual(second.get_size(), 0)
        second.enqueue(20)
        first.enqueue(30)
        self.assertEqual(first.dequeue(), 10)
        self.assertEqual(second.dequeue(), 20)
        self.assertEqual(first.dequeue(), 30)


if __name__ == "__main__":
    unittest.main()

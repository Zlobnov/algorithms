class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, value):
        """Добавить значение в стек."""
        node = Node(value)
        node.next = self.top
        self.top = node
        self._size += 1

    def pop(self):
        """Удалить и вернуть последнее добавленное значение."""
        if self.top is None:
            raise IndexError("pop from empty stack")

        value = self.top.value
        self.top = self.top.next
        self._size -= 1
        return value

    def peek(self):
        """Вернуть последнее добавленное значение."""
        if self.top is None:
            raise IndexError("peek from empty stack")
        return self.top.value

    def is_empty(self):
        return self.top is None

    def get_size(self):
        return self._size


class Queue:
    def __init__(self):
        self.head = self.tail = None
        self._size = 0

    def enqueue(self, value):
        """Добавить значение в очередь."""
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node

        self.tail = node
        self._size += 1

    def dequeue(self):
        """Удалить и вернуть первое добавленное значение."""
        if self.head is None:
            raise IndexError("dequeue from empty queue")

        value = self.head.value
        self.head = self.head.next
        self._size -= 1

        if self.head is None:
            self.tail = None

        return value

    def is_empty(self):
        return self.head is None

    def peek(self):
        """Вернуть первое добавленное значение."""
        if self.head is None:
            raise IndexError("peek from empty queue")
        return self.head.value

    def get_size(self):
        return self._size

class HashTable:
    """Хеш-таблица с цепочками и увеличением числа корзин."""

    def __init__(self, capacity=8):
        if capacity < 1:
            raise ValueError("Число корзин должно быть положительным")
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def __len__(self):
        return self._size

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def insert(self, key, value):
        """Добавить пару или заменить значение существующего ключа."""
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] is key or pair[0] == key:
                pair[1] = value
                return

        if (self._size + 1) * 4 > len(self._buckets) * 3:
            self._resize()
            bucket = self._bucket(key)

        bucket.append([key, value])
        self._size += 1

    def search(self, key):
        """Найти значение; если ключа нет, выбросить KeyError."""
        for stored_key, value in self._bucket(key):
            if stored_key is key or stored_key == key:
                return value
        raise KeyError(key)

    def delete(self, key):
        """Удалить пару и вернуть её значение; иначе выбросить KeyError."""
        bucket = self._bucket(key)
        for index, pair in enumerate(bucket):
            if pair[0] is key or pair[0] == key:
                value = pair[1]
                bucket.pop(index)
                self._size -= 1
                return value
        raise KeyError(key)

    def _resize(self):
        buckets = [[] for _ in range(len(self._buckets) * 2)]
        for bucket in self._buckets:
            for pair in bucket:
                buckets[hash(pair[0]) % len(buckets)].append(pair)
        self._buckets = buckets


if __name__ == "__main__":
    table = HashTable(4)
    table.insert(1, "A")
    table.insert(5, "B")
    table.insert(9, "C")
    table.insert(5, "B2")
    table.insert(13, "D")
    print(table.search(5))
    print(table.delete(9))
    print(len(table))

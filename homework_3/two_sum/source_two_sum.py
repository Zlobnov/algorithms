def two_sum(arr, k):
    """Вернуть индексы единственной пары с суммой k по возрастанию."""
    seen = {}

    for index, value in enumerate(arr):
        complement = k - value
        if complement in seen:
            return seen[complement], index
        seen[value] = index


if __name__ == "__main__":
    arr = [1, 3, 4, 10]
    k = 7
    print(*two_sum(arr, k))

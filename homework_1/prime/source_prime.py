def get_primes(N):
    if N <= 2:
        return 0

    numbers = [0] + [number for number in range(1, N)]
    numbers[1] = 0

    pointer = 2
    while pointer * pointer < N:
        if numbers[pointer] != 0:
            pointer_lower = pointer * pointer
            while pointer_lower < N:
                numbers[pointer_lower] = 0
                pointer_lower = pointer_lower + pointer

        pointer = pointer + 1

    return len([number for number in numbers if number != 0])

print(get_primes(int(input())))

def is_palindrome(number):
    digits = []

    while number != 0:
        digit, number = number % 10, number // 10
        digits.append(digit)

    head, tail = digits[0], digits[-1]
    if head != tail:
        return False

    for i in range(len(digits) // 2):
        if digits[i] != digits[-i - 1]:
            return False

    return True

print(is_palindrome(int(input())))

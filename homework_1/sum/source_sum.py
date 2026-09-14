def maximize_sum(numbers_list):
    min_odd = -1
    total = 0

    for number in numbers_list:
        total += number
        if number % 2:
            if min_odd == -1 or number < min_odd:
                min_odd = number

    if total % 2 == 0:
        return total
    else:
        return total - min_odd


print(maximize_sum(map(int, input().split())))
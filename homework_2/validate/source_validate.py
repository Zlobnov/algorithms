def validate_stack_sequences(pushed, popped):
    """Проверить, возможен ли заданный порядок извлечения из стека."""
    stack = []
    next_pop = 0

    for value in pushed:
        stack.append(value)
        while stack and stack[-1] == popped[next_pop]:
            stack.pop()
            next_pop += 1

    return not stack

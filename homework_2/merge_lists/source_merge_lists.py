class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


def merge_with_dummy(list1, list2):
    """Объединить списки, используя фиктивный начальный узел."""
    dummy = Node(None)
    tail = dummy

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    tail.next = list1 if list1 is not None else list2
    return dummy.next


def merge_without_dummy(list1, list2):
    """Объединить списки без создания новых узлов."""
    if list1 is None:
        return list2
    if list2 is None:
        return list1

    if list1.value <= list2.value:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next
    tail = head

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    tail.next = list1 if list1 is not None else list2
    return head

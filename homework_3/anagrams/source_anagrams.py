def group_anagrams(words):
    """Сгруппировать анаграммы, сохранив порядок появления групп и слов."""
    groups = {}

    for word in words:
        signature = "".join(sorted(word))
        if signature not in groups:
            groups[signature] = []
        groups[signature].append(word)

    return list(groups.values())

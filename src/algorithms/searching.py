def normalize_title(title):
    return title.strip().casefold()


def binary_search(items, title):
    target = normalize_title(title)

    left = 0
    right = len(items) - 1

    while left <= right:
        middle = (left + right) // 2

        current = normalize_title(items[middle].title)

        if current == target:
            return items[middle]

        if current < target:
            left = middle + 1
        else:
            right = middle - 1

    return None

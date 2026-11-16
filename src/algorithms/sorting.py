def merge_sort(items, key, reverse=False):
    if len(items) <= 1:
        return items

    middle = len(items) // 2

    left = merge_sort(items[:middle], key, reverse)
    right = merge_sort(items[middle:], key, reverse)

    return merge(left, right, key, reverse)


def merge(left, right, key, reverse):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        left_value = key(left[i])
        right_value = key(right[j])

        if reverse:
            condition = left_value >= right_value
        else:
            condition = left_value <= right_value

        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

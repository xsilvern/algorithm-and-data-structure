from tree import MaxHeap


def selection_sort(array):
    size = len(array)
    for i in range(size-1):
        least = i
        for j in range(i+1, size):
            if array[least] > array[j]:
                least = j
        array[least], array[i] = array[i], array[least]
    return array


def insertion_sort(array):
    size = len(array)
    for i in range(1, size):
        key = array[i]
        j = i-1
        while key < array[j] and j >= 0:
            array[j+1] = array[j]
            j -= 1
        array[j+1] = key
    return array


def bubble_sort_normal(array):
    size = len(array)
    for i in range(size-1, 0, -1):
        for j in range(i):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
    return array


def heap_sort(array):
    n = len(array)
    max_heap = MaxHeap()

    for item in array:
        max_heap.insert(item)

    for i in range(n - 1, -1, -1):
        array[i] = max_heap.extract_max()

    return array


def quick_sort(array):
    _divide(array, 0, len(array) - 1)
    return array


def _divide(array, low, high):
    if low < high:
        pi = _partition(array, low, high)
        _divide(array, low, pi - 1)
        _divide(array, pi + 1, high)


def _partition(array, low, high):
    pivot_index = _median_of_three(array, low, (low+high)//2, high)
    array[high], array[pivot_index] = array[pivot_index], array[high]
    pivot = array[high]
    i = low - 1

    for j in range(low, high):
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]

    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1


def _median_of_three(array, a, b, c):
    if array[a] > array[b] and array[a] > array[c]:
        return b if array[b] >= array[c] else c
    elif array[b] > array[a] and array[b] > array[c]:
        return a if array[a] >= array[c] else c
    else:
        return a if array[a] >= array[b] else b


def merge_sort(array):
    if len(array) > 1:
        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]

        merge_sort(left)
        merge_sort(right)

        _merge(array, left, right)
    return array


def _merge(array, left, right):
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            array[k] = left[i]
            i += 1
        else:
            array[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        array[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        array[k] = right[j]
        j += 1
        k += 1


def counting_sort(array):
    max_val = max(array)
    count = [0] * (max_val + 1)
    result = [0] * len(array)

    for num in array:
        count[num] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for num in reversed(array):
        result[count[num] - 1] = num
        count[num] -= 1

    return result

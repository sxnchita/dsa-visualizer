# algorithms/sorting.py
# Returns step-by-step instructions for each sort algorithm

def bubble_sort_steps(arr):
    a = arr[:]
    steps = []
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            steps.append({"type": "compare", "i": j, "j": j + 1, "array": a[:]})
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                steps.append({"type": "swap", "i": j, "j": j + 1, "array": a[:]})
        steps.append({"type": "sorted", "index": n - i - 1, "array": a[:]})
    return steps, a


def insertion_sort_steps(arr):
    a = arr[:]
    steps = []
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        steps.append({"type": "pick", "index": i, "array": a[:]})
        while j >= 0 and a[j] > key:
            steps.append({"type": "compare", "i": j, "j": j + 1, "array": a[:]})
            a[j + 1] = a[j]
            steps.append({"type": "shift", "i": j, "j": j + 1, "array": a[:]})
            j -= 1
        a[j + 1] = key
        steps.append({"type": "place", "index": j + 1, "array": a[:]})
    return steps, a


def selection_sort_steps(arr):
    a = arr[:]
    steps = []
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            steps.append({"type": "compare", "i": min_idx, "j": j, "array": a[:]})
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            steps.append({"type": "swap", "i": i, "j": min_idx, "array": a[:]})
        steps.append({"type": "sorted", "index": i, "array": a[:]})
    return steps, a


def merge_sort_steps(arr):
    steps = []

    def merge_sort(a, left):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        L = merge_sort(a[:mid], left)
        R = merge_sort(a[mid:], left + mid)
        return merge(L, R, left, left + mid)

    def merge(L, R, left, right):
        result = []
        i = j = 0
        while i < len(L) and j < len(R):
            steps.append({"type": "compare", "i": left + i, "j": right + j, "array": None})
            if L[i] <= R[j]:
                result.append(L[i]); i += 1
            else:
                result.append(R[j]); j += 1
        result += L[i:]; result += R[j:]
        steps.append({"type": "merge", "left": left, "right": right + len(R), "array": result[:]})
        return result

    final = merge_sort(arr[:], 0)
    return steps, final


def quick_sort_steps(arr):
    a = arr[:]
    steps = []

    def partition(low, high):
        pivot = a[high]
        steps.append({"type": "pivot", "index": high, "array": a[:]})
        i = low - 1
        for j in range(low, high):
            steps.append({"type": "compare", "i": j, "j": high, "array": a[:]})
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                steps.append({"type": "swap", "i": i, "j": j, "array": a[:]})
        a[i + 1], a[high] = a[high], a[i + 1]
        steps.append({"type": "swap", "i": i + 1, "j": high, "array": a[:]})
        steps.append({"type": "sorted", "index": i + 1, "array": a[:]})
        return i + 1

    def quick_sort(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort(low, pi - 1)
            quick_sort(pi + 1, high)

    quick_sort(0, len(a) - 1)
    return steps, a

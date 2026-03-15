# algorithms/linear.py
# Linked List, Stack, Queue step generators

def linked_list_steps(operation, values, target=None):
    """Simulate linked list operations and return animation steps."""
    steps = []
    current = list(values)  # current state of the list

    if operation == "insert_end":
        steps.append({"type": "start", "list": current[:], "message": f"Inserting {target} at end"})
        for i, val in enumerate(current):
            steps.append({"type": "traverse", "index": i, "list": current[:], "message": f"Visiting node {val}"})
        current.append(target)
        steps.append({"type": "insert", "index": len(current)-1, "list": current[:], "message": f"Inserted {target} at end"})

    elif operation == "insert_front":
        steps.append({"type": "start", "list": current[:], "message": f"Inserting {target} at front"})
        current.insert(0, target)
        steps.append({"type": "insert", "index": 0, "list": current[:], "message": f"Inserted {target} at front"})

    elif operation == "delete":
        steps.append({"type": "start", "list": current[:], "message": f"Deleting {target}"})
        for i, val in enumerate(current):
            steps.append({"type": "traverse", "index": i, "list": current[:], "message": f"Checking node {val}"})
            if val == target:
                current.pop(i)
                steps.append({"type": "delete", "index": i, "list": current[:], "message": f"Deleted {target}"})
                break
        else:
            steps.append({"type": "notfound", "list": current[:], "message": f"{target} not found"})

    elif operation == "search":
        steps.append({"type": "start", "list": current[:], "message": f"Searching for {target}"})
        for i, val in enumerate(current):
            steps.append({"type": "traverse", "index": i, "list": current[:], "message": f"Checking node {val}"})
            if val == target:
                steps.append({"type": "found", "index": i, "list": current[:], "message": f"Found {target} at index {i}"})
                break
        else:
            steps.append({"type": "notfound", "list": current[:], "message": f"{target} not found"})

    elif operation == "reverse":
        steps.append({"type": "start", "list": current[:], "message": "Reversing linked list"})
        left, right = 0, len(current) - 1
        while left < right:
            steps.append({"type": "compare", "i": left, "j": right, "list": current[:], "message": f"Swapping {current[left]} and {current[right]}"})
            current[left], current[right] = current[right], current[left]
            steps.append({"type": "swap", "i": left, "j": right, "list": current[:], "message": "Swapped!"})
            left += 1; right -= 1
        steps.append({"type": "done", "list": current[:], "message": "List reversed!"})

    return steps, current


def stack_steps(operations):
    """
    operations: list of {"op": "push"/"pop"/"peek", "value": x}
    """
    stack = []
    steps = []
    steps.append({"type": "init", "stack": [], "message": "Stack initialized (LIFO)"})

    for op in operations:
        action = op.get("op")
        val = op.get("value")

        if action == "push":
            stack.append(val)
            steps.append({"type": "push", "value": val, "stack": stack[:], "message": f"PUSH {val} → added to top"})
        elif action == "pop":
            if stack:
                popped = stack.pop()
                steps.append({"type": "pop", "value": popped, "stack": stack[:], "message": f"POP → removed {popped} from top"})
            else:
                steps.append({"type": "error", "stack": stack[:], "message": "Stack Underflow! Cannot pop from empty stack"})
        elif action == "peek":
            if stack:
                steps.append({"type": "peek", "value": stack[-1], "stack": stack[:], "message": f"PEEK → top is {stack[-1]}"})
            else:
                steps.append({"type": "error", "stack": stack[:], "message": "Stack is empty!"})

    return steps, stack


def queue_steps(operations):
    """
    operations: list of {"op": "enqueue"/"dequeue"/"front", "value": x}
    """
    queue = []
    steps = []
    steps.append({"type": "init", "queue": [], "message": "Queue initialized (FIFO)"})

    for op in operations:
        action = op.get("op")
        val = op.get("value")

        if action == "enqueue":
            queue.append(val)
            steps.append({"type": "enqueue", "value": val, "queue": queue[:], "message": f"ENQUEUE {val} → added to rear"})
        elif action == "dequeue":
            if queue:
                removed = queue.pop(0)
                steps.append({"type": "dequeue", "value": removed, "queue": queue[:], "message": f"DEQUEUE → removed {removed} from front"})
            else:
                steps.append({"type": "error", "queue": queue[:], "message": "Queue Underflow! Cannot dequeue from empty queue"})
        elif action == "front":
            if queue:
                steps.append({"type": "front", "value": queue[0], "queue": queue[:], "message": f"FRONT → {queue[0]}"})
            else:
                steps.append({"type": "error", "queue": queue[:], "message": "Queue is empty!"})

    return steps, queue


def binary_search_steps(arr, target):
    a = sorted(arr)
    steps = []
    left, right = 0, len(a) - 1
    steps.append({"type": "init", "array": a[:], "target": target, "message": f"Searching for {target} in sorted array"})

    while left <= right:
        mid = (left + right) // 2
        steps.append({"type": "mid", "left": left, "right": right, "mid": mid, "array": a[:], "message": f"Checking middle index {mid} → value {a[mid]}"})
        if a[mid] == target:
            steps.append({"type": "found", "index": mid, "array": a[:], "message": f"Found {target} at index {mid}!"})
            return steps, mid
        elif a[mid] < target:
            steps.append({"type": "goright", "left": left, "right": right, "mid": mid, "array": a[:], "message": f"{a[mid]} < {target} → search right half"})
            left = mid + 1
        else:
            steps.append({"type": "goleft", "left": left, "right": right, "mid": mid, "array": a[:], "message": f"{a[mid]} > {target} → search left half"})
            right = mid - 1

    steps.append({"type": "notfound", "array": a[:], "message": f"{target} not found in array"})
    return steps, -1

# algorithms/graph.py
from collections import deque

def bfs_steps(nodes, edges, start):
    # Build adjacency list
    adj = {n: [] for n in nodes}
    for e in edges:
        adj[e["from"]].append(e["to"])
        adj[e["to"]].append(e["from"])

    steps = []
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    steps.append({"type": "start", "node": start, "visited": list(visited), "queue": list(queue)})

    while queue:
        node = queue.popleft()
        order.append(node)
        steps.append({"type": "visit", "node": node, "visited": list(visited), "queue": list(queue)})

        for neighbor in sorted(adj[node]):
            steps.append({"type": "explore", "from": node, "to": neighbor, "visited": list(visited)})
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                steps.append({"type": "enqueue", "node": neighbor, "visited": list(visited), "queue": list(queue)})

    return steps, order


def dfs_steps(nodes, edges, start):
    adj = {n: [] for n in nodes}
    for e in edges:
        adj[e["from"]].append(e["to"])
        adj[e["to"]].append(e["from"])

    steps = []
    visited = set()
    order = []

    def dfs(node):
        visited.add(node)
        order.append(node)
        steps.append({"type": "visit", "node": node, "visited": list(visited)})
        for neighbor in sorted(adj[node]):
            steps.append({"type": "explore", "from": node, "to": neighbor, "visited": list(visited)})
            if neighbor not in visited:
                steps.append({"type": "recurse", "from": node, "to": neighbor})
                dfs(neighbor)
        steps.append({"type": "backtrack", "node": node, "visited": list(visited)})

    dfs(start)
    return steps, order


def dijkstra_steps(nodes, edges, start):
    import heapq
    adj = {n: [] for n in nodes}
    for e in edges:
        w = e.get("weight", 1)
        adj[e["from"]].append((e["to"], w))
        adj[e["to"]].append((e["from"], w))

    dist = {n: float('inf') for n in nodes}
    dist[start] = 0
    pq = [(0, start)]
    visited = set()
    steps = []
    order = []

    steps.append({"type": "init", "node": start, "dist": dict(dist)})

    while pq:
        d, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        steps.append({"type": "visit", "node": node, "dist": dict(dist), "visited": list(visited)})

        for neighbor, weight in adj[node]:
            new_dist = dist[node] + weight
            steps.append({"type": "relax", "from": node, "to": neighbor, "weight": weight, "newDist": new_dist, "oldDist": dist[neighbor]})
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
                steps.append({"type": "update", "node": neighbor, "dist": dict(dist)})

    return steps, dist

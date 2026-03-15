"""
app.py — DSA Algorithm Visualizer Backend
Flask server that computes algorithm steps and returns them as JSON
"""
import os, random
from flask import Flask, request, jsonify
from flask_cors import CORS

from algorithms.sorting import (
    bubble_sort_steps, insertion_sort_steps,
    selection_sort_steps, merge_sort_steps, quick_sort_steps
)
from algorithms.graph import bfs_steps, dfs_steps, dijkstra_steps
from algorithms.linear import (
    linked_list_steps, stack_steps, queue_steps, binary_search_steps
)

app = Flask(__name__)
CORS(app)

def ok(data):
    return jsonify({"success": True, "data": data})

def err(msg, code=400):
    return jsonify({"success": False, "error": msg}), code


# ── Health ────────────────────────────────────────────

@app.route("/api/health")
def health():
    return ok({"status": "ok", "message": "DSA Visualizer backend running!"})


# ── SORTING ──────────────────────────────────────────

@app.route("/api/sort", methods=["POST"])
def sort():
    body = request.json or {}
    algo  = body.get("algorithm", "bubble").lower()
    array = body.get("array", [])

    if not array or len(array) > 100:
        return err("Array must have 1–100 elements")

    algos = {
        "bubble":    bubble_sort_steps,
        "insertion": insertion_sort_steps,
        "selection": selection_sort_steps,
        "merge":     merge_sort_steps,
        "quick":     quick_sort_steps,
    }

    if algo not in algos:
        return err(f"Unknown algorithm '{algo}'. Choose: {list(algos.keys())}")

    steps, result = algos[algo](array)
    return ok({
        "algorithm": algo,
        "original":  array,
        "sorted":    result,
        "steps":     steps,
        "stepCount": len(steps),
    })


@app.route("/api/sort/random", methods=["GET"])
def random_array():
    size = min(int(request.args.get("size", 12)), 30)
    arr  = random.sample(range(1, 100), size)
    return ok({"array": arr})


# ── GRAPH ─────────────────────────────────────────────

@app.route("/api/graph/bfs", methods=["POST"])
def graph_bfs():
    body  = request.json or {}
    nodes = body.get("nodes", [])
    edges = body.get("edges", [])
    start = body.get("start")
    if not nodes or start not in nodes:
        return err("Invalid nodes or start node")
    steps, order = bfs_steps(nodes, edges, start)
    return ok({"algorithm": "BFS", "order": order, "steps": steps, "stepCount": len(steps)})


@app.route("/api/graph/dfs", methods=["POST"])
def graph_dfs():
    body  = request.json or {}
    nodes = body.get("nodes", [])
    edges = body.get("edges", [])
    start = body.get("start")
    if not nodes or start not in nodes:
        return err("Invalid nodes or start node")
    steps, order = dfs_steps(nodes, edges, start)
    return ok({"algorithm": "DFS", "order": order, "steps": steps, "stepCount": len(steps)})


@app.route("/api/graph/dijkstra", methods=["POST"])
def graph_dijkstra():
    body  = request.json or {}
    nodes = body.get("nodes", [])
    edges = body.get("edges", [])
    start = body.get("start")
    if not nodes or start not in nodes:
        return err("Invalid nodes or start node")
    steps, dist = dijkstra_steps(nodes, edges, start)
    return ok({"algorithm": "Dijkstra", "distances": dist, "steps": steps, "stepCount": len(steps)})


# ── LINKED LIST ──────────────────────────────────────

@app.route("/api/linkedlist", methods=["POST"])
def linkedlist():
    body      = request.json or {}
    operation = body.get("operation", "insert_end")
    values    = body.get("values", [])
    target    = body.get("target")
    steps, result = linked_list_steps(operation, values, target)
    return ok({"operation": operation, "result": result, "steps": steps, "stepCount": len(steps)})


# ── STACK ────────────────────────────────────────────

@app.route("/api/stack", methods=["POST"])
def stack():
    body       = request.json or {}
    operations = body.get("operations", [])
    if not operations:
        return err("Provide a list of operations: [{op: push/pop/peek, value: x}]")
    steps, result = stack_steps(operations)
    return ok({"result": result, "steps": steps, "stepCount": len(steps)})


# ── QUEUE ────────────────────────────────────────────

@app.route("/api/queue", methods=["POST"])
def queue_route():
    body       = request.json or {}
    operations = body.get("operations", [])
    if not operations:
        return err("Provide a list of operations: [{op: enqueue/dequeue/front, value: x}]")
    steps, result = queue_steps(operations)
    return ok({"result": result, "steps": steps, "stepCount": len(steps)})


# ── BINARY SEARCH ────────────────────────────────────

@app.route("/api/search/binary", methods=["POST"])
def binary_search():
    body   = request.json or {}
    array  = body.get("array", [])
    target = body.get("target")
    if not array or target is None:
        return err("Provide array and target")
    steps, idx = binary_search_steps(array, target)
    return ok({"target": target, "foundAt": idx, "steps": steps, "stepCount": len(steps)})


# ── Entry Point ──────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    print(f"\n🚀 DSA Visualizer Backend running at http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=True)

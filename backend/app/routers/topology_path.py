# Pfad: backend/app/routers/topology_path.py
from fastapi import APIRouter
import json
import heapq

router = APIRouter()

def load_topology():
    with open("data/topology/core_topology.json", "r") as f:
        return json.load(f)

def build_graph(data):
    graph = {}
    for link in data["links"]:
        src = link["source"]
        dst = link["target"]
        cost = link.get("length", 1)
        graph.setdefault(src, []).append((dst, cost))
        graph.setdefault(dst, []).append((src, cost))
    return graph

def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        curr_dist, curr_node = heapq.heappop(heap)
        if curr_dist > distances[curr_node]:
            continue
        for neighbor, weight in graph[curr_node]:
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = curr_node
                heapq.heappush(heap, (distance, neighbor))

    return distances, previous

def reconstruct_path(previous, target):
    path = []
    while target:
        path.insert(0, target)
        target = previous[target]
    return path

@router.get("/path/{device_id}")
async def get_path(device_id: str):
    data = load_topology()
    graph = build_graph(data)

    if device_id not in graph:
        return {"path": []}

    distances, previous = dijkstra(graph, device_id)
    longest = max(distances.items(), key=lambda x: x[1] if x[1] < float("inf") else -1)
    path_ids = reconstruct_path(previous, longest[0])

    id_to_node = {n["id"]: n for n in data["nodes"]}
    path = [id_to_node[nid] for nid in path_ids if nid in id_to_node]
    return {"path": path}

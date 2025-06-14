# Pfad: backend/app/simulation/redundancy.py

from collections import defaultdict, deque

# Beispielgraph (wird später aus echter Topologie gespeist)
graph = defaultdict(list)

def build_graph(links):
    graph.clear()
    for link in links:
        src = link["source"]
        dst = link["target"]
        weight = link.get("distance", 1)
        graph[src].append((dst, weight))
        graph[dst].append((src, weight))
    return graph

def dijkstra(source, failed_links=None):
    import heapq

    if failed_links is None:
        failed_links = []

    queue = [(0, source, [])]
    visited = set()
    paths = {}

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        paths[node] = path + [node]

        for neighbor, weight in graph[node]:
            if (node, neighbor) in failed_links or (neighbor, node) in failed_links:
                continue
            heapq.heappush(queue, (cost + weight, neighbor, path + [node]))

    return paths

def simulate_outage(devices, links, failed_device_id):
    failed_links = []
    for link in links:
        if link["source"] == failed_device_id or link["target"] == failed_device_id:
            failed_links.append((link["source"], link["target"]))

    build_graph(links)
    result = {}

    for device in devices:
        if device["id"] == failed_device_id:
            continue
        paths = dijkstra(device["id"])
        backup_paths = dijkstra(device["id"], failed_links)
        result[device["id"]] = {
            "primary": paths,
            "backup": backup_paths,
            "failed_links": failed_links
        }

    return result

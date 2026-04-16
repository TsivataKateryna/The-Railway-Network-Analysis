from collections import defaultdict
import pandas as pd

# INPUT_CSV = "data/belgium.csv"
INPUT_CSV = "data/total.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")
# print(df.head())

def number_of_nodes(df):
    """
    Returns the number of nodes in the graph
    """
    nodes_a = set(df["station_a"])
    nodes_b = set(df["station_b"])
    nodes = nodes_a.union(nodes_b)
    nodes.discard("")
    return len(nodes)

print(f"number_of_nodes {number_of_nodes(df)}")

def number_of_edges(df):
    """
    Returns the number of edges in the graph
    """
    # return len(df) -> TODO
    edges = set()
    for idx, row in df.iterrows():
        a = row["station_a"]
        b = row["station_b"]
        if a and b:
            edges.add(tuple(sorted((a, b))))
    return len(edges)

print(f"number_of_edges {number_of_edges(df)}")

def number_of_components(df):
    """
    Returns the number of components in the graph
    """
    adj = defaultdict(set)
    for a, b in zip(df["station_a"], df["station_b"]):
        if a and b:
            adj[a].add(b)
            adj[b].add(a)

    # DFS
    visited = set()
    components = 0

    for node in adj:
        if node in visited:
            continue
        components += 1
        stack = [node]
        visited.add(node)

        while stack:
            v = stack.pop()
            for n in adj.get(v, ()):
                if n not in visited:
                    visited.add(n)
                    stack.append(n)

    return components

def only_path(df):
    """
    Returns a list of strings representing the stations in the only path from "Ahlbeck_Grenze" to "Peenemunde".
    nb: the stations must be in order
    """
    src = "Ahlbeck_Grenze" 
    dst = "Peenemunde"
    adj = defaultdict(set)
    for a, b in zip(df["station_a"], df["station_b"]):
        if a and b:
            adj[a].add(b)
            adj[b].add(a)

    if src not in adj or dst not in adj:
        return []

    # BFS
    q = [src]
    parent = {src: None}
    qi = 0
    while qi < len(q):
        v = q[qi]
        qi += 1
        if v == dst:
            break
        for n in adj[v]:
            if n not in parent:
                parent[n] = v
                q.append(n)

    if dst not in parent:
        return []

    path = []
    cur = dst
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

def length_of_path(df):
    """
    Returns the length (float, in km) of the shortest path between "Ahlbeck_Grenze" to "Peenemunde".
    """
    path = only_path(df)
    # TODO


def shortest_path(df):
    """
    Returns the length (float, in km) of the shortest path between "Portarlington_Junction" and "Foyens_Junction"
    """
    src = "Portarlington_Junction"
    dst = "Foyens_Junction"
    # build adjacency + weights (undirected)
    adj = defaultdict(set)
    w = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"]).strip()
        b = str(row["station_b"]).strip()
        d = str(row["distance_km"]).strip()

        if not a or not b or not d:
            continue

        adj[a].add(b)
        adj[b].add(a)

        key = tuple(sorted((a, b)))
        if key not in w:
            w[key] = float(d)

    if src not in adj or dst not in adj:
        # print("case 1")
        return 0.0

    best = float("inf")
    visited = {src}
    stack = [(src, 0.0, iter(adj[src]))]

    while stack:
        v, dist_so_far, it = stack[-1]

        try:
            n = next(it)
        except StopIteration:
            stack.pop()
            if v != src:
                visited.remove(v)
            continue

        if n in visited:
            continue

        key = tuple(sorted((v, n)))
        new_dist = dist_so_far + w[key]
        if new_dist >= best:
            continue

        if n == dst:
            best = new_dist
            continue

        visited.add(n)
        stack.append((n, new_dist, iter(adj[n])))

    # print("case 2")
    if best == float("inf"):
        return 0.0
    return best

print(f"shortest_path {shortest_path(df)}")


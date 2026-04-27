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
    return len(df)

print(f"number_of_edges {number_of_edges(df)}")

def number_of_components(df):
    """
    Returns the number of components in the graph
    """
    adj = {}
    for idx, row in df.iterrows():
        a = row["station_a"]
        b = row["station_b"]
        if a and b:
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)

    # DFS
    visited = set()
    components = 0

    for node in adj:
        if node in visited:
            continue
        components += 1
        s = [node]
        visited.add(node)

        while s:
            v = s.pop()
            for n in adj.get(v, set()):
                if n not in visited:
                    visited.add(n)
                    s.append(n)

    return components

print(f"number_of_components {number_of_components(df)}")

def only_path(df):
    """
    Returns a list of strings representing the stations in the only path from "Ahlbeck_Grenze" to "Peenemunde".
    nb: the stations must be in order
    """
    src = "Ahlbeck_Grenze" 
    dst = "Peenemunde"
    adj = {}
    for idx, row in df.iterrows():
        a = row["station_a"]
        b = row["station_b"]
        if a and b:
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)

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

print(f"only_path {only_path(df)}")

def length_of_path(df):
    """
    Returns the length (float, in km) of the shortest path between "Ahlbeck_Grenze" to "Peenemunde".
    """
    path = only_path(df)

    w = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        d = str(row["distance_km"])

        key = (a, b) if a < b else (b, a)

        if key not in w:
            w[key] = float(d)

    result = 0.0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        key = (u, v) if u < v else (v, u)
        result += w[key]

    return result

print(f"length_of_path {length_of_path(df)}")


def shortest_path(df):
    """
    Returns the length (float, in km) of the shortest path between "Portarlington_Junction" and "Foyens_Junction"
    """
    src = "Portarlington_Junction"
    dst = "Foyens_Junction"

    adj = {}
    w = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        d = str(row["distance_km"])

        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

        key = (a, b) if a < b else (b, a)
        if key not in w:
            w[key] = float(d)

    if src not in adj or dst not in adj:
        # print("case 1")
        return 0.0

    best = float("inf")
    visited = set()

    def dfs(v, dist_so_far):
        nonlocal best
        if dist_so_far >= best:
            return
        if v == dst:
            best = dist_so_far
            return
        for n in adj.get(v, set()):
            if n in visited:
                continue
            key = (v, n) if v < n else (n, v)
            visited.add(n)
            dfs(n, dist_so_far + w[key])
            visited.remove(n)

    visited.add(src)
    dfs(src, 0.0)

    if best == float("inf"):
        # print("case 2") 
        return 0.0
    return best

print(f"shortest_path {shortest_path(df)}")

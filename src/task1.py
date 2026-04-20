import pandas as pd

# INPUT_CSV = "data/belgium.csv"
INPUT_CSV = "data/total.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def average_degree(df):
    """
    Returns the average degree of the nodes in the graph
    """
    deg = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])

        if not a or not b:
            continue

        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1

    if len(deg) == 0:
        return 0.0

    result_mean = sum(deg.values()) / len(deg)

    return result_mean

print(f"average_degree {(average_degree(df))}")

def number_of_bridges(df):
    """
    Returns the number of bridges in the graph
    """
    adj = {}
    edge_count = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if not a or not b:
            continue
        key = tuple(sorted((a, b)))
        edge_count[key] = edge_count.get(key, 0) + 1
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)

    timer = 0
    tin = {}
    low = {}
    visited = set()
    bridges = 0

    def dfs(v, parent):
        nonlocal timer, bridges
        visited.add(v)
        tin[v] = low[v] = timer
        timer += 1

        for to in adj[v]:
            if to == parent:
                k = tuple(sorted((v, parent)))
                if edge_count.get(k, 0) > 1:
                    low[v] = min(low[v], tin[parent])
                continue
            if to not in visited:
                dfs(to, v)
                low[v] = min(low[v], low[to])
                k = tuple(sorted((v, to)))
                if edge_count.get(k, 0) == 1 and low[to] > tin[v]:
                    bridges += 1
            else:
                low[v] = min(low[v], tin[to])

    for s in adj:
        if s not in visited:
            dfs(s, None)

    return bridges

print(f"number_of_bridges {number_of_bridges(df)}")

def number_of_local_bridges(df):
    """
    Returns the number of local bridges in the graph
    """
    adj = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if not a or not b:
            continue
        if a not in adj:
            adj[a] = set()
        if b not in adj:
            adj[b] = set()
        adj[a].add(b)
        adj[b].add(a)

    local_bridges = 0
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if not a or not b:
            continue
        na = adj[a] - {b}
        nb = adj[b] - {a}
        if na.isdisjoint(nb):
            local_bridges += 1

    return local_bridges

print(f"number_of_local_bridges {number_of_local_bridges(df)}")
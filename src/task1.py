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

        key = (a, b) if a < b else (b, a)
        edge_count[key] = edge_count.get(key, 0) + 1
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)

    timer = 0
    tin = {}
    low = {}
    visited = set()
    bridges = 0

    for s in adj:
        if s in visited:
            continue

        visited.add(s)
        tin[s] = low[s] = timer
        timer += 1

        # frame = [v, parent, next_index, parent_skipped]
        stack = [[s, None, 0, False]]
        while stack:
            v, parent, i, parent_skipped = stack[-1]
            neigh = adj.get(v, [])

            if i >= len(neigh):
                stack.pop()
                if parent is not None:
                    low[parent] = min(low[parent], low[v])
                    k = (v, parent) if v < parent else (parent, v)
                    if edge_count.get(k, 0) == 1 and low[v] > tin[parent]:
                        bridges += 1
                continue

            to = neigh[i]
            stack[-1][2] = i + 1

            if to == parent and not parent_skipped:
                stack[-1][3] = True
                continue

            if to in visited:
                low[v] = min(low[v], tin[to])
                continue

            visited.add(to)
            tin[to] = low[to] = timer
            timer += 1
            stack.append([to, v, 0, False])

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
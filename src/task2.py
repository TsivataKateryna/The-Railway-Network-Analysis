import pandas as pd


# INPUT_CSV = "data/belgium.csv"
INPUT_CSV = "data/total.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def clustering_coefficient(df, station):
    """
    Returns the clustering coefficient of a node named `station` in the graph
    """
    adj = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if a == b:
            continue
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    neib = adj.get(station)

    k = len(neib)
    if k < 2:
        return 0.0

    linked_pairs = 0
    for u in neib:
        for v in neib:
            if u < v and v in adj[u]:
                linked_pairs += 1

    return (2.0 * linked_pairs) / (k * (k - 1))

print(f" clustering_coefficient Berlin_Westhafen {clustering_coefficient(df, "Berlin_Westhafen")}")
print(f" clustering_coefficient Krakow_Gowny {clustering_coefficient(df, "Krakow_Gowny")}")
print(f" clustering_coefficient Amsterdam_Transformatorweg_Aansl {clustering_coefficient(df, "Amsterdam_Transformatorweg_Aansl.")}")
print(f" clustering_coefficient ROMA_TERMINI {clustering_coefficient(df, "ROMA_TERMINI")}")


def number_of_triangles(df):
    """
    Returns the number of triangles in the graph
    """
    adj = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if a == b:
            continue
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    n = 0
    for a in adj:
        for b in adj[a]:
            if b <= a:
                continue
            for c in adj[a] & adj[b]:
                if c > b:
                    n += 1
    return n

print(f"number_of_triangles {number_of_triangles(df)}")


def number_of_balanced_triangles(df):
    """
    Returns the number of balanced triangles in the graph
    """
    adj = {}
    dist = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if a == b:
            continue
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
        try:
            d = float(row["distance_km"])
        except (ValueError, TypeError):
            continue
        key = (a, b) if a < b else (b, a)
        dist[key] = d

    balanced = 0
    for a in adj:
        for b in adj[a]:
            if b <= a:
                continue
            for c in adj[a] & adj[b]:
                if c <= b:
                    continue
                s_ab = 1 if dist.get((a, b), 0.0) < 1.0 else -1
                s_ac = 1 if dist.get((a, c), 0.0) < 1.0 else -1
                s_bc = 1 if dist.get((b, c), 0.0) < 1.0 else -1
                if s_ab * s_ac * s_bc == 1:
                    balanced += 1
    return balanced

print(f"number_of_balanced_triangles {number_of_balanced_triangles(df)}")

def number_of_unbalanced_triangles(df):
    """
    Returns the number of unbalanced triangles in the graph
    """
    return number_of_triangles(df) - number_of_balanced_triangles(df)

print(f"number_of_unbalanced_triangles {number_of_unbalanced_triangles(df)}")


def gcc(df):
    """
    Returns global clustering coefficient of the graph
    """
    adj = {}
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if a == b:
            continue
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    triangles = 0
    for a in adj:
        for b in adj[a]:
            if b <= a:
                continue
            for c in adj[a] & adj[b]:
                if c > b:
                    triangles += 1

    closed_triplets = 3 * triangles

    open_triplets = 0
    for v in adj:
        for u in adj[v]:
            for w in adj[v]:
                if u < w and w not in adj[u]:
                    open_triplets += 1

    if open_triplets == 0:
        return 0.0
    return closed_triplets / open_triplets

print(f"gcc {gcc(df)}")
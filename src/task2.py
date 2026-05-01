import pandas as pd

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

    neib = adj.get(station, set())

    k = len(neib)
    if k < 2:
        return 0.0

    linked_pairs = 0
    for u in neib:
        for v in neib:
            if u < v and v in adj[u]:
                linked_pairs += 1

    return (2.0 * linked_pairs) / (k * (k - 1))

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

    triangles = 0
    for a in adj:
        for b in adj[a]:
            if b <= a:
                continue
            for c in adj[a] & adj[b]:
                if c > b:
                    triangles += 1
    return triangles


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

        d = float(row["distance_km"])

        mini = a
        maxi = b
        if b < a:
            mini = b
            maxi = a
        key = (mini, maxi)
        dist[key] = d

    balanced = 0
    
    def edge_sign(x, y):
        key = (x, y) if x < y else (y, x)
        return 1 if dist.get(key, 0.0) < 1.0 else -1

    for a in adj:
        for b in adj[a]:
            if b <= a:
                continue
            for c in adj[a] & adj[b]:
                if c <= b:
                    continue
                if edge_sign(a, b) * edge_sign(a, c) * edge_sign(b, c) == 1:
                    balanced += 1

    return balanced

def number_of_unbalanced_triangles(df):
    """
    Returns the number of unbalanced triangles in the graph
    """
    return number_of_triangles(df) - number_of_balanced_triangles(df)

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

    triangles = number_of_triangles(df)
    closed_triplets = 3 * triangles

    total_triplets = 0
    for v in adj:
        k = len(adj[v])
        if k >= 2:
            total_triplets += (k * (k - 1)) // 2

    if total_triplets == 0:
        return 0.0
    return closed_triplets / total_triplets


if __name__ == "__main__":

    df = pd.read_csv("data/total.csv", dtype=str).fillna("")

    print("Clustering coefficients:")
    print("Berlin_Westhafen:", clustering_coefficient(df, "Berlin_Westhafen"))
    print("Krakow_Gowny:", clustering_coefficient(df, "Krakow_Gowny"))
    print("Amsterdam_Transformatorweg_Aansl.:", clustering_coefficient(df, "Amsterdam_Transformatorweg_Aansl."))
    print("ROMA_TERMINI:", clustering_coefficient(df, "ROMA_TERMINI"))

    print("\nGlobal metrics:")
    print("Number of triangles:", number_of_triangles(df))
    print("Balanced triangles:", number_of_balanced_triangles(df))
    print("Unbalanced triangles:", number_of_unbalanced_triangles(df))
    print("GCC:", gcc(df))
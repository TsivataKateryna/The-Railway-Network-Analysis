import pandas as pd
from collections import defaultdict


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")


def _build_weighted_graph(df):
    adj = defaultdict(dict)
    for idx, row in df.iterrows():
        a = str(row.get("station_a", ""))
        b = str(row.get("station_b", ""))
        if not a or not b or a == b:
            continue

        try:
            d = float(row.get("distance_km", ""))
        except (TypeError, ValueError):
            continue

        if d <= 0:
            continue

        if b not in adj[a] or d < adj[a][b]:
            adj[a][b] = d
            adj[b][a] = d
    return adj


def score(df, station):
    """
    Returns the score (as defined in the project statement) of a node named `station` in the graph
    """
    adj = _build_weighted_graph(df)
    stat = str(station)

    deg = {}
    for u, n in adj.items():
        deg[u] = len(n)

    if stat not in adj:
        #print("asdfg")
        return 0.0

    if deg.get(stat, 0) <= 0:
        return 0.0

    total = 0.0
    for i, d_ni in adj.get(stat, {}).items():
        if d_ni <= 0:
            return 0.0
        if deg.get(i, 0) <= 0:
            return 0.0

        summ = 0.0
        for j, d_ij in adj.get(i, {}).items():
            if j == stat:
                continue
            if d_ij <= 0 or deg.get(j, 0) <= 0:
                return 0.0
            summ += float(deg[j]) * float(d_ij)

        total += (float(deg[i]) / float(d_ni)) * summ

    return float(deg[stat]) * total

def gain_from_split(df, station_a, station_b):
    """
    Returns the gain (criterion defined above) from splitting the edge station_a - station_b.
    """
    u = str(station_a)
    v = str(station_b)

    adj = _build_weighted_graph(df)
    if u not in adj or v not in adj.get(u, {}):
        return 0.0

    def sum_scores(graph):
        deg = {x: len(nbrs) for x, nbrs in graph.items()}
        t = 0.0

        for x, x_n in graph.items():
            if deg.get(x, 0) <= 0:
                continue
            total = 0.0
            valid = True
            for i, d_xi in x_n.items():
                if d_xi <= 0 or deg.get(i, 0) <= 0:
                    valid = False
                    break
                summ = 0.0
                for j, d_ij in graph.get(i, {}).items():
                    if j == x:
                        continue
                    if d_ij <= 0 or deg.get(j, 0) <= 0:
                        valid = False
                        break
                    summ += float(deg[j]) * float(d_ij)
                if not valid:
                    break
                total += (float(deg[i]) / float(d_xi)) * summ
            if not valid:
                continue
            t += float(deg[x]) * total

        return t

    old_sum = sum_scores(adj)
    denom = score(df, u) + score(df, v)

    adj2 = {}
    for stat, n in adj.items():
        adj2[stat] = dict(n)

    d_uv = adj2[u][v]
    result = d_uv / 2.0

    adj2[u].pop(v, None)
    adj2[v].pop(u, None)

    left, right = (u, v) if u <= v else (v, u)
    base_mid = f"{left}__SPLIT__{right}"
    mid = base_mid
    constant = 1
    while mid in adj2:
        constant += 1
        mid = f"{base_mid}_{constant}"

    adj2[mid] = {u: result, v: result}
    adj2[u][mid] = result
    adj2[v][mid] = result

    new_sum = sum_scores(adj2)

    final = new_sum - old_sum

    if denom == 0:
        # print("here")
        return 0.0
    return (final * float(d_uv) * 100.0) / float(denom)
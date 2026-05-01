import heapq
from collections import defaultdict

import pandas as pd


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")


def _build_weighted_graph(df):
    adj = defaultdict(dict)
    for idx, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if a == b:
            continue
        d = float(row["distance_km"])
        if b not in adj[a] or d < adj[a][b]:
            adj[a][b] = d
            adj[b][a] = d
    return adj


def _betweenness_raw(adj):
    V = list(adj.keys())
    n = len(V)
    if n < 3:
        return dict.fromkeys(V, 0.0)

    C_B = defaultdict(float)
    eps = 1e-12

    for s in V:
        P = defaultdict(list)
        d = {s: 0.0}
        sigma = defaultdict(float)
        sigma[s] = 1.0
        Q = [(0.0, s)]  # Dijkstra priority queue (BFS queue in unweighted version)
        S = []
        settled = set()

        while Q:
            d_v, v = heapq.heappop(Q)
            if abs(d_v - d.get(v, float("inf"))) > eps:
                continue
            if v in settled:
                continue
            settled.add(v)
            S.append(v)
            for w, len_vw in adj[v].items():
                nd = d_v + len_vw
                if w not in d or nd + eps < d[w]:
                    d[w] = nd
                    sigma[w] = sigma[v]
                    P[w] = [v]
                    heapq.heappush(Q, (nd, w))
                elif abs(nd - d[w]) <= eps:
                    sigma[w] += sigma[v]
                    P[w].append(v)

        delta = defaultdict(float)
        for w in reversed(S):
            coeff = (1.0 + delta[w]) / sigma[w] if sigma[w] else 0.0
            for v in P[w]:
                delta[v] += sigma[v] * coeff
            if w != s:
                C_B[w] += delta[w]

    for v in C_B:
        C_B[v] *= 0.5
    for v in V:
        C_B.setdefault(v, 0.0)
    return C_B


def betweenness_centrality(df, station):
    """
    Returns the betweenness centrality score of a node named `station` in the graph
    (normalized by (|V|-1)(|V|-2)/2 as in the project statement).
    """
    adj = _build_weighted_graph(df)
    if station not in adj:
        return 0.0

    n = len(adj)
    denom = (n - 1) * (n - 2) / 2.0
    if denom <= 0:
        return 0.0

    raw = _betweenness_raw(adj)
    return raw.get(station, 0.0) / denom


if __name__ == "__main__":
    adj = _build_weighted_graph(df)
    raw = _betweenness_raw(adj)

    n = len(adj)
    denom = (n - 1) * (n - 2) / 2.0
    if denom <= 0 or not raw:
        print("Graph too small to compute betweenness centrality.")
    else:
        normalized = {v: raw_v / denom for v, raw_v in raw.items()}
        best_station, best_value = max(normalized.items(), key=lambda kv: kv[1])
        print(f"station_with_highest_betweenness {best_station}")
        print(f"highest_betweenness_value {best_value}")









import matplotlib.pyplot as plt

adj = _build_weighted_graph(df)   # 🔥 construire le graphe
betweenness = _betweenness_raw(adj)  # 🔥 passer adj (PAS df)

values = list(betweenness.values())

plt.hist(values, bins=20)
plt.title("Betweenness centrality distribution")
plt.xlabel("Centrality")
plt.ylabel("Number of nodes")
plt.savefig("histogram_task3.png")

print("Histogram saved as histogram_task3.png")
import heapq
from collections import defaultdict

import pandas as pd


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")


def _build_weighted_graph(df):
    """Undirected graph: for each pair keep the minimum edge length (shortest direct link)."""
    adj = defaultdict(dict)
    for _, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if a == b:
            continue
        try:
            w = float(row["distance_km"])
        except (ValueError, TypeError):
            continue
        if b not in adj[a] or w < adj[a][b]:
            adj[a][b] = w
            adj[b][a] = w
    return adj


def _betweenness_raw(adj):
    """
    Unweighted shortest-path betweenness on positive weighted undirected graph.
    Brandes + Dijkstra; undirected double-counting removed by factor 1/2.
    """
    nodes = list(adj.keys())
    n = len(nodes)
    if n < 3:
        return {v: 0.0 for v in nodes}

    between = defaultdict(float)
    eps = 1e-12

    for s in nodes:
        pred = defaultdict(list)
        dist = {s: 0.0}
        sigma = defaultdict(float)
        sigma[s] = 1.0
        heap = [(0.0, s)]
        order = []
        settled = set()

        while heap:
            d_v, v = heapq.heappop(heap)
            if abs(d_v - dist.get(v, float("inf"))) > eps:
                continue
            if v in settled:
                continue
            settled.add(v)
            order.append(v)
            for w, len_vw in adj[v].items():
                nd = d_v + len_vw
                if w not in dist or nd + eps < dist[w]:
                    dist[w] = nd
                    sigma[w] = sigma[v]
                    pred[w] = [v]
                    heapq.heappush(heap, (nd, w))
                elif abs(nd - dist[w]) <= eps:
                    sigma[w] += sigma[v]
                    pred[w].append(v)

        delta = defaultdict(float)
        for w in reversed(order):
            coeff = (1.0 + delta[w]) / sigma[w] if sigma[w] else 0.0
            for v in pred[w]:
                delta[v] += sigma[v] * coeff
            if w != s:
                between[w] += delta[w]

    for v in between:
        between[v] *= 0.5
    for v in nodes:
        between.setdefault(v, 0.0)
    return between


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

import pandas as pd
import math
from collections import defaultdict


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

_CACHE = {
    "df_id": None,
    "adj": None,   # dict[str, dict[str, float]]
    "deg": None,   # dict[str, int]
    "score": None  # dict[str, float]
}


def _build_weighted_graph(df):
    """Undirected graph: keep the minimum distance per unordered pair."""
    adj = defaultdict(dict)
    for _, row in df.iterrows():
        a = str(row["station_a"])
        b = str(row["station_b"])
        if a == b:
            continue
        d = float(row["distance_km"])
        if d <= 0:
            # Defensive: distances are expected positive; ignore invalid entries.
            continue
        if b not in adj[a] or d < adj[a][b]:
            adj[a][b] = d
            adj[b][a] = d
    return dict(adj)


def _prepare(df):
    df_id = id(df)
    if _CACHE["df_id"] == df_id and _CACHE["adj"] is not None:
        return _CACHE["adj"], _CACHE["deg"]

    adj = _build_weighted_graph(df)
    deg = {u: len(nbrs) for u, nbrs in adj.items()}

    _CACHE["df_id"] = df_id
    _CACHE["adj"] = adj
    _CACHE["deg"] = deg
    _CACHE["score"] = {}
    return adj, deg


def _score_from(adj, deg, station):
    if station not in adj:
        return 0.0
    k = deg.get(station, 0)
    if k <= 0:
        return 0.0

    # Compute in log-space to reduce overflow.
    log_s = math.log(float(k))
    for i, d_ni in adj[station].items():
        di = deg.get(i, 0)
        if di <= 0 or d_ni <= 0:
            return 0.0

        log_s += math.log(float(di)) - math.log(float(d_ni))

        # Product over j in Neighbours(i) \ {station} of deg(j) * d(i, j).
        for j, d_ij in adj[i].items():
            if j == station:
                continue
            dj = deg.get(j, 0)
            if dj <= 0 or d_ij <= 0:
                return 0.0
            log_s += math.log(float(dj)) + math.log(float(d_ij))

    # exp bounds for double precision
    if log_s > 709.0:
        return float("inf")
    if log_s < -745.0:
        return 0.0
    return math.exp(log_s)


def _nodes_within_two_hops(adj, seeds):
    out = set(seeds)
    frontier = set(seeds)
    for _ in range(2):
        nxt = set()
        for u in frontier:
            for v in adj.get(u, {}):
                if v not in out:
                    out.add(v)
                    nxt.add(v)
        frontier = nxt
        if not frontier:
            break
    return out


def score(df, station):
    """
    Returns the score (as defined in the project statement) of a node named `station` in the graph
    """
    adj, deg = _prepare(df)
    cache = _CACHE["score"]
    if station in cache:
        return cache[station]
    s = _score_from(adj, deg, station)
    cache[station] = s
    return s

def gain_from_split(df, station_a, station_b):
    """
    Returns the gain (criterion defined above) from splitting the edge station_a - station_b.
    """
    adj, deg = _prepare(df)
    u = str(station_a)
    v = str(station_b)
    if u not in adj or v not in adj[u]:
        return 0.0

    # Old scores for affected nodes (only nodes within 2 hops of {u, v} can change).
    affected = _nodes_within_two_hops(adj, {u, v})
    old_sum = 0.0
    for x in affected:
        old_sum += score(df, x)

    # Build a local modified graph for the affected region only.
    adj2 = {x: dict(adj.get(x, {})) for x in affected}
    deg2 = {x: deg.get(x, 0) for x in affected}

    # Add the new station in the middle of edge (u, v).
    d_uv = adj[u][v]
    mid = f"{u}__SPLIT__{v}"
    half = d_uv / 2.0

    # Remove original edge.
    adj2[u].pop(v, None)
    adj2[v].pop(u, None)

    # Ensure u and v stay in local structure.
    adj2.setdefault(u, {})
    adj2.setdefault(v, {})

    # Insert midpoint connections.
    adj2[mid] = {u: half, v: half}
    adj2[u][mid] = half
    adj2[v][mid] = half

    # Update degrees.
    deg2[u] = len(adj2[u])
    deg2[v] = len(adj2[v])
    deg2[mid] = 2

    # Some nodes in affected might point to u/v; their adjacency wasn't changed,
    # but u/v degree changed, so their score may change (handled by recomputation).

    new_sum = 0.0
    for x in affected:
        new_sum += _score_from(adj2, deg2, x)
    new_sum += _score_from(adj2, deg2, mid)

    return new_sum - old_sum
import pandas as pd


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def betweenness_centrality(df, station):
    """
    Returns the betweenness centrality score of a node named `station` in the graph
    """
    return 0
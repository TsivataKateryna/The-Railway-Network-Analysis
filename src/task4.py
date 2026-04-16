import pandas as pd


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def score(df, station):
    """
    Returns the score (as defined in the project statement) of a node named `station` in the graph
    """
    return 0

def gain_from_split(df, station_a, station_b):
    """
    Returns the gain (criterion defined above) from splitting the edge station_a - station_b.
    """
    return 0
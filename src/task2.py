import pandas as pd


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def clustering_coefficient(df, station):
    """
    Returns the clustering coefficient of a node named `station` in the graph
    """
    return 0

def number_of_triangles(df):
    """
    Returns the number of triangles in the graph
    """
    return 0

def number_of_balanced_triangles(df):
    """
    Returns the number of balanced triangles in the graph
    """
    return 0

def number_of_unbalanced_triangles(df):
    """
    Returns the number of unbalanced triangles in the graph
    """
    return 0


def gcc(df):
    """
    Returns global clustering coefficient of the graph
    """
    return 0
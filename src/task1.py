import pandas as pd


# INPUT_CSV = "data/belgium.csv"
INPUT_CSV = "data/total.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def average_degree(df):
    """
    Returns the average degree of the nodes in the graph
    """
    return 0

def number_of_bridges(df):
    """
    Returns the number of bridges in the graph
    """
    return 0

def number_of_local_bridges(df):
    """
    Returns the number of local bridges in the graph
    """
    return 0
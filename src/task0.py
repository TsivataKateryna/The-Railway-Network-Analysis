import pandas as pd


INPUT_CSV = "data/belgium.csv"
df = pd.read_csv(INPUT_CSV, dtype=str).fillna("")

def number_of_nodes(df):
    """
    Returns the number of nodes in the graph
    """
    return 0

def number_of_edges(df):
    """
    Returns the number of edges in the graph
    """
    return 0

def number_of_components(df):
    """
    Returns the number of components in the graph
    """
    return 0

def only_path(df):
    """
    Returns a list of strings representing the stations in the only path from "Ahlbeck_Grenze" to "Peenemunde".
    nb: the stations must be in order
    """
    src = "Ahlbeck_Grenze" 
    dst = "Peenemunde"
    return []

def length_of_path(df):
    """
    Returns the length (float, in km) of the shortest path between "Ahlbeck_Grenze" to "Peenemunde".
    """
    path = only_path(df)

    return 0


def shortest_path(df):
    """
    Returns the length (float, in km) of the shortest path between "Portarlington_Junction" and "Foyens_Junction"
    """
    src = "Portarlington_Junction"
    dst = "Foyens_Junction"
    return 0


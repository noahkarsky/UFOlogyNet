# we need to make a way to read in the data
import pandas as pd
import networkx as nx

def read_in_data(dataset_selection):
    """
    Reads in the data from JSON files and returns the dataframes.

    Returns:
        tuple: A tuple containing the dataframe for nodes and the dataframe for edges.

    Examples:
        >>> df_nodes, df_edges = read_in_data()
    """
    if dataset_selection == "Phenomena Timeline Data":
        node_path = r"data/phenomena_timeline_nodes.json"
        edge_path = r"data/phenomena_timeline_edges.json"
    elif dataset_selection == "Project Amanita Data":
        node_path = r"data/project_amanita_nodes.json"
        edge_path = r"data/project_amanita_edges.json"

    df_nodes = pd.read_json(node_path)
    df_edges = pd.read_json(edge_path)
    return df_nodes, df_edges


def get_neighborhood(G, node, radius=1):
    """
    Get the neighborhood of a node in a graph.

    Args:
        G (networkx.Graph): The graph object.
        node (str): The node to get the neighborhood of.
        radius (int, optional): The radius of the neighborhood. Defaults to 1.

    Returns:
        set: A set of nodes in the neighborhood.
    """
    # Create an undirected version of the graph
    G_undirected = G.to_undirected()

    neighborhood = {node}
    for _ in range(radius):
        neighborhood.update(
            [
                neighbor
                for n in neighborhood.copy()  # We need to iterate over a copy of the set because we're modifying it in the loop
                for neighbor in G_undirected.neighbors(n)
                if neighbor not in neighborhood
            ]
        )
    return neighborhood

def filter_dataframes(node_name, df_nodes, df_edges):
    """
    Filters the given dataframes based on a specified node name.

    Args:
        node_name (str): The name of the node to filter on.
        df_nodes (pandas.DataFrame): The dataframe containing the nodes data.
        df_edges (pandas.DataFrame): The dataframe containing the edges data.

    Returns:
        tuple: A tuple containing the filtered nodes dataframe and the filtered edges dataframe.

    Examples:
        >>> df_nodes, df_edges = filter_dataframes("Node1", df_nodes, df_edges)
    """

    # first check if the node name is "all", if so return the original dataframes
    if node_name == "ALL":
        return df_nodes, df_edges

    df_nodes_filtered = df_nodes[df_nodes["name"] == node_name]
    # grab the node id
    node_id = df_nodes_filtered["id"].values[0]
    
    # filter edges
    df_edges_filtered = df_edges[
        (df_edges["source"] == node_id) | (df_edges["target"] == node_id)
    ]
    # we need to add the nodes that are connected to the node we are filtering on
    for index, row in df_edges_filtered.iterrows():
        if row["source"] == node_id:
            df_nodes_filtered = pd.concat(
                [
                    df_nodes_filtered,
                    df_nodes[df_nodes["id"] == row["target"]],
                ]
            )
        else:
            df_nodes_filtered = pd.concat(
                [
                    df_nodes_filtered,
                    df_nodes[df_nodes["id"] == row["source"]],
                ]
            )

    return df_nodes_filtered, df_edges_filtered
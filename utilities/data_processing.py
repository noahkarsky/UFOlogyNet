# we need to make a way to read in the data
import pandas as pd


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
        print("returning original dataframes")
        return df_nodes, df_edges

    df_nodes_filtered = df_nodes[df_nodes["name"] == node_name]
    # filter edges
    df_edges_filtered = df_edges[
        (df_edges["source"] == node_name) | (df_edges["target"] == node_name)
    ]
    # we need to add the nodes that are connected to the node we are filtering on
    for index, row in df_edges_filtered.iterrows():
        if row["source"] == node_name:
            df_nodes_filtered = pd.concat(
                [
                    df_nodes_filtered,
                    df_nodes[df_nodes["name"] == row["target"]],
                ]
            )
        else:
            df_nodes_filtered = pd.concat(
                [
                    df_nodes_filtered,
                    df_nodes[df_nodes["name"] == row["source"]],
                ]
            )

    return df_nodes_filtered, df_edges_filtered


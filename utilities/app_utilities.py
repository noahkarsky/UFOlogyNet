import yaml
import gravis as gv
import networkx as nx

import os

# Get the absolute path to the config.yaml file
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.yaml")

with open(config_path, "r") as file:
    config = yaml.safe_load(file)
node_color_map = config["node_color_map"]


def assign_color(node_type):
    if node_type in node_color_map:
        return node_color_map.get(node_type)
    else:
        return node_color_map.get("")


def make_graph(df_nodes, df_edges):
    """
    Makes a graph from the given nodes and edges dataframes.

    Args:
        df_nodes (pandas.DataFrame): The dataframe containing the nodes data.
        df_edges (pandas.DataFrame): The dataframe containing the edges data.

    Returns:
        networkx.Graph: A graph object.

    Examples:
        >>> G = make_graph(df_nodes, df_edges)
    """
    G = nx.DiGraph()
    for index, row in df_nodes.iterrows():
        G.add_node(
            row["id"],
            label=row["name"],
            group=row["type"],
            color=assign_color(row["type"]),
            hover=[
                row.properties["properties.notes"]
                if "properties.notes" in row.properties
                else ""
            ][0],
        )

    for index, row in df_edges.iterrows():
        # also we want to show an arrow for the direction of the relationship
        G.add_edge(
            row["source"], row["target"],
             label=row["relationship_type"],
              arrows=True
        )

    centrality = nx.degree_centrality(G)
    nx.set_node_attributes(G, centrality, "size")
    return G


def make_plot(G, input_dict):
    return gv.d3(G, **input_dict)

from utilities.data_processing import read_in_data, get_neighborhood
from utilities.app_utilities import make_graph, make_plot

import streamlit as st
import yaml

import streamlit.components.v1 as components

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
gravis_plot_config = config["gravis_plot_config"]


# APP DESIGN
# make st wide
st.set_page_config(layout="wide")
st.title("Anonymous Phenomena Timeline - Knowledge Graph")
st.markdown(
    """
On this app, one can explore two datasets.

1. Project Amanita Data - A curated, not always referenced collection of events, peoples, places, and things related to the UAP phenomenon that I have come across in my research. I have added to it, and will continue to do so. I hope to make it a useful tool for researchers and enthusiasts alike.
2. Phenomena Timeline Data - A knowledge graph representation of [the author-unknown timeline of UAP historical events](https://pdfhost.io/v/gR8lAdgVd_Uap_Timeline_Prepared_By_Another), released during the [July 26 Congressional hearings](https://time.com/6298287/congress-ufo-hearing/), into a knowledge graph. 

The data was compiled into a markdown file, I programatically pulled entities and relationships from the file, cleaned the data a bit, and made a graph.
At this stage it is more of a fun thing to mess around with, but I hope to add more functionality to make it a viable research tool.

The now deprecated [Project Amanita](https://github.com/noahkarsky/project-amanita?tab=readme-ov-file/), and added to it. I think I will keep expanding it as I sift through this timeline data mode, and eventually merge the two of them in a useful way.

hit me up on twitter [@noahkarsky](https://twitter.com/noahkarsky) if you have any questions or comments.
    """
)
# create a dropdown where people slect eith "Phenomena Timeline Data" or "Project Amanita Data

dataset_selection = st.selectbox(
    "Select a dataset", [ "Project Amanita Data","Phenomena Timeline Data"]
)


df_nodes, df_edges = read_in_data(dataset_selection)


# Get a list of all nodes
all_nodes = df_nodes["name"].unique().tolist()
all_nodes.insert(0, "ALL")  # Add "ALL" option to the list
# Create a dropdown menu for node selection
selected_node = st.selectbox("Select a node to explore a subset of the graph", all_nodes)

#get the id of the selected node


G = make_graph(df_nodes, df_edges)

if selected_node != "ALL":
    selected_node_id = df_nodes[df_nodes["name"] == selected_node]["id"].values[0]
    # lets get the neighborhood of the selected node
    filtered_nodes = get_neighborhood(G, selected_node_id, radius=2)
    G = G.subgraph(filtered_nodes)


graph_vis = make_plot(G, gravis_plot_config)


components.html(graph_vis.to_html(), height=1200)  # << adjust if needed
#lets print some statistics about the graph
st.subheader("Graph Statistics (to be added to in the future))")
st.markdown(f"Number of nodes: {len(G.nodes())}")
st.markdown(f"Number of edges: {len(G.edges())}")

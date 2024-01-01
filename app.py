from utilities.data_processing import read_in_data, filter_dataframes
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

This is a small project to turn [the author-unknown timeline of UAP historical events](https://pdfhost.io/v/gR8lAdgVd_Uap_Timeline_Prepared_By_Another), released during the [July 26 Congressional hearings](https://time.com/6298287/congress-ufo-hearing/), into a knowledge graph. 
It helps to view the app in full screen, if not sometimes the nodes can be found dragging around the graph.**It may take several seconds for ALL nodes to render**
    
    """
)
#create a dropdown where people slect eith "Phenomena Timeline Data" or "Project Amanita Data

dataset_selection = st.selectbox('Select a dataset', ['Phenomena Timeline Data', 'Project Amanita Data'])


df_nodes, df_edges = read_in_data(dataset_selection)


# Get a list of all nodes
all_nodes = df_nodes['name'].unique().tolist()
all_nodes.insert(0, "ALL")  # Add "ALL" option to the list




# Create a dropdown menu for node selection
selected_node = st.selectbox('Select a node', all_nodes)

df_nodes_filtered, df_edges_filtered = filter_dataframes(selected_node, df_nodes, df_edges)
G = make_graph(df_nodes_filtered, df_edges_filtered)
graph_vis = make_plot(G,gravis_plot_config)


components.html(graph_vis.to_html(), height=900) # << adjust if needed

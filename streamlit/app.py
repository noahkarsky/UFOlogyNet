import streamlit
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
from data_import_formatting import import_and_format_data

import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

node_color_map = config['node_color_map']
#data import and formatting
nodes,edges = import_and_format_data('../data/graph_data.json')

#### FUNCTIONS ####
def find_related_nodes(node_id, edges_df, degree=2):
    related = [node_id]
    for _ in range(degree):
        new_related = edges_df[edges_df['source'].isin(related)]['target'].tolist()
        #add also things pointing to the node
        new_related.extend(edges_df[edges_df['target'].isin(related)]['source'].tolist())
        related.extend(new_related)
        related = list(set(related))  # remove duplicates
        print(related)
    return related


#APP DESIGN
# APP DESIGN
# Create two columns
col1, col2 = streamlit.columns([8, 2])  # 8:2 ratio, adjust as needed
# Add a dropdown menu for node selection in the first column
with col1:
    selected_node = streamlit.selectbox('Select a node', nodes['id'].tolist())

# Add a legend in the second column
with col2:
    streamlit.markdown("## Legend")
    for node_type, color in node_color_map.items():
        streamlit.markdown(f"<span style='color: {color};'>■</span> {node_type}", unsafe_allow_html=True)

# APP FUNCTIONALITY (in the first column)
with col1:
    related_nodes = find_related_nodes(selected_node, edges, degree=2)
    # Filter the nodes and edges for the graph
    filtered_nodes = nodes[nodes['id'].isin(related_nodes)]
    filtered_edges = edges[edges['source'].isin(related_nodes) & edges['target'].isin(related_nodes)]
    # Convert to list
    nodes_list = filtered_nodes['Node'].tolist()
    edges_list = filtered_edges['Edge'].tolist()

    # Display the graph
    config = Config(width=3000, 
                    height=700, 
                    directed=True,
                    # nodeHighlightBehavior=True, 
                    # highlightColor="#F7A7A6",
                    collapsible=True, 
                    physics=False, 
                    hierarchical=False,
                    staticGraphWithDragAndDrop=True,
                    graphviz_layout=True,
                    )

    return_value = agraph(nodes=nodes_list, edges=edges_list, config=config)

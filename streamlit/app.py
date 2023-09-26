import streamlit
from streamlit_agraph import agraph, Config
from data_import_formatting import import_and_format_data
import yaml
import networkx as nx

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

node_color_map = config['node_color_map']
#data import and formatting
nodes,edges = import_and_format_data('../data/graph_data.json')

#### FUNCTIONS ####
def find_related_nodes_efficient(node_id, edges_df, degree=2):
    G = nx.from_pandas_edgelist(edges_df, 'source', 'target')
    related = nx.single_source_shortest_path_length(G, node_id, cutoff=degree)
    return list(related.keys())


#APP DESIGN
#make streamlit wide
streamlit.set_page_config(layout="wide")
# Create two columns
col1, col2 = streamlit.columns([9, 1]) 
# Add a dropdown menu for node selection in the first column
with col1:
    # Adding 'ALL' to the list of node IDs
    node_options = ['ALL'] + nodes['id'].tolist()
    selected_node = streamlit.selectbox('Select a node', node_options)

# Add a legend in the second column
with col2:
    streamlit.markdown("## Legend")
    for node_type, color in node_color_map.items():
        streamlit.markdown(f"<span style='color: {color};'>■</span> {node_type}", unsafe_allow_html=True)

# APP FUNCTIONALITY (in the first column)
with col1:
    if selected_node == 'ALL':
        # If 'ALL' is selected, include all nodes and edges
        filtered_nodes = nodes
        filtered_edges = edges
    else:
        related_nodes = find_related_nodes_efficient(selected_node, edges, degree=2)
        # Filter the nodes and edges for the graph based on related_nodes
        filtered_nodes = nodes[nodes['id'].isin(related_nodes)]
        filtered_edges = edges[edges['source'].isin(related_nodes) & edges['target'].isin(related_nodes)]

    nodes_list = filtered_nodes['Node'].tolist()
    edges_list = filtered_edges['Edge'].tolist()

    # Display the graph
    config = Config(width=3000, 
                    height=700, 
                    directed=True,
                    # nodeHighlightBehavior=True, 
                    # highlightColor="#F7A7A6",
                    collapsible=True, 
                    physics=True, 
                    hierarchical=False,
                    staticGraphWithDragAndDrop=True,
                    graphviz_layout=True,
                    )

    return_value = agraph(nodes=nodes_list, edges=edges_list, config=config)

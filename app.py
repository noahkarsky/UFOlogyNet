import streamlit as st
from streamlit_agraph import agraph, Config
from data_import_formatting import import_and_format_data, make_wordcloud, make_word_count_bar_chart
import yaml
import networkx as nx

from collections import Counter
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

node_color_map = config["node_color_map"]
# data import and formatting
nodes, edges = import_and_format_data()


#### FUNCTIONS ####
def find_related_nodes_efficient(node_id, edges_df, degree=2):
    G = nx.from_pandas_edgelist(edges_df, "source", "target")
    related = nx.single_source_shortest_path_length(G, node_id, cutoff=degree)
    return list(related.keys())


# Function to perform the graph rendering
def render_graph(selected_node, nodes, edges):
    if selected_node == "ALL(takes a second to load)":
        filtered_nodes = nodes
        filtered_edges = edges
        physics = True
    else:
        related_nodes = find_related_nodes_efficient(selected_node, edges, degree=2)
        filtered_nodes = nodes[nodes["id"].isin(related_nodes)]
        filtered_edges = edges[
            edges["source"].isin(related_nodes) & edges["target"].isin(related_nodes)
        ]
        physics = False

    nodes_list = filtered_nodes["Node"].tolist()
    edges_list = filtered_edges["Edge"].tolist()

    config = Config(
        width=3000,
        height=700,
        directed=True,
        # nodeHighlightBehavior=True,
        # highlightColor="#F7A7A6",
        collapsible=True,
        physics=physics,
        hierarchical=False,
        graphviz_layout=True,
    )

    return agraph(nodes=nodes_list, edges=edges_list, config=config)


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



# Create two columns
col1, col2 = st.columns([9, 1])
# Add a dropdown menu for node selection in the first column
with col1:
    # Adding 'ALL' to the list of node IDs
    node_options = ["ALL(takes a second to load)"] + nodes["id"].tolist()
    selected_node = st.selectbox("Select a node", node_options)

# Add a legend in the second column
with col2:
    st.markdown("## Legend")
    for node_type, color in node_color_map.items():
        st.markdown(
            f"<span style='color: {color};'>■</span> {node_type}",
            unsafe_allow_html=True,
        )

# APP FUNCTIONALITY (in the first column)
with col1:
    render_graph(selected_node, nodes, edges)



left_co,last_co = st.columns(2)
with left_co:
    st.plotly_chart(make_word_count_bar_chart(edges),use_container_width=True)
    

with last_co:
    st.image(make_wordcloud(edges).to_array(),width=1200)
    st.markdown("Wordcloud of the nodes in the timeline.",)

st.markdown(
    """
Find the github repo [here](https://github.com/noahkarsky/anonymous_phenomena_timeline).
Check out my other knowledge graph build off my own research here: [Project Amanita Knowledge Graph](https://noahkarsky.github.io/project-amanita/).
"""
)

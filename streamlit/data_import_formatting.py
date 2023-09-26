from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd
# make a function to import data from a json file with the above format
import yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

node_color_map = config['node_color_map']

import json
def import_json_data(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data


def import_and_format_data(json_file):

    #data import and formatting
    data = import_json_data('../data/graph_data.json')
    #make this into somethign graphistry can read
    nodes = pd.DataFrame(data['nodes'])
    edges = pd.DataFrame(data['edges'])

    #correct the value 'groip' to 'group' found in the type column
    nodes['type'] = nodes['type'].str.replace('groip', 'group')

    #add color to nodes df
    nodes['color'] = nodes['type'].map(node_color_map)
    nodes['Node']  = nodes.apply(lambda x: Node(id=x['id'], label=x['node_edited'], size=10,shape='dot' ,color =x['color']), axis=1)
    edges['Edge'] = edges.apply(lambda x: Edge(source=x['source'], target=x['target'], label=x['relationship_type']), axis=1)
    
    
    return nodes, edges
from streamlit_agraph import Node, Edge
import pandas as pd
from wordcloud import WordCloud
import numpy as np
from collections import Counter
import json
import yaml
import plotly.express as px


def load_config(file_path: str = "config.yaml") -> dict:
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def create_mapping_dict(mapping_dict_path:str):
    """Create a mapping dictionary from a json file"""
    with open(mapping_dict_path) as json_file:
        mapping_dict = json.load(json_file)
    flattened = [(col, orig, altered) for col in mapping_dict for orig, altered in mapping_dict[col].items()]
    
    mapping_dict = pd.DataFrame(flattened, columns=['column', 'original', 'altered'])
    #drop the column column
    mapping_dict = mapping_dict.drop(columns='column')
    return mapping_dict

mapping_dict = create_mapping_dict(r'data\mapping_dict.json')
config = load_config()
node_color_map = config["node_color_map"]

def get_original(mapping_dict: pd.DataFrame, input_str: str) -> str:
    #first we need to replac
    match = mapping_dict[mapping_dict['altered'] == input_str]['original']
    if not match.empty:
        return match.values[0]
    else:
        return input_str


def import_data(json_file: str) -> dict:
    try:
        with open(json_file) as f:
            data = json.load(f)
        
        #clean up the data, we want to replace the node_edited values with the original values
        #first replace spaces with underscores
        data['nodes'] = [{k: v.replace(' ', '_') if k == 'node_edited' else v for k, v in d.items()} for d in data['nodes']]
        #now use mapping dict to replace values
        data['nodes'] = [{k: get_original(mapping_dict, v) if k == 'node_edited' else v for k, v in d.items()} for d in data['nodes']]
        return data
    except FileNotFoundError:
        print(f"The file {json_file} was not found.")
        return None  # Or raise the error to halt execution with raise


def format_nodes(data: dict) -> pd.DataFrame:
    nodes = pd.DataFrame(data["nodes"])
    nodes["type"] = nodes["type"].str.replace("groip", "group")
    nodes["color"] = nodes["type"].map(node_color_map)
    nodes["Node"] = nodes.apply(
        lambda x: Node(
            id=x["id"], label=x["node_edited"], size=10, shape="dot", color=x["color"]
        ),
        axis=1,
    )
    #use mapping dict to replace values
   

    return nodes


def format_edges(data: dict) -> pd.DataFrame:
    edges = pd.DataFrame(data["edges"])
    edges["Edge"] = edges.apply(
        lambda x: Edge(
            source=x["source"], target=x["target"], label=x["relationship_type"]
        ),
        axis=1,
    )
    return edges


def import_and_format_data(
    json_file: str = r"D:\repos\anonymous_phenomena_timeline\data\graph_data.json",
) -> tuple:
    
    data = import_data(json_file)
    if data is None:
        raise FileNotFoundError(f"The file {json_file} was not found.")
    nodes = format_nodes(data)
    edges = format_edges(data)
    return nodes, edges


def aggregate_words(edges: pd.DataFrame) -> list:
    words = []
    for i in edges["source"]:
        words.append(i)
    for i in edges["target"]:
        words.append(i)
    #clean words
    words = [word.replace('_', ' ') for word in words]
    #now use mapping dict to replace values
    words = [get_original(mapping_dict, word) for word in words]
    return words


def make_word_count_bar_chart(edges: pd.DataFrame):
    words = aggregate_words(edges)
    word_counts = Counter(words)
    word_counts = dict(word_counts.most_common(20))
    word_counts = pd.DataFrame.from_dict(word_counts, orient="index").reset_index()
    word_counts.columns = ["word", "count"]
    fig = px.bar(word_counts, x="word", y="count")
    fig.update_layout(
        title="Most Common Nodes in the Timeline",
        xaxis_title="Word",
        yaxis_title="Count",
    )
    return fig


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(220, 100%%, %d%%)" % np.random.randint(50, 70)


def make_wordcloud(edges: pd.DataFrame) -> WordCloud:
    words = aggregate_words(edges)
    frequency_dict = dict(Counter(words))
    wordcloud = WordCloud(
        background_color="white",
        width=800,
        height=400,
        max_font_size=40,
        color_func=color_func,
    )
    wordcloud.generate_from_frequencies(frequency_dict, max_font_size=33)
    return wordcloud

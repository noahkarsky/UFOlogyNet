# The UFOlogyNet

This project aims to demystify the convoluted, cryptic, misleading, and often wacky world of the UAP (Unidentified Aerial Phenomena) phenomena by transforming it into a comprehensive knowledge graph. Our goal is to elucidate the complex relationships between various events, sightings, and key figures involved in UAP studies, making it significantly easier for researchers, enthusiasts, and the curious public to navigate and understand the field.

## Project Components

The UFOlogyNet is divided into two main components:
**Data Collection and Standardization**

The very first dataset I used for the project was the [Loose Threads Story](https://www.reddit.com/r/lexfridman/comments/11sgbxl/loose_threads_a_robust_thorough_and_well/). I used NLP methods to extract entities and build the initial graph which was then cleaned and expanded upon manually. I added to this over time with interesting relationships and people that I see when reading things. I then used the [UAP Timeline](https://pdfhost.io/v/gR8lAdgVd_Uap_Timeline_Prepared_By_Another) as a second dataset which I will fold into the main graph. This timeline was released directly following the July 26 Congressional hearings. I have been sub-par with adding extra notes and references, but will add to these in the future. The two datasets are called "Project Amanita Data" and "Phenomena Timeline Data" respectively.


## Tools used
- Babelscape/rebel-large
- Lots of GPT for entity extraction and cleaning
- Streamlit for visualization
- Networkx for graph manipulation
- Pandas for data manipulation
- gravis for graph visualization



My original project (now defunct) can be found [here](https://noahkarsky.github.io/project-amanita/).

# [Click here for UFOlogyNet Knowledge Graph Visualization](https://noahkarsky-anonymous-phenomena-timeline-app-s0ulm7.streamlit.app/)

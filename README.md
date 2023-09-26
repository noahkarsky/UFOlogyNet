# anonymous_phenomena_timeline
 Work conducted to clean up and analyse the anonymous ufo timeline that came out of the July 26 Congressional hearings on the phenomena

The method to generate the graph is as follows:

1. Use custom function in 1_parsing to get data from the markdown file
2. Use Babelscape/rebel-large to extract the entities from the text that we pulled from each event
3.Standardized the triplets and did some data cleaning to help with visualization
4. Then using vectors, we did some grouping and manual cleaning to add labels to all the points

Original PDF I believe is anonymous as far as I know. You can find a hosted PDF of it [HERE](https://pdfhost.io/v/gR8lAdgVd_Uap_Timeline_Prepared_By_Another)


I had originally used a python graph library to handle the visualization, but I like being able to control various aspects so I instead went with a streamlit implementation. 
Someday I will [fold it into my other knowledge graph](https://noahkarsky.github.io/project-amanita/) and create a unified visualization.

# [Anonymous UAP Timeline - Knowledge Graph](https://uap-timeline-knowledge-graph.streamlit.app/)

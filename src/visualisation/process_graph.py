import networkx as nx
import matplotlib.pyplot as plt

def build_process_graph(relationship_report):

    graph = nx.DiGraph()

    for _, row in relationship_report.iterrows():

        source = row["source"]
        target = row["target"]

        graph.add_edge(
            source,
            target
        )

    return graph

def draw_process_graph(graph):

    plt.figure(
        figsize=(12, 8)
    )

    nx.draw(
        graph,
        with_labels=True
    )

    plt.show()

def save_process_graph(
    graph,
    path
):

    plt.figure(
        figsize=(12, 8)
    )

    nx.draw(
        graph,
        with_labels=True
    )

    plt.savefig(path)

    plt.close()
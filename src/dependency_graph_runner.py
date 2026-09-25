from ml.dependency_discovery.dependency_graph import (
    DependencyGraph
)


def run_dependency_graph():

    graph = DependencyGraph(
        "reports/dependency_consensus.csv",
        min_votes=2
    )

    asset = "LIT101"

    print(
        "\nDEPENDENCY GRAPH"
    )

    print(
        "================"
    )

    print(
        graph.get_dependencies(asset)
    )

    print()

    print(
        graph.get_dependency_report(asset)
    )
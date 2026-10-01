from ml.soft_sensor.automatic_soft_sensor import (
    train_automatic_soft_sensor
)

from ml.dependency_discovery.dependency_graph import (
    DependencyGraph
)


def run_automatic_soft_sensor(df):

    graph = DependencyGraph(
        "reports/dependency_consensus.csv",
        min_votes=2
    )

    train_automatic_soft_sensor(
        df,
        "LIT101",
        graph
    )
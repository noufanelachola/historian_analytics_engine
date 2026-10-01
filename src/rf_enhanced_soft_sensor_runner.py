from ml.dependency_discovery.dependency_graph import (
    DependencyGraph
)

from ml.soft_sensor.enhanced_soft_sensor import (
    train_enhanced_soft_sensor
)


def run_rf_enhanced_soft_sensor(df):

    graph = DependencyGraph(
        "reports/dependency_consensus.csv",
        min_votes=2
    )

    train_enhanced_soft_sensor(
        df,
        "LIT101",
        graph
    )
from ml.dependency_discovery.weighted_dependency_graph import (
    WeightedDependencyGraph
)

from ml.soft_sensor.dependency_guided_xgb import (
    train_dependency_guided_xgb
)


def run_dependency_guided_xgb(df):

    graph = WeightedDependencyGraph(
        "reports/dependency_confidence.csv",
        min_confidence=0.1
    )

    train_dependency_guided_xgb(
        df,
        "LIT101",
        graph
    )
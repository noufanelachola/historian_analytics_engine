from ml.dependency_discovery.dependency_graph import (
    DependencyGraph
)

from ml.soft_sensor.feature_generator import (
    generate_temporal_features
)

from ml.soft_sensor.xgb_soft_sensor import (
    train_xgb_soft_sensor
)


def run_xgb_soft_sensor(df):

    graph = DependencyGraph(
        "reports/dependency_consensus.csv",
        min_votes=2
    )

    target = "LIT101"

    dependencies = graph.get_dependencies(
        target
    )

    print("\nDEPENDENCIES")
    print("============")
    print(dependencies)

    # Add target sensor for temporal features
    dependencies.append(target)

    df_temp = generate_temporal_features(
        df,
        dependencies
    )

    generated_features = []

    for feature in dependencies:

        # For target asset:
        # only use history, never current value
        if feature == target:

            generated_features.extend([
                f"{feature}_lag1",
                f"{feature}_lag5",
                f"{feature}_lag10",
                f"{feature}_avg10",
                f"{feature}_avg50"
            ])

        else:

            generated_features.extend([
                feature,
                f"{feature}_lag1",
                f"{feature}_lag5",
                f"{feature}_lag10",
                f"{feature}_avg10",
                f"{feature}_avg50"
            ])

    print("\nTOTAL FEATURES")
    print("==============")
    print(len(generated_features))

    train_xgb_soft_sensor(
        df_temp,
        target,
        generated_features
    )
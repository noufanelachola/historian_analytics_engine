import pandas as pd

from ml.dependency_discovery.consensus_dependency import (
    build_consensus_dependency
)


def run_consensus():
    print(
        pd.read_csv(
            "reports/dependency_same_stage.csv"
        ).columns
    )

    print(
        pd.read_csv(
            "reports/dependency_mi_same_stage.csv"
        ).columns
    )

    print(
        pd.read_csv(
            "reports/dependency_xgb_same_stage.csv"
        ).columns
    )

    

    rf = pd.read_csv(
        "reports/dependency_same_stage.csv"
    )

    mi = pd.read_csv(
        "reports/dependency_mi_same_stage.csv"
    )

    xgb = pd.read_csv(
        "reports/dependency_xgb_same_stage.csv"
    )

    report = build_consensus_dependency(
        rf,
        mi,
        xgb
    )

    report.to_csv(
        "reports/dependency_consensus.csv",
        index=False
    )

    print("\nCONSENSUS DEPENDENCY")
    print("====================")

    print(report.head(20))
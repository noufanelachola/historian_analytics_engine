import pandas as pd

from asset_classifier import classify_asset


def build_stage_relationships(
    relationship_report
):

    stage_relationships = []

    for _, row in relationship_report.iterrows():

        source = row["source"]
        target = row["target"]

        source_info = classify_asset(
            source
        )

        target_info = classify_asset(
            target
        )

        stage_relationships.append({
            "source": source,
            "source_stage":
                source_info["asset_stage"],

            "target": target,
            "target_stage":
                target_info["asset_stage"],

            "score": row["score"]
        })

    report = pd.DataFrame(
        stage_relationships
    )

    return report
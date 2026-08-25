import pandas as pd
from asset_classifier import classify_asset

def get_transition_rows(df, asset):

    states = df[asset]

    previous_states = states.shift(1)

    transitions = states != previous_states

    transition_rows = df.index[
        transitions
    ].tolist()

    return transition_rows


def count_responses(df, source_asset, target_asset, window=5):

    transition_rows = get_transition_rows(df, source_asset)

    if len(transition_rows) == 0:
        return {
            "responses": 0,
            "confidence": 0
        }

    responses = 0

    for row in transition_rows:

        if row + window >= len(df):
            continue

        before = df.iloc[row][target_asset]

        after = df.iloc[
            row + window
        ][target_asset]

        if before != after:
            responses += 1

    confidence = (responses / len(transition_rows)) * 100

    return {
        "responses": responses,
        "confidence": confidence
    }


def discover_confidence_relationships(df, source_asset, assets, window=5):

    relationships = []

    for asset in assets:

        if asset == source_asset:
            continue

        result = count_responses(df, source_asset, asset, window)

        relationships.append({
            "source": source_asset,
            "target": asset,
            "responses": result["responses"],
            "confidence": result["confidence"]
        })

    report = pd.DataFrame(relationships)

    report = report.sort_values(
        by="confidence",
        ascending=False
    )

    return report


def get_assets_in_same_stage(source_asset, assets, max_stage_difference=1):
    source_info = classify_asset(source_asset)

    source_stage = source_info[
        "asset_stage"
    ]

    related_assets = []

    for asset in assets:

        if asset == source_asset:
            continue

        asset_info = classify_asset(
            asset
        )

        asset_stage = asset_info[
            "asset_stage"
        ]

        stage_difference = abs(
            asset_stage - source_stage
        )

        if stage_difference <= max_stage_difference:
            related_assets.append(
                asset
            )

    return related_assets
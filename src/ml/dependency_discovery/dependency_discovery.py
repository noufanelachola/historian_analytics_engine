import pandas as pd

from ml.dependency_discovery.dependency_models import train_random_forest
from core.asset_classifier import classify_asset


def get_assets_in_same_stage(assets, target_asset):
    target_stage = classify_asset(target_asset)["asset_stage"]

    candidates = []

    for asset in assets:

        stage = classify_asset(asset)["asset_stage"]

        if stage == target_stage:
            candidates.append(asset)

    return candidates

def get_assets_in_adjacent_stages(assets, target_asset):
    target_stage = classify_asset(target_asset)["asset_stage"]

    candidates = []

    for asset in assets:

        stage = classify_asset(asset)["asset_stage"]

        if abs(stage - target_stage) <= 1:
            candidates.append(asset)

    return candidates


def prepare_dependency_dataset(df, target_asset, candidate_assets):
    columns = candidate_assets + [target_asset]

    dataset = df[columns].copy()

    dataset = dataset.select_dtypes(
        include=["number"]
    )

    dataset = dataset.dropna()

    X = dataset.drop(columns=[target_asset])

    y = dataset[target_asset]

    return X, y


def extract_feature_importance(model, X, target_asset):
    report = pd.DataFrame({
        "target": target_asset,
        "dependency": X.columns,
        "importance": model.feature_importances_
    })

    report = report.sort_values(by="importance", ascending=False)
    return report


def discover_dependencies(df, target_asset,candidate_assets, top_n=10):

    sample_df = df.sample(
        n=100000,
        random_state=42
    )

    X, y = prepare_dependency_dataset(
        sample_df,
        target_asset,
        candidate_assets
    )

    # X, y = prepare_dependency_dataset(
    #     df,
    #     target_asset
    # )

    model = train_random_forest(X, y)

    report = extract_feature_importance(model, X, target_asset)

    return report.head(top_n)

def get_analog_assets(asset_profiles):
    analog_assets = []

    for profile in asset_profiles:

        if profile["category"] == "Analog":
            analog_assets.append(profile["asset"])
    
    return analog_assets
from ml.dependency_discovery.xgboost_dependency import (
    discover_dependencies_xgboost
)

from ml.dependency_discovery.dependency_discovery import (
    get_assets_in_same_stage,
    get_assets_in_adjacent_stages
)

from core.asset_profiler import profile_asset

import pandas as pd


def get_candidate_assets(
    assets,
    target_asset,
    strategy
):

    if strategy == "same_stage":

        candidates = get_assets_in_same_stage(
            assets,
            target_asset
        )

    elif strategy == "adjacent_stage":

        candidates = get_assets_in_adjacent_stages(
            assets,
            target_asset
        )

    elif strategy == "entire_plant":

        candidates = assets.copy()

    else:

        raise ValueError(
            "Unknown strategy"
        )

    if target_asset in candidates:
        candidates.remove(target_asset)

    return candidates


def run_xgboost_strategy(
    df,
    assets,
    strategy
):

    all_reports = []

    for asset in assets:

        profile = profile_asset(
            df,
            asset
        )

        if profile["category"] != "Analog":
            continue

        print(
            f"Analyzing {asset}..."
        )

        candidates = get_candidate_assets(
            assets,
            asset,
            strategy
        )

        report = discover_dependencies_xgboost(
            df,
            asset,
            candidates
        )

        report["strategy"] = strategy

        if not report.empty:
            all_reports.append(
                report.head(5)
            )

    final_report = pd.concat(
        all_reports,
        ignore_index=True
    )

    return final_report


def run_dependency_discovery_xgboost(
    df,
    assets
):

    print()
    print("XGBOOST DEPENDENCY DISCOVERY")
    print("============================")

    print()
    print("CASE 1 : SAME STAGE")
    print("===================")

    same_stage = run_xgboost_strategy(
        df,
        assets,
        "same_stage"
    )

    same_stage.to_csv(
        "./reports/dependency_xgb_same_stage.csv",
        index=False
    )

    print()
    print("CASE 2 : ADJACENT STAGE")
    print("=======================")

    adjacent_stage = run_xgboost_strategy(
        df,
        assets,
        "adjacent_stage"
    )

    adjacent_stage.to_csv(
        "./reports/dependency_xgb_adjacent_stage.csv",
        index=False
    )

    print()
    print("CASE 3 : ENTIRE PLANT")
    print("=====================")

    entire_plant = run_xgboost_strategy(
        df,
        assets,
        "entire_plant"
    )

    entire_plant.to_csv(
        "./reports/dependency_xgb_entire_plant.csv",
        index=False
    )

    print()
    print("XGBoost reports saved.")

    return (
        same_stage,
        adjacent_stage,
        entire_plant
    )
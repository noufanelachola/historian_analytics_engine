from ml.dependency_discovery.correlation_dependency import (
    discover_dependencies_correlation
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


def run_correlation_strategy(
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

        for candidate in candidates:
            if df[candidate].nunique() <= 1:
                print(f"Skipping constant asset: {candidate}")

        for candidate in candidates:
            if df[candidate].nunique() <= 1:
                print(f"Skipping constant asset: {candidate}")

        report = discover_dependencies_correlation(
            df,
            asset,
            candidates
        )

        report["strategy"] = strategy

        all_reports.append(
            report
        )

    final_report = pd.concat(
        all_reports,
        ignore_index=True
    )

    return final_report


def run_dependency_discovery_correlation(
    df,
    assets
):

    print()
    print("CORRELATION DEPENDENCY DISCOVERY")
    print("================================")

    # SAME STAGE

    print()
    print("CASE 1 : SAME STAGE")
    print("===================")

    same_stage_report = run_correlation_strategy(
        df,
        assets,
        "same_stage"
    )

    same_stage_report.to_csv(
        "./reports/dependency_corr_same_stage.csv",
        index=False
    )

    print(
        "Saved dependency_corr_same_stage.csv"
    )

    # ADJACENT STAGE

    print()
    print("CASE 2 : ADJACENT STAGE")
    print("=======================")

    adjacent_report = run_correlation_strategy(
        df,
        assets,
        "adjacent_stage"
    )

    adjacent_report.to_csv(
        "./reports/dependency_corr_adjacent_stage.csv",
        index=False
    )

    print(
        "Saved dependency_corr_adjacent_stage.csv"
    )

    # ENTIRE PLANT

    print()
    print("CASE 3 : ENTIRE PLANT")
    print("=====================")

    entire_plant_report = run_correlation_strategy(
        df,
        assets,
        "entire_plant"
    )

    entire_plant_report.to_csv(
        "./reports/dependency_corr_entire_plant.csv",
        index=False
    )

    print(
        "Saved dependency_corr_entire_plant.csv"
    )

    return (
        same_stage_report,
        adjacent_report,
        entire_plant_report
    )
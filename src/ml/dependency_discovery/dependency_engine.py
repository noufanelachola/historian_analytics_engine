import pandas as pd

from ml.dependency_discovery.dependency_discovery import (
    discover_dependencies,
    get_assets_in_same_stage,
    get_assets_in_adjacent_stages
)

from core.asset_profiler import profile_asset


def get_candidate_assets(assets, target_asset, strategy):

    if strategy == "same_stage":
        candidates = get_assets_in_same_stage( assets, target_asset)
    elif strategy == "adjacent_stage":
        candidates = get_assets_in_adjacent_stages(assets, target_asset)
    elif strategy == "entire_plant":
        candidates = assets.copy()
    else:
        raise ValueError(
            "Unknown strategy"
        )

    if target_asset in candidates:
        candidates.remove(target_asset)

    return candidates


def build_dependency_knowledge(df, assets, strategy="same_stage"):
    reports = []

    for asset in assets:

        profile = profile_asset(df, asset)

        if profile["category"] != "Analog":
            continue

        print(f"Analyzing {asset}")

        candidates = get_candidate_assets(assets, asset, strategy)

        report = discover_dependencies(df, asset, candidates)

        report["strategy"] = strategy

        reports.append(report)

    final_report = pd.concat(
        reports,
        ignore_index=True
    )

    return final_report
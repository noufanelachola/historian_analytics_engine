from asset_classifier import classify_asset
from asset_profiler import profile_asset


def get_related_assets(
    relationship_report,
    asset,
    top_n=3
):
    related = relationship_report[
        relationship_report["source"] == asset
    ]

    return related.head(top_n)[
        "target"
    ].tolist()


def build_asset_intelligence(
    df,
    asset,
    relationship_report,
    threshold_report
):
    asset_info = classify_asset(asset)

    profile_info = profile_asset(
        df,
        asset
    )

    threshold_info = get_threshold_knowledge(threshold_report, asset)

    related_assets = get_related_assets(
        relationship_report,
        asset
    )

    return {
        "asset": asset,
        "asset_type": asset_info["asset_type"],
        "asset_stage": asset_info["asset_stage"],
        **profile_info,
        **threshold_info,
        "related_assets": related_assets
    }


def build_plant_intelligence(df, assets, relationship_report,threshold_report):
    reports = []

    for asset in assets:
        report = build_asset_intelligence(df, asset, relationship_report, threshold_report)
        reports.append(report)

    return reports

def get_threshold_knowledge(threshold_report, asset):

    row = threshold_report[
        threshold_report["Actuator"] == asset
    ]

    if row.empty:
        return {
            "start_threshold": None,
            "stop_threshold": None,
            "process_variable": None
        }

    row = row.iloc[0]

    return {
        "process_variable":
            row["Process Variable"],

        "start_threshold":
            row["Fall Median"],

        "stop_threshold":
            row["Rise Median"]
    }
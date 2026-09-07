from ml.dependency_discovery.mutual_information import discover_dependencies_mi
from ml.dependency_discovery.dependency_discovery import get_assets_in_same_stage
from core.asset_profiler import profile_asset
import pandas as pd

def run_dependency_discovery_mi(df, assets):
    print()
    print("MUTUAL INFORMATION")
    print("==================")

    all_reports = []

    for asset in assets:
        profile = profile_asset(df,asset)

        if profile["category"] != "Analog":
            continue

        print(f"Analyzing {asset}...")

        candidates = get_assets_in_same_stage(assets,asset)

        if asset in candidates:
            candidates.remove(asset)

        report = discover_dependencies_mi(df,asset,candidates)

        all_reports.append(report.head(5))

    final_report = pd.concat(all_reports,ignore_index=True)

    final_report.to_csv("./reports/dependency_mi_same_stage.csv",index=False)

    print()
    print("MI Report Saved")

    return final_report
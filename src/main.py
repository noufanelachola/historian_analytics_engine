from core.load_dataset import load_dataset
from core.asset_inventory import get_assets

from ml.dependency_discovery.dependency_discovery import (
    discover_dependencies,
    get_assets_in_same_stage,
    get_assets_in_adjacent_stages
)



## Initial Settings ... ##

print("Loading dataset...")
df = load_dataset("./data/swat_normal.csv")

print()
assets = get_assets(df)

print(f"Total Assets: {len(assets)}")
print()


### 1. Dependency Discovery ###

target_asset = "LIT101"

print()
print("DEPENDENCY DISCOVERY")
print("====================")


#__ Case 1: Entire Plant __#

all_assets = assets.copy()
all_assets.remove(target_asset)

print("\nCASE 1 : ENTIRE PLANT")
print("=====================")

report_all = discover_dependencies(
    df,
    target_asset,
    all_assets
)

print(report_all)

report_all.to_csv(
    "./reports/lit101_all_assets.csv",
    index=False
)

print()
print("Reports saved.")
print("Done.")


#__ Case 2: SAME STAGE __#

same_stage_assets = get_assets_in_same_stage(assets, target_asset)
same_stage_assets.remove(target_asset)

print("\nCASE 2 : SAME STAGE")
print("===================")

report_same = discover_dependencies(df, target_asset, same_stage_assets)
print(report_same.head(10))

report_same.to_csv(
    "./reports/lit101_same_stage.csv",
    index=False
)

print()
print("Reports saved.")
print("Done.")


#__ Case 3: ADJACENT STAGE __#

adjacent_assets = get_assets_in_adjacent_stages(assets, target_asset)

adjacent_assets.remove(target_asset)

print("\nCASE 3 : ADJACENT STAGES")
print("========================")

report_adjacent = discover_dependencies(df, target_asset, adjacent_assets)

print(report_adjacent)

report_adjacent.to_csv(
    "./reports/lit101_adjacent_stages.csv",
    index=False
)

print()
print("Reports saved.")
print("Done.")
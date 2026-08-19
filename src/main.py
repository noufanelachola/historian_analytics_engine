from load_dataset import load_dataset
from asset_inventory import *
from asset_classifier import classify_asset, save_asset_classification
from asset_profiler import profile_assets
from threshold_discovery import *

df = load_dataset("./data/swat.csv")
assets = get_assets(df)

# save_inventory(assets, "./reports/asset_inventory.csv")

# print(df.head())
# print(assets)
# print(f"Total Assets: {len(assets)}")

# generate_summary(assets)

# print("\n ")

# asset_info_list = []
# for asset in assets:
#     info = classify_asset(asset)
#     asset_info_list.append(info)

# save_asset_classification(asset_info_list, "./reports/asset_classification.csv")

# print(f"Assets : {assets}")

# for asset in assets:

#     if df[asset].nunique() > 5:
#         continue    
#     print(f"\nAsset: {asset}")

#     print("\nUnique Values:")
#     print(df[asset].nunique())

#     print("-" * 50) 

# print(profile_assets(df, assets))

print("======================")
print("\nP101 STATE TRANSITIONS")

transitions = find_transition_conditions(
    df,
    "P101",
    "LIT101"
)

print(transitions.head())

print("======================")
print("\nSplitt")

rise, fall = split_transitions(transitions)
rise_levels = rise["LIT101"]
fall_levels = fall["LIT101"]

print("\nRise Transitions")
print(rise)
rise_stats = estimate_threshold(rise_levels)

print()
print(rise_stats)

print("\nFall Transitions")
print(fall)
fall_stats = estimate_threshold(fall_levels)
print()
print(fall_stats)



print("\nCount")
report = discover_threshold(
    df,
    "P101",
    "LIT101"
)
report.to_csv("./reports/threshold_report.csv", index=False)

print(report)
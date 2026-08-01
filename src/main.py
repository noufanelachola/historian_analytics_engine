from load_dataset import load_dataset
from asset_inventory import *
from asset_classifier import classify_asset, save_asset_classification
from asset_profiler import profile_asset

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

print(profile_asset(df, "P101"))
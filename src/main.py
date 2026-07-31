from load_dataset import load_dataset
from asset_inventory import *
from asset_classifier import classify_asset

df = load_dataset("./data/swat.csv")
assets = get_assets(df)
save_inventory(assets, "./reports/asset_inventory.csv")

print(df.head())
print(assets)
print(f"Total Assets: {len(assets)}")

generate_summary(assets)

print("\n ")
print(classify_asset("FIT101"))
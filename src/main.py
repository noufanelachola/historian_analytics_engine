from load_dataset import load_dataset
from asset_inventory import *

df = load_dataset("./data/swat.csv")
assets = get_assets(df)
save_inventory(assets, "./reports/asset_inventory.csv")

print(df.head())
print(assets)
print(f"Total Assets: {len(assets)}")

generate_summary(assets)
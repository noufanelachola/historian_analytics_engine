import pandas as pd

def get_assets(data):
    print(data.columns)
    assets = list(data.columns)

    # Since the Timestamp column is not an asset, we remove it from the list of assets
    if "Timestamp" in assets:
        assets.remove("Timestamp")
    
    # Since the Normal/Attack column is not an asset, we remove it from the list of assets.
    if "Normal/Attack" in assets:
        assets.remove("Normal/Attack")
    
    return assets

def save_inventory(assets, path):
    inventory = pd.DataFrame({
        "S.no": range(1, len(assets) + 1),
        "Asset": assets
    })

    inventory.to_csv(path, index=False)

def generate_summary(assets):

    print("\nASSET INVENTORY")
    print("====================")

    print(f"Total Assets: {len(assets)}")

    print("\nAssets:")

    for asset in assets:
        print(asset,end="\t")
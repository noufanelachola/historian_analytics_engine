from core.load_dataset import load_dataset
from core.asset_inventory import get_assets

from dependency_runner import *
from dependency_runner_mi import *


## Initial Settings ... ##

print("Loading dataset...")
df = load_dataset("./data/swat_normal.csv")

print()
assets = get_assets(df)

print(f"Total Assets: {len(assets)}")
print()


### 1.1 Dependency Discovery ###
# run_dependency_discovery(df, assets)  

### 1.2 Dependency Discovery Mutual Information ###
run_dependency_discovery_mi(df, assets)
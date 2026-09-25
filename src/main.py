from core.load_dataset import load_dataset
from core.asset_inventory import get_assets

from dependency_runner import *
from dependency_runner_mi import *
from correlation_runner import *
from xgboost_runner import *

from consensus_runner import run_consensus
from dependency_graph_runner import run_dependency_graph



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
# run_dependency_discovery_mi(df, assets)

### 1.3 Dependency Discovery Correlation ###
# run_dependency_discovery_correlation(df, assets)

### 1.3 Dependency Discovery Correlation ###
# run_dependency_discovery_xgboost(df,assets)

# run_consensus()

run_dependency_graph()
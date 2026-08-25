import time
import pandas as pd

from load_dataset import load_dataset

from asset_inventory import get_assets
from asset_classifier import is_actuator

from threshold_discovery import discover_threshold

from relationship_discovery import (
    calculate_correlations,
    save_correlation_matrix,
    discover_relationships
)

from process_graph import (
    build_process_graph,
    save_process_graph
)

from historian_intelligence import *

from relationship_confidence import *

# ==================================
# LOAD DATASET
# ==================================

print("Loading dataset...")

df = load_dataset("./data/swat_normal.csv")

assets = get_assets(df)

print(f"\nTotal Assets: {len(assets)}")

# ==================================
# FIND ACTUATORS
# ==================================

actuators = [
    asset
    for asset in assets
    if is_actuator(asset)
]

print("\nACTUATORS")
print("==========")

for actuator in actuators:
    print(actuator)

# ==================================
# THRESHOLD DISCOVERY
# ==================================

print("\nGenerating Threshold Report...")

threshold_report = discover_threshold(
    df,
    "P101",
    "LIT101"
)

threshold_report.to_csv(
    "./reports/threshold_report.csv",
    index=False
)

# ==================================
# CORRELATION ANALYSIS
# ==================================

print("\nGenerating Correlation Matrix...")

correlation_matrix = calculate_correlations(df)

save_correlation_matrix(
    correlation_matrix,
    "./reports/correlation_matrix.csv"
)

# ==================================
# RELATIONSHIP DISCOVERY
# ==================================

print("\nDiscovering Relationships...")

start_time = time.time()

all_relationships = []

# Only analyze first 3 actuators for now
for actuator in actuators[:3]:

    print(f"\nAnalyzing {actuator}...")

    report = discover_relationships(
        df,
        actuator,
        assets
    )

    # Keep only top 3 relationships
    top_report = report.head(3)

    all_relationships.append(
        top_report
    )

master_report = pd.concat(
    all_relationships,
    ignore_index=True
)

master_report.to_csv(
    "./reports/master_relationship_report.csv",
    index=False
)

print("\nGenerating Historian Intelligence Report...")

plant_intelligence = build_plant_intelligence(
    df,
    assets,
    master_report,
    threshold_report
)

pd.DataFrame(
    plant_intelligence
).to_csv(
    "./reports/historian_intelligence_report.csv",
    index=False
)

print("\nHistorian Intelligence Report Saved.")

print("\nMASTER REPORT")
print("=============")

print(master_report)

end_time = time.time()

print(
    f"\nRelationship Discovery Time: "
    f"{end_time - start_time:.2f} seconds"
)



plant_intelligence = (
    build_plant_intelligence(
        df,
        assets,
        master_report,
        threshold_report
    )
)

print ("Plant intellignece")
print(plant_intelligence)

# ==================================
# PROCESS GRAPH
# ==================================

print("\nGenerating Process Graph...")

graph = build_process_graph(
    master_report
)

save_process_graph(
    graph,
    "./reports/process_graph.png"
)

print("\nProcess graph saved.")

print("\nDone.")

print("\nCONFIDENCE RELATIONSHIPS")
print("========================")

candidate_assets = get_assets_in_same_stage(
    "P101",
    assets
)

confidence_report = discover_confidence_relationships(
    df,
    "P101",
    candidate_assets
)

print(candidate_assets)
print(f"Total Candidates: {len(candidate_assets)}")

print(
    confidence_report.head(20)
)

confidence_report.to_csv(
    "./reports/p101_confidence_report.csv",
    index=False
)
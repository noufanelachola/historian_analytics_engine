from ml.dependency_discovery.dependency_engine import build_dependency_knowledge

def run_dependency_discovery(df, assets):

    print()
    print("DEPENDENCY DISCOVERY")
    print("====================")

    # SAME STAGE

    same_stage_report = build_dependency_knowledge(df, assets, strategy="same_stage")

    same_stage_report.to_csv(
        "./reports/dependency_same_stage.csv",
        index=False
    )

    print("✓ Same Stage Complete")

    # ADJACENT STAGE

    adjacent_report = build_dependency_knowledge(df, assets, strategy="adjacent_stage")

    adjacent_report.to_csv(
        "./reports/dependency_adjacent_stage.csv",
        index=False
    )

    print("✓ Adjacent Stage Complete")

    # ENTIRE PLANT

    entire_plant_report = build_dependency_knowledge(df, assets, strategy="entire_plant")

    entire_plant_report.to_csv(
        "./reports/dependency_entire_plant.csv",
        index=False
    )

    print("✓ Entire Plant Complete")

    return (
        same_stage_report,
        adjacent_report,
        entire_plant_report
    )


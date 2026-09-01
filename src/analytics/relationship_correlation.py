import pandas as pd


def calculate_asset_correlation(
    df,
    source_asset,
    target_asset
):
    correlation = df[
        source_asset
    ].corr(
        df[target_asset]
    )

    return correlation


def discover_correlation_relationships(
    df,
    source_asset,
    assets
):
    relationships = []

    for asset in assets:

        if asset == source_asset:
            continue

        correlation = calculate_asset_correlation(
            df,
            source_asset,
            asset
        )

        relationships.append({
            "source": source_asset,
            "target": asset,
            "correlation": correlation
        })

    report = pd.DataFrame(
        relationships
    )

    report["abs_correlation"] = (
        report["correlation"].abs()
    )

    report = report.sort_values(
        by="abs_correlation",
        ascending=False
    )

    return report
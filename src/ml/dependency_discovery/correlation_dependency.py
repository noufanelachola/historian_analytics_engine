import pandas as pd
import numpy as np


import pandas as pd
import numpy as np


def discover_dependencies_correlation(
    df,
    target_asset,
    candidate_assets,
    top_n=10
):

    relationships = []

    target_series = df[target_asset]

    # Skip constant target
    if target_series.nunique() <= 1:
        return pd.DataFrame()

    for asset in candidate_assets:

        series = df[asset]

        # Skip constant signals
        if series.nunique() <= 1:
            continue

        # Skip if standard deviation is zero
        if series.std() == 0:
            continue

        if target_series.std() == 0:
            continue

        try:

            correlation = target_series.corr(
                series
            )

            if np.isnan(correlation):
                continue

            relationships.append({
                "target": target_asset,
                "dependency": asset,
                "correlation": correlation,
                "abs_correlation": abs(correlation)
            })

        except Exception:

            continue

    report = pd.DataFrame(
        relationships
    )

    if report.empty:
        return report

    report = report.sort_values(
        by="abs_correlation",
        ascending=False
    )

    return report.head(top_n)
import pandas as pd

from xgboost import XGBRegressor


def discover_dependencies_xgboost(
    df,
    target_asset,
    candidate_assets,
    top_n=10
):

    X = df[candidate_assets]

    y = df[target_asset]

    # Combine and remove rows containing NaN
    data = pd.concat(
        [X, y],
        axis=1
    )

    original_rows = len(data)

    data = data.dropna()

    print(
        f"{target_asset}: "
        f"{original_rows} -> {len(data)} rows"
    )

    if len(data) == 0:
        return pd.DataFrame()

    # Remove constant features
    valid_candidates = []

    for asset in candidate_assets:

        if asset not in data.columns:
            continue

        if data[asset].nunique() > 1:
            valid_candidates.append(asset)

    if len(valid_candidates) == 0:
        return pd.DataFrame()

    X = data[valid_candidates]

    y = data[target_asset]

    # Skip constant targets
    if y.nunique() <= 1:
        return pd.DataFrame()

    model = XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X, y)

    report = pd.DataFrame({
        "target": target_asset,
        "dependency": valid_candidates,
        "importance": model.feature_importances_
    })

    report = report.sort_values(
        by="importance",
        ascending=False
    )

    return report.head(top_n)
import pandas as pd
from sklearn.feature_selection import mutual_info_regression

def discover_dependencies_mi(df, target_asset, candidate_assets, top_n=10):
    X = df[candidate_assets]
    y = df[target_asset]

    data = pd.concat([X, y],axis=1)

    data = data.dropna()

    X = data[candidate_assets]
    y = data[target_asset]

    scores = mutual_info_regression(X, y, random_state=42)

    report = pd.DataFrame({
        "target": target_asset,
        "dependency": candidate_assets,
        "mi_score": scores
    })

    report = report.sort_values(
        by="mi_score",
        ascending=False
    )

    return report.head(top_n)
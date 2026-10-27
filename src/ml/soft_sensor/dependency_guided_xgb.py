import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor

from ml.soft_sensor.feature_generator import (
    generate_temporal_features
)


def train_dependency_guided_xgb(
    df,
    target_asset,
    graph
):

    deps = graph.get_dependencies(
        target_asset
    )

    print("\nDEPENDENCIES")
    print("============")
    print(deps)

    assets = [
        dep for dep, weight in deps
    ]

    assets.append(target_asset)

    df_temp = generate_temporal_features(
        df,
        assets
    )

    generated_features = []

    feature_weights = {}

    for dep, weight in deps:

        cols = [
            dep,
            f"{dep}_lag1",
            f"{dep}_lag5",
            f"{dep}_lag10",
            f"{dep}_avg10",
            f"{dep}_avg50"
        ]

        generated_features.extend(cols)

        for c in cols:
            feature_weights[c] = weight

    target_history = [
        f"{target_asset}_lag1",
        f"{target_asset}_lag5",
        f"{target_asset}_lag10",
        f"{target_asset}_avg10",
        f"{target_asset}_avg50"
    ]

    generated_features.extend(
        target_history
    )

    for c in target_history:
        feature_weights[c] = 1.0

    data = df_temp[
        generated_features +
        [target_asset]
    ].dropna()

    X = data[generated_features].copy()

    # Apply confidence weights

    for col in generated_features:

        X[col] = (
            X[col] *
            feature_weights[col]
        )

    y = data[target_asset]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    print("\nDEPENDENCY GUIDED XGB")
    print("=====================")

    print("MAE :", mae)
    print("RMSE:", rmse)
    print("R²  :", r2)

    importance = pd.DataFrame({
        "feature": generated_features,
        "importance": model.feature_importances_
    })

    importance = importance.sort_values(
        by="importance",
        ascending=False
    )

    print("\nFEATURE IMPORTANCE")
    print("==================")
    print(importance.head(25))

    return model
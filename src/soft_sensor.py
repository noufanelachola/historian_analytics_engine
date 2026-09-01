import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from feature_engineering import create_temporal_features


def prepare_soft_sensor_data(df):

    data = df[
        [
            "FIT101",
            "MV101",
            "P101",
            "LIT101"
        ]
    ].copy()

    # Previous level values
    data["LIT101_lag1"] = data["LIT101"].shift(1)
    data["LIT101_lag5"] = data["LIT101"].shift(5)
    data["LIT101_lag10"] = data["LIT101"].shift(10)

    # Previous flow values
    data["FIT101_lag1"] = data["FIT101"].shift(1)
    data["FIT101_lag5"] = data["FIT101"].shift(5)

    # Remove rows where lagging produced NaN
    data = data.dropna()

    return data


from feature_engineering import create_temporal_features

import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def train_virtual_sensor(df):

    # ----------------------------------
    # FEATURE ENGINEERING
    # ----------------------------------

    df = create_temporal_features(df)

    # ----------------------------------
    # FEATURES
    # ----------------------------------

    features = [

        # Current values

        "FIT101",
        "MV101",
        "P101",

        "FIT201",
        "MV201",
        "P203",

        # Historical values

        "FIT101_lag1",
        "FIT101_lag5",
        "FIT101_lag10",

        "FIT201_lag1",
        "FIT201_lag5",
        "FIT201_lag10",

        # Rolling averages

        "FIT101_avg10",
        "FIT101_avg50",

        "FIT201_avg10",
        "FIT201_avg50"
    ]

    target = "LIT101"

    # ----------------------------------
    # DATASET
    # ----------------------------------

    data = df[
        features + [target]
    ].dropna()

    X = data[features]
    y = data[target]

    # ----------------------------------
    # CHRONOLOGICAL SPLIT
    # ----------------------------------

    split_index = int(
        len(data) * 0.8
    )

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    print(
        f"Training samples: {len(X_train)}"
    )

    print(
        f"Testing samples : {len(X_test)}"
    )

    # ----------------------------------
    # MODEL
    # ----------------------------------

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    print(
        "\nTraining Virtual Sensor..."
    )

    model.fit(
        X_train,
        y_train
    )

    # ----------------------------------
    # PREDICTIONS
    # ----------------------------------

    predictions = model.predict(
        X_test
    )

    # ----------------------------------
    # METRICS
    # ----------------------------------

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

    # ----------------------------------
    # FEATURE IMPORTANCE
    # ----------------------------------

    importance_report = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_
    })

    importance_report = importance_report.sort_values(
        by="importance",
        ascending=False
    )

    # ----------------------------------
    # PREDICTION REPORT
    # ----------------------------------

    prediction_report = pd.DataFrame({
        "actual": y_test.values,
        "predicted": predictions
    })

    return {
        "model": model,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "feature_importance": importance_report,
        "predictions": prediction_report
    }
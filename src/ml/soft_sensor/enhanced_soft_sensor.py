import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.ensemble import RandomForestRegressor

from ml.soft_sensor.feature_generator import (
    generate_temporal_features
)


def train_enhanced_soft_sensor(
    df,
    target_asset,
    dependency_graph
):

    features = dependency_graph.get_dependencies(
        target_asset
    )

    print("\nTARGET")
    print("======")
    print(target_asset)

    print("\nDEPENDENCIES")
    print("============")
    print(features)

    # Add target for temporal history
    features.append(target_asset)

    df_temp = generate_temporal_features(
        df,
        features
    )

    generated_features = []

    for feature in features:

        if feature == target_asset:

            generated_features.extend([
                f"{feature}_lag1",
                f"{feature}_lag5",
                f"{feature}_lag10",
                f"{feature}_avg10",
                f"{feature}_avg50"
            ])

        else:

            generated_features.extend([
                feature,
                f"{feature}_lag1",
                f"{feature}_lag5",
                f"{feature}_lag10",
                f"{feature}_avg10",
                f"{feature}_avg50"
            ])

    print("\nTOTAL FEATURES")
    print("==============")
    print(len(generated_features))

    data = df_temp[
        generated_features +
        [target_asset]
    ].dropna()

    X = data[generated_features]
    y = data[target_asset]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
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

    print("\nPERFORMANCE")
    print("===========")

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
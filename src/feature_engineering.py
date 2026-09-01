import pandas as pd


def create_temporal_features(df):

    engineered = df.copy()

    # -------------------------
    # FIT101 History
    # -------------------------

    engineered["FIT101_lag1"] = (
        engineered["FIT101"].shift(1)
    )

    engineered["FIT101_lag5"] = (
        engineered["FIT101"].shift(5)
    )

    engineered["FIT101_lag10"] = (
        engineered["FIT101"].shift(10)
    )

    # -------------------------
    # FIT201 History
    # -------------------------

    engineered["FIT201_lag1"] = (
        engineered["FIT201"].shift(1)
    )

    engineered["FIT201_lag5"] = (
        engineered["FIT201"].shift(5)
    )

    engineered["FIT201_lag10"] = (
        engineered["FIT201"].shift(10)
    )

    # -------------------------
    # Rolling Means
    # -------------------------

    engineered["FIT101_avg10"] = (
        engineered["FIT101"]
        .rolling(10)
        .mean()
    )

    engineered["FIT101_avg50"] = (
        engineered["FIT101"]
        .rolling(50)
        .mean()
    )

    engineered["FIT201_avg10"] = (
        engineered["FIT201"]
        .rolling(10)
        .mean()
    )

    engineered["FIT201_avg50"] = (
        engineered["FIT201"]
        .rolling(50)
        .mean()
    )

    return engineered.dropna()
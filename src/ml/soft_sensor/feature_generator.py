import pandas as pd


def generate_temporal_features(
    df,
    features
):

    df = df.copy()

    for feature in features:

        # Lag Features

        df[f"{feature}_lag1"] = df[
            feature
        ].shift(1)

        df[f"{feature}_lag5"] = df[
            feature
        ].shift(5)

        df[f"{feature}_lag10"] = df[
            feature
        ].shift(10)

        # Moving Averages

        df[f"{feature}_avg10"] = df[
            feature
        ].rolling(10).mean()

        df[f"{feature}_avg50"] = df[
            feature
        ].rolling(50).mean()

    return df
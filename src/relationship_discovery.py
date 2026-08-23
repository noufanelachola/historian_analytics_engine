import pandas as pd


def calculate_correlations(df):

    correlation_matrix = df.corr(numeric_only=True)

    return correlation_matrix


def find_related_assets(df, asset, threshold=0.5):

    correlation_matrix = calculate_correlations(df)

    correlations = correlation_matrix[asset]

    related_assets = correlations[
        abs(correlations) > threshold
    ]

    return related_assets.sort_values(
        ascending=False
    )


def save_correlation_matrix(correlation_matrix, path):

    correlation_matrix.to_csv(path)


def generate_relationship_report(df, asset, threshold=0.5):

    related_assets = find_related_assets(
        df,
        asset,
        threshold
    )

    report = pd.DataFrame({
        "Related Asset": related_assets.index,
        "Correlation": related_assets.values
    })

    return report
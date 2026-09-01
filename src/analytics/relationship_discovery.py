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

def get_transition_rows(df, asset):
    states = df[asset]

    previous_states = states.shift(1)

    transitions = states != previous_states

    transition_rows = df.index[
        transitions
    ].tolist()

    return transition_rows

def calculate_change_score(df, source_asset, target_asset, window=5):

    transition_rows = get_transition_rows(df,source_asset)
    transition_rows = transition_rows[:500]

    total_change = 0

    for row in transition_rows:

        if row + window >= len(df):
            continue

        before = df.iloc[row][target_asset]

        after = df.iloc[
            row + window
        ][target_asset]

        change = abs(after - before)

        total_change += change

    return total_change


def discover_relationships(df, source_asset, assets):

    relationships = []

    for asset in assets:

        if asset == source_asset:
            continue

        score = calculate_change_score(
            df,
            source_asset,
            asset
        )

        relationships.append({
            "source": source_asset,
            "target": asset,
            "score": score
        })

    report = pd.DataFrame(
        relationships
    )

    report = report.sort_values(
        by="score",
        ascending=False
    )

    return report


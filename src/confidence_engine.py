import pandas as pd


def normalize(df, score_column):

    max_score = df[score_column].max()

    df["normalized"] = (
        df[score_column] / max_score
    )

    return df


def build_dependency_confidence():

    rf = pd.read_csv(
        "reports/dependency_same_stage.csv"
    )

    mi = pd.read_csv(
        "reports/dependency_mi_same_stage.csv"
    )

    xgb = pd.read_csv(
        "reports/dependency_xgb_same_stage.csv"
    )

    rf = normalize(
        rf,
        "importance"
    )

    mi = normalize(
        mi,
        "mi_score"
    )

    xgb = normalize(
        xgb,
        "importance"
    )

    confidence = (
        rf[["target","dependency","normalized"]]
        .rename(
            columns={
                "normalized":"rf_score"
            }
        )
    )

    confidence = confidence.merge(
        mi[
            ["target","dependency","normalized"]
        ].rename(
            columns={
                "normalized":"mi_score"
            }
        ),
        on=["target","dependency"],
        how="outer"
    )

    confidence = confidence.merge(
        xgb[
            ["target","dependency","normalized"]
        ].rename(
            columns={
                "normalized":"xgb_score"
            }
        ),
        on=["target","dependency"],
        how="outer"
    )

    confidence = confidence.fillna(0)

    confidence["confidence"] = (
        confidence["rf_score"] +
        confidence["mi_score"] +
        confidence["xgb_score"]
    ) / 3

    confidence = confidence.sort_values(
        by="confidence",
        ascending=False
    )

    confidence.to_csv(
        "reports/dependency_confidence.csv",
        index=False
    )

    print("\nDEPENDENCY CONFIDENCE")
    print("=====================")

    print(
        confidence.head(20)
    )

    return confidence
import pandas as pd


def build_consensus_dependency(
    rf_report,
    mi_report,
    xgb_report
):

    votes = {}

    # Random Forest
    for _, row in rf_report.iterrows():

        key = (
            row["target"],
            row["dependency"]
        )

        votes[key] = votes.get(key, 0) + 1

    # Mutual Information
    for _, row in mi_report.iterrows():

        key = (
            row["target"],
            row["dependency"]
        )

        votes[key] = votes.get(key, 0) + 1

    # XGBoost
    for _, row in xgb_report.iterrows():

        key = (
            row["target"],
            row["dependency"]
        )

        votes[key] = votes.get(key, 0) + 1

    results = []

    for key, count in votes.items():

        target, dependency = key

        results.append(
            {
                "target": target,
                "dependency": dependency,
                "votes": count
            }
        )

    report = pd.DataFrame(results)

    report = report.sort_values(
        by=["target", "votes"],
        ascending=[True, False]
    )

    return report
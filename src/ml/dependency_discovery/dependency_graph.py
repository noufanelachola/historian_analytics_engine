import pandas as pd


class DependencyGraph:

    def __init__(
        self,
        consensus_file,
        min_votes=2
    ):

        self.df = pd.read_csv(
            consensus_file
        )

        self.min_votes = min_votes

    def get_dependencies(
        self,
        asset
    ):

        rows = self.df[
            (self.df["target"] == asset)
            &
            (self.df["votes"] >= self.min_votes)
        ]

        rows = rows.sort_values(
            by="votes",
            ascending=False
        )

        return rows[
            "dependency"
        ].tolist()

    def get_dependency_report(
        self,
        asset
    ):

        rows = self.df[
            self.df["target"] == asset
        ]

        rows = rows.sort_values(
            by="votes",
            ascending=False
        )

        return rows
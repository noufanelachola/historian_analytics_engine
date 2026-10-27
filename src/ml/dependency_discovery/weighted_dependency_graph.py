import pandas as pd


class WeightedDependencyGraph:

    def __init__(
        self,
        confidence_file,
        min_confidence=0.1
    ):

        self.df = pd.read_csv(
            confidence_file
        )

        self.df = self.df[
            self.df["confidence"] >= min_confidence
        ]

    def get_dependencies(
        self,
        target_asset
    ):

        rows = self.df[
            self.df["target"] == target_asset
        ]

        return list(
            zip(
                rows["dependency"],
                rows["confidence"]
            )
        )
import pandas as pd


def validate_timestamps(df, timestamp_col="Timestamp"):
    """
    Validate timestamp ordering, duplicates, missing timestamps,
    backward jumps, and unusually large time gaps.

    Parameters
    ----------
    df : pandas.DataFrame
        Already-loaded dataset.
    timestamp_col : str
        Name of the timestamp column.
    """

    print("\n" + "=" * 50)
    print("TIMESTAMP VALIDATION")
    print("=" * 50)

    if timestamp_col not in df.columns:
        print(f"ERROR: Column '{timestamp_col}' not found.")
        print("Available columns:", df.columns.tolist())
        return

    # Convert timestamps for validation without modifying df
    timestamps = pd.to_datetime(
        df[timestamp_col],
        errors="coerce"
    )

    missing_count = timestamps.isna().sum()
    valid_timestamps = timestamps.dropna()

    if valid_timestamps.empty:
        print("ERROR: No valid timestamps found.")
        return

    # Check ordering in the original row order
    differences = valid_timestamps.diff()

    is_sorted = valid_timestamps.is_monotonic_increasing
    duplicate_count = valid_timestamps.duplicated().sum()
    backward_jumps = (differences < pd.Timedelta(0)).sum()

    positive_differences = differences[
        differences > pd.Timedelta(0)
    ]

    print(f"Total rows: {len(df):,}")
    print(f"Valid timestamps: {len(valid_timestamps):,}")
    print(f"Missing/invalid timestamps: {missing_count:,}")
    print(f"Already sorted: {is_sorted}")
    print(f"Backward jumps: {backward_jumps:,}")
    print(f"Duplicate timestamps: {duplicate_count:,}")

    print("\nFirst timestamp:", valid_timestamps.iloc[0])
    print("Last timestamp: ", valid_timestamps.iloc[-1])

    if not positive_differences.empty:
        print("\nLargest positive time gaps:")
        print(
            positive_differences
            .nlargest(5)
            .to_string()
        )

    # Display examples of backward jumps
    if backward_jumps > 0:
        print("\nExamples of backward timestamp jumps:")

        jump_positions = differences[
            differences < pd.Timedelta(0)
        ].index[:5]

        for position in jump_positions:
            print(
                f"Row index {position}: "
                f"previous valid timestamp = "
                f"{valid_timestamps.loc[:position].iloc[-2] if len(valid_timestamps.loc[:position]) > 1 else 'N/A'}, "
                f"current timestamp = {valid_timestamps.loc[position]}"
            )

    print("\n" + "=" * 50)
    print("VALIDATION COMPLETE")
    print("=" * 50)
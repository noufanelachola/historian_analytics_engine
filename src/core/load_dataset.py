import pandas as pd

# def load_dataset(path):
#     df = pd.read_csv(path)
#     df.columns = df.columns.str.strip()  

#     print("\nMISSING VALUES REPORT")
#     print("=====================")

#     missing = df.isna().sum()

#     missing = missing[missing > 0]

#     print(missing.sort_values(ascending=False))

#     return df

import pandas as pd


def load_dataset(path):

    df = pd.read_csv(path)

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    print("\nDATASET SHAPE")
    print("=============")
    print(df.shape)

    print("\nMISSING VALUES REPORT")
    print("=====================")

    missing = df.isna().sum()

    missing = missing[missing > 0]

    if len(missing) == 0:
        print("No missing values found.")
    else:
        print(
            missing.sort_values(
                ascending=False
            )
        )

    print("\nCOLUMN CHECK")
    print("============")

    columns_to_check = [
        "MV101",
        "AIT201",
        "MV201",
        "P201",
        "P202",
        "P204",
        "MV303"
    ]

    for col in columns_to_check:

        if col not in df.columns:
            print(f"{col} : NOT FOUND")
            continue

        print(
            f"{col}"
            f" | NaNs: {df[col].isna().sum()}"
            f" | Unique Values: {df[col].nunique(dropna=True)}"
        )

    print("\nSAMPLE DATA")
    print("===========")

    sample_columns = [
        col for col in [
            "MV101",
            "AIT201",
            "MV201"
        ]
        if col in df.columns
    ]

    if len(sample_columns) > 0:
        print(
            df[sample_columns]
            .head(20)
        )

    print("\nCOLUMN NAMES")
    print("============")

    print(df.columns.tolist())

    print("\nNORMAL/ATTACK COLUMN")
    print("====================")

    print(
        df["Normal/Attack"]
        .value_counts(dropna=False)
    )

    print("\nUNIQUE VALUES")
    print("=============")

    print(
        df["Normal/Attack"]
        .unique()
    )

    print("\nFIRST NaN LOCATIONS")
    print("===================")

    for col in [
        "MV101",
        "AIT201",
        "MV201",
        "P201",
        "P202",
        "P204",
        "MV303"
    ]:

        nan_rows = df[df[col].isna()]

        if len(nan_rows) == 0:
            continue

        first_nan = nan_rows.index[0]

        print(
            f"{col}: first NaN at row {first_nan}"
        )

        print("\nROWS AROUND BOUNDARY")
        
    print("====================")

    print(
        df.loc[
            395290:395305,
            [
                "Timestamp",
                "MV101",
                "AIT201",
                "MV201",
                "P201",
                "MV303"
            ]
        ]
    )

    return df
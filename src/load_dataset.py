import pandas as pd

def load_dataset(path):
    df = pd.read_csv(path)

    # Strip whitespace from the column names
    df.columns = df.columns.str.strip()  

    print(df["Normal/Attack"].value_counts())

    return df
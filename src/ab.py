import pandas as pd

df = pd.read_csv(
    "./data/DataNew13-14.csv",
    encoding="utf-16"
)

print(df.shape)
print(df.columns.tolist())
print(df.head())
print(df.isna().sum().sum())
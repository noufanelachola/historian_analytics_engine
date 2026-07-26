from dataset_loader import load_dataset

df = load_dataset("datasets/swat/swat.csv")

print(df.shape)
print(df.columns)



import pandas as pd

file_path = "../data_raw/Electric_Vehicle_Population_Data.csv"
df = pd.read_csv(file_path)

print("=== 1. Dataset Shape (Rows, Columns) ===")
print(df.shape)

print("\n=== 2. First 5 Rows ===")
print(df.head())

print("\n=== 3. Dataset Info ===")
print(df.info())

print("\n=== 4. Missing Values Count ===")
print(df.isnull().sum())

print("\n=== 5. Duplicated Rows count ===")
print(df.duplicated().sum())

print("\n=== 6. Descriptive Statistics ===")
print(df.describe())


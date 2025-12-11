import pandas as pd

df = pd.read_csv("raw_merged.csv")

# Уникальные категории
print("\nУникальные категории")
print(df["category"].unique())

# Уникальные цвета
print("\nУникальные цвета")
print(df["color"].unique())

print(df["price"].unique())

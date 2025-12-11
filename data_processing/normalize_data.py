import pandas as pd

from category_map import normalize_category
from color_map import normalize_color, preprocess
from price_cleaner import clean_price
from name_cleaner import clean_name


df = pd.read_csv("raw_merged.csv")

df = df.replace({"": None, " ": None, "nan": None})
df = df.fillna('')

# Цвета
df["color_clean"] = df["color"].apply(preprocess)
df["color_norm"] = df["color"].apply(normalize_color)

# Категории
df["category_norm"] = df["category"].apply(normalize_category)

# Цена
df["price_norm"] = df["price"].apply(clean_price)

# Названия
df["name_clean"] = df.apply(
    lambda row: clean_name(row["name"], row["shop"]),
    axis=1
)

df.to_csv("clean_norm.csv", index=False, encoding="utf-8-sig")









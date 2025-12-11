import os
import pandas as pd
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

df = pd.read_csv("../data_processing/clean_norm.csv")

# ————— ИСПРАВЛЕНИЕ "nan" —————
df = df.replace({pd.NA: None, float("nan"): None, "nan": None, "NaN": None})
df = df.where(pd.notnull(df), None)

# оставляем только нужные колонки (14)
df = df[
    [
        "shop",
        "category_norm",
        "name_clean",
        "article",
        "color_norm",
        "price_norm",
        "image",
        "url"
    ]
]

insert_sql = """
INSERT INTO products (
    shop, category_norm, name_clean, article, color_norm,
    price_norm, image, url
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""


for _, row in df.iterrows():
    cursor.execute(insert_sql, tuple(row.values))

conn.commit()

cursor.close()
conn.close()


import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PARSERS_DIR = BASE / "parsers"

def load_and_merge():
    files = [
        "irnby_products.csv",
        "lookonline_products.csv",
        "feelz_products.csv",
        "lime_products.csv",
        "befree_products.csv"

    ]

    dfs = []
    for f in files:
        df = pd.read_csv(PARSERS_DIR / f)

        required_columns = ["shop", "category", "id", "name", "article", "color", "price", "image", "url"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Invalid CSV format: missing required columns in {f}")

        df["source"] = f
        dfs.append(df)

    full = pd.concat(dfs, ignore_index=True)

    OUTPUT = BASE / "data_processing" / "raw_merged.csv"
    full.to_csv(OUTPUT, index=False)

    print("Готово! Сохранено в", OUTPUT)


if __name__ == "__main__":
    load_and_merge()

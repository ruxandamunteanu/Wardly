import requests
import csv
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

CATEGORIES_URL = "https://irnby.com/api/categories"
FIRST_PAGE_URL = "https://irnby.com/api/pages/catalog"
LOAD_MORE_URL = "https://irnby.com/api/pages/catalog/load-more"

session = requests.Session()

retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retry))

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://irnby.com/"
}


# категории
def get_categories():
    r = session.get(CATEGORIES_URL, headers=HEADERS)
    r.raise_for_status()
    cats = r.json()

    EXCLUDED_SLUGS = {
        "women",
        "new",
        "soon",
        "sport",
        "casual",
        "activities",
        "must-have",
        "underwear",
        "men",
    }

    filtered = []

    for c in cats:
        slug = (c.get("slug") or "").lower()

        if not slug:
            continue

        if slug in EXCLUDED_SLUGS:
            continue

        if slug.endswith("-spirit"):
            continue

        filtered.append(c)

    return filtered


# товары
def get_page(category_id, page):
    payload = {
        "categories": [category_id],
        "page": page,
        "currencyCode": "RUB",
        "query": "",
        "inStock": True,
        "sort": "DEFAULT"
    }

    url = FIRST_PAGE_URL if page == 1 else LOAD_MORE_URL
    r = session.post(url, json=payload, headers=HEADERS)
    r.raise_for_status()

    return r.json().get("products", [])


def get_all_products(category_id):
    all_items = []
    page = 1

    while True:
        products = get_page(category_id, page)
        if not products:
            break

        all_items.extend(products)
        page += 1
        time.sleep(random.uniform(0.5, 1.1))

    return all_items


# обработка товара
def parse_product(p, category_title):

    sku = p.get("skus", [])
    if sku:
        sku = sku[0]
        article = sku.get("article", "")
        color = sku.get("color", {}).get("title", "")
    else:
        article = ""
        color = ""

    images = p.get("images", []) or [""]
    image_url = images[0]

    if "MEN" in image_url.upper():
        return None

    return {
        "shop": "irnby",
        "category": category_title,
        "id": p.get("id"),
        "name": p.get("title"),
        "article": article,
        "color": color,
        "price": p.get("prices", {}).get("RUB", {}).get("price", ""),
        "image": image_url,
        "url": f"https://irnby.com/product/{p.get('slug', '')}"
    }


if __name__ == "__main__":
    print("Получаем категории...")
    categories = get_categories()
    print(f"Категорий после фильтрации: {len(categories)}")

    EXCLUDE_CATEGORIES = {
        "Спортивный инвентарь",
        "Украшения",
        "Посуда",
        "Декор",
        "Объекты",
        "Картины",
        "ART"
    }

    all_products = []
    seen = set()

    for cat in categories:
        title = (cat.get("title") or "").strip()

        if title in EXCLUDE_CATEGORIES:
            print(f"Пропуск: {title}")
            continue

        cid = cat["id"]
        print(f"\nКатегория: {title}")

        items = get_all_products(cid)
        print(f"Найдено товаров: {len(items)}")

        for p in items:
            pr = parse_product(p, title)

            if pr is None:
                continue

            if pr["id"] not in seen:
                seen.add(pr["id"])
                all_products.append(pr)

    # Сохранение CSV
    if all_products:
        with open("irnby_products.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_products[0].keys())
            writer.writeheader()
            writer.writerows(all_products)

    print(f"\nВсего товаров: {len(all_products)}")

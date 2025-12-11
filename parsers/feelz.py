import requests
import csv
import time

BASE_URL = "https://feelz.ru/api/customer/v1/catalog"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "accept": "application/json",
    "content-type": "application/json"
}

CATEGORIES = {
    "bodi-2-zhenskie": "Боди женские",
    "bryki-zhenskie": "Брюки женские",
    "vyazanyiy-trikotazh-4-zhenskie": "Вязаный трикотаж",
    "tolstovki-2-zhenskie": "Толстовки",
    "topy-2-zhenskie": "Топы",
    "zhakety-zhenskie": "Жакеты",
    "longslivy-zhenskie": "Лонгсливы",
    "shorty-zhenskie": "Шорты",
    "futbolki-zhenskie": "Футболки",
    "bluzy-i-rubashki-6-zhenskie": "Блузы и рубашки",
    "platya-2-zhenskie": "Платья",
    "dzhinsy-zhenskie": "Джинсы",
    "ybki-zhenskie": "Юбки",
    "kostyumy-zhenskie": "Костюмы",
    "puhoviki-zhenskie": "Пуховики женские",
    "kurtki-zhenskie": "Куртки женские",
    "zhiletki-zhenskie": "Жилетки женские",
    "shapki-zhenskie-new": "Шапки женские"
}

def parse_product(card, category_title):
    name = card.get("name", "")

    variant = card.get("selectedVariant", {}) or {}

    article = variant.get("seller_sku", "")
    price = (
        variant.get("final_price")
        or variant.get("price")
        or card.get("finalPrice")
        or card.get("price")
        or ""
    )

    color = ""
    for ch in variant.get("characteristics", []):
        if ch.get("slug") == "cvet":
            color = ch.get("value", "")
            break

    image = ""
    media = variant.get("media_items") or card.get("media_items") or []
    if media:
        image = media[0].get("payload", {}).get("file_path", "")

    url = (
        variant.get("link_url")
        or card.get("link_url")
        or ("https://feelz.ru" + variant.get("relative_link_url", ""))
        or ("https://feelz.ru" + card.get("relative_link_url", ""))
    )

    prod_id = (
        variant.get("product_id")
        or card.get("product_id")
        or card.get("product_card_id", "")
    )

    return {
        "shop": "feelz",
        "category": category_title,
        "id": prod_id,
        "name": name,
        "article": article,
        "color": color,
        "price": price,
        "image": image,
        "url": url
    }

def load_category(slug, title):
    all_items = []
    seen_ids = set()
    page = 1

    while True:
        print(f"\nКатегория {slug}, страница {page}")

        payload = {
            "stock_availability": "available_only",
            "statuses": ["PUBLISHED"],
            "characteristics": [],
            "page": page,
            "per_page": 32,
            "category_slug": slug,
            "collection_slugs": []
        }

        r = requests.post(BASE_URL, json=payload, headers=HEADERS)
        print("STATUS:", r.status_code)

        if r.status_code != 200:
            break

        data = r.json()
        views = data.get("views", [])

        if not views:
            print("конец категории")
            break

        page_cards = []
        for v in views:
            page_cards.extend(v.get("cards", []))

        if not page_cards:
            break

        print(f"найдено карточек: {len(page_cards)}")

        for card in page_cards:
            variant = card.get("selectedVariant", {}) or {}
            prod_id = (
                variant.get("product_id")
                or card.get("product_id")
                or card.get("product_card_id")
            )

            if prod_id and prod_id in seen_ids:
                continue

            seen_ids.add(prod_id)
            item = parse_product(card, title)
            all_items.append(item)

        page += 1
        time.sleep(0.3)

    print(f"Всего товаров в категории {title}: {len(all_items)}")
    return all_items

if __name__ == "__main__":

    all_items = []

    for slug, title in CATEGORIES.items():
        print(f"\n{title} ({slug})")
        items = load_category(slug, title)
        all_items.extend(items)


    if all_items:
        with open("feelz_products.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["shop", "category", "id", "name",
                            "article", "color", "price", "image", "url"]
            )
            writer.writeheader()
            writer.writerows(all_items)

    print(f"\nВсего товаров: {len(all_items)}")














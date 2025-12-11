import requests
import csv
import time

CATEGORIES = [
    "dresses",
    "women_blazers_waistcoats",
    "women_tops_bodysuits",
    "trousers",
    "women_shirts_all",
    "women_skirts_shorts",
    "outerwear",
    "women_sweaters_cardigans",
    "women_jeans",
    "t_shirts",
    "all_shoes"
]

BASE_URL = "https://limestore.com/api/section/{}"


# Извлечение цены

def extract_price(skus):
    if not isinstance(skus, list) or len(skus) == 0:
        return ""

    first = skus[0]

    if isinstance(first, dict):
        return first.get("price", "")

    if isinstance(first, list) and len(first) > 0 and isinstance(first[0], dict):
        return first[0].get("price", "")

    return ""


# Запрос страницы

def get_page(code, page):
    url = BASE_URL.format(code) + f"?page={page}&page_size=4"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


# Извлечение товаров

def extract_products(data, category):
    products = []

    for block in data.get("items", []):
        for cell in block.get("cells", []):
            if cell.get("type") != "product":
                continue

            product = cell.get("entity", {})
            models = product.get("models", [])

            for model in models:
                skus = model.get("skus", [])
                color = model.get("color", {}).get("name", "")
                photo = model.get("photo", {})
                model_code = model.get("code")

                # формируем URL товара
                if model_code:
                    url = (
                        f"https://limestore.com/ru_ru/product/"
                        f"{product.get('code')}-{model_code}"
                    )
                else:
                    url = f"https://limestore.com/ru_ru/product/{product.get('code')}"

                products.append({
                    "shop": "lime",
                    "category": category,
                    "id": product.get("id", ""),
                    "name": product.get("name", ""),
                    "article": product.get("article", ""),
                    "color": color,
                    "price": extract_price(skus),
                    "image": photo.get("url", ""),
                    "url": url
                })

    return products


# Сохранение cvs

def save_to_csv(filename, data):
    if not data:
        print("Нет данных для сохранения")
        return

    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)



if __name__ == "__main__":

    all_products = []
    seen = set()

    for code in CATEGORIES:
        print(f"\n Парсим категорию: {code} ")

        first_page = get_page(code, 1)
        total_pages = first_page["meta"]["total"]
        print(f"Страниц: {total_pages}")

        for page in range(1, total_pages + 1):
            print(f"  Страница {page}/{total_pages}")

            try:
                data = get_page(code, page)
            except Exception as e:
                print("Ошибка:", e)
                break

            products = extract_products(data, code)

            for p in products:
                uniq_key = (p["id"], p["color"])

                if uniq_key in seen:
                    continue

                seen.add(uniq_key)
                all_products.append(p)

            time.sleep(0.3)

    save_to_csv("lime_products.csv", all_products)

    print(f"\nВсего товаров: {len(all_products)}")

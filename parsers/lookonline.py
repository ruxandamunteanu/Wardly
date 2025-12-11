import requests
import csv
import time
import random
import uuid
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept-Language": "ru,en;q=0.9",
    "Referer": "https://lookonline.ru/",
    "Connection": "keep-alive",
}

# Глобальная сессия
session = requests.Session()
session.headers.update(HEADERS)

#  Категории
CATEGORIES = {
    "outerwear": "https://lookonline.ru/odeghda/verhnyaya%20odeghda/?rdrf[attr][17][]=интернетмагазин",
    "blazers": "https://lookonline.ru/odeghda/pidghaki1ghakety/?rdrf[attr][17][]=интернетмагазин",
    "jeans": "https://lookonline.ru/odeghda/dghinsy/?rdrf[attr][17][]=интернетмагазин",
    "tricot": "https://lookonline.ru/odeghda/trikotaj/?rdrf[attr][17][]=интернетмагазин",
    "pants": "https://lookonline.ru/odeghda/bryuki/?rdrf[attr][17][]=интернетмагазин",
    "tshirts": "https://lookonline.ru/odeghda/futbolki%20%7C%20longslivy/?rdrf[attr][17][]=интернетмагазин",
    "tops": "https://lookonline.ru/odeghda/topy%20%7C%20bodi%20%7C%20kombinezony/?rdrf[attr][17][]=интернетмагазин",
    "hoodies": "https://lookonline.ru/odeghda/hudi%20%7C%20svitshoty%20%7C%20tolstovki/?rdrf[attr][17][]=интернетмагазин",
    "dresses": "https://lookonline.ru/odeghda/platyya/?rdrf[attr][17][]=интернетмагазин",
    "skirts": "https://lookonline.ru/odeghda/yubki/?rdrf[attr][17][]=интернетмагазин",
    "shorts": "https://lookonline.ru/odeghda/shorty/?rdrf[attr][17][]=интернетмагазин",
    "shirts": "https://lookonline.ru/odeghda/bluzki%20%7C%20rubashki/?rdrf[attr][17][]=интернетмагазин",
    "shoes": "https://lookonline.ru/obuv--aksessuary/obuvy/?rdrf[attr][17][]=интернетмагазин"
}

# загрузка страницы
def get_soup(url):
    time.sleep(random.uniform(1.5, 3.0))

    try:
        r = session.get(url, timeout=20)
    except Exception:
        print("Ошибка сети — повтор через 5 сек...")
        time.sleep(5)
        r = session.get(url, timeout=20)

    if r.status_code == 403:
        print(f"403! Блокировка — жду 10 сек…")
        time.sleep(10)
        r = session.get(url, timeout=20)
        if r.status_code == 403:
            print(f"Пропускаю URL: {url}")
            return BeautifulSoup("<html></html>", "html.parser")

    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

# Кол-во страниц
def get_total_pages(soup):
    pages = soup.select(".pagination a")
    nums = [int(x.text.strip()) for x in pages if x.text.strip().isdigit()]
    return max(nums) if nums else 1

#  Cтраница товара
def parse_product_page(url):
    soup = get_soup(url)

    article_el = soup.select_one(".product_info_item p.title:contains('Артикул')")
    article = article_el.find_next("p", class_="value").get_text(strip=True) if article_el else ""

    color_el = soup.select_one(".product_info_item p.title:contains('Цвет')")
    color = color_el.find_next("p", class_="value").get_text(strip=True) if color_el else ""

    return article, color

#  карточка из каталога
def parse_card(card):
    a = card.find("a")
    url = a["href"]
    if not url.startswith("http"):
        url = urljoin("https://lookonline.ru/", url)

    name = card.select_one(".product_name").get_text(strip=True)
    price = card.select_one(".price").get_text(strip=True)

    img = card.select_one("img")
    image = img["src"] if img else ""

    return name, price, image, url

# Главный цикл
all_products = []

for code, cat_url in CATEGORIES.items():
    print(f"\n=== Категория: {code} ===")

    soup = get_soup(cat_url)
    total_pages = get_total_pages(soup)
    print(f"Страниц: {total_pages}")

    for page in range(1, total_pages + 1):
        page_url = cat_url + f"&PAGEN_1={page}"
        print(f"  → Страница {page}: {page_url}")

        page_soup = get_soup(page_url)
        cards = page_soup.select(".product_item")
        print(f"    Найдено товаров: {len(cards)}")

        for card in cards:
            name, price, image, url = parse_card(card)
            article, color = parse_product_page(url)


            product_id = str(uuid.uuid4())

            all_products.append({
                "shop": "lookonline",
                "category": code,
                "id": product_id,
                "name": name,
                "article": article,
                "color": color,
                "price": price,
                "image": image,
                "url": url,
            })

#
with open("lookonline_products.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "shop", "category", "id", "name", "article", "color", "price", "image", "url"
    ])
    writer.writeheader()
    writer.writerows(all_products)

print(f"Всего товаров: {len(all_products)}")



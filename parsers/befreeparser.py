import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
}

SHOP_NAME = "befree"

def clean_text(text):
    """Чистим текст от лишних пробелов, неразрывных пробелов и запятых"""
    if text:
        return text.replace('\xa0', ' ').replace(',', '').strip()
    return ''

def get_category_from_url(url):
    """Получаем название категории из URL"""
    path = urlparse(url).path
    parts = path.strip('/').split('/')
    return parts[-1] if parts else ''

def parse_page(url, category):
    """Парсинг одной страницы категории с точными селекторами для name и price"""
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    container = soup.select_one('div.sc-6f929eaa-2.jTojHQ')
    products = []
    if container:
        for a in container.find_all('a', href=True):
            link = a.get('href')

            # Получаем id товара
            item_id = a.get('data-item-id') or ''

            # Название по точному селектору внутри ссылки
            name_tag = a.select_one(
                'div.sc-a0d6ee61-2.jfixMg > div.sc-a0d6ee61-3.liGEjk > div.sc-7b424381-0.fzBzDT.sc-a0d6ee61-1.AWnf'
            )
            name = clean_text(name_tag.get_text() if name_tag else '')

            # Цена по точному селектору внутри ссылки
            price_tag = a.select_one(
                f'div.sc-a0d6ee61-2.jfixMg > div.sc-a0d6ee61-3.liGEjk > div.sc-6407de65-0.ixkYkI'
            )
            price = clean_text(price_tag.get_text() if price_tag else '')

            # Артикул и цвет
            article = clean_text(a.get('data-article'))
            color = clean_text(a.get('data-color'))

            # Изображение
            img_tag = a.select_one('img')
            img = img_tag['src'] if img_tag else ''

            products.append({
                'shop': SHOP_NAME,
                'category': category,
                'id': item_id,
                'name': name,
                'article': article,
                'color': color,
                'price': price,
                'image': img,
                'url': link
            })
    return products

def parse_category(base_url, max_pages=20, delay=1.0):
    """Парсинг всей категории с пагинацией"""
    category_name = get_category_from_url(base_url)
    all_products = []
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        print(f"Парсим: {url}")
        try:
            products = parse_page(url, category_name)
            if not products:
                print("Товары на странице не найдены. Останавливаемся.")
                break
            all_products.extend(products)
        except Exception as e:
            print(f"Ошибка на странице {page}: {e}")
            break
        time.sleep(delay)
    return all_products

def save_to_csv(products, filename='products.csv'):
    """Сохраняем товары в CSV с новой структурой"""
    keys = ['shop', 'category', 'id', 'name', 'article', 'color', 'price', 'image', 'url']
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for p in products:
            writer.writerow(p)
    print(f"Сохранено {len(products)} товаров в {filename}")

if __name__ == '__main__':
    categories = [
        'https://befree.ru/zhenskaya/zen-verxniaia-odezda',
        'https://befree.ru/zhenskaya/platia',
    ]
    all_products = []
    for cat_url in categories:
        products = parse_category(cat_url, max_pages=20, delay=1.0)
        all_products.extend(products)

    save_to_csv(all_products)

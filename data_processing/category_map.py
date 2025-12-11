CATEGORY_MAP = {
    # спортивная одежда
    "топы спортивные": "sportswear",
    "легинсы": "sportswear",
    "рашгарды": "sportswear",
    "брюки спортивные": "sportswear",
    "лонгсливы спортивные": "sportswear",
    "шорты спортивные": "sportswear",
    "комбинезоны спортивные": "sportswear",
    "платья спортивные": "sportswear",
    "футболки спортивные": "sportswear",
    "велосипедки": "sportswear",

    # аксессуары
    "accessories": "accessories",
    "сумки": "accessories",
    "шапки женские": "accessories",

    # верхняя одежда
    "верхняя одежда": "outerwear",
    "outerwear": "outerwear",
    "пуховики женские": "outerwear",
    "куртки женские": "outerwear",
    "жилетки женские": "outerwear",
    "zen-verxniaia-odezda": "outerwear",
    "zilety-zenskie": "outerwear",


    # платья
    "платья": "dresses",
    "dresses": "dresses",
    "platia": "dresses",

    # джинсы
    "джинсы": "jeans",
    "jeans": "jeans",
    "dzinsy-zenskie": "jeans",
    "women_jeans": "jeans",

    # брюки
    "брюки": "pants",
    "брюки женские": "pants",
    "briuki-zenskie": "pants",
    "pants": "pants",
    "trousers": "pants",
    "брюки из экокожи": "pants",

    # топы
    "топы": "tops",
    "топы и корсеты": "tops",
    "tops": "tops",
    "topy": "tops",
    "women_tops_bodysuits": "tops",
    "maiki-zenskie": "tops",


    # блузки/рубашки
    "блузы и рубашки": "shirts",
    "shirts": "shirts",
    "bluzki": "shirts",
    "rubaski-zenskie": "shirts",
    "women_shirts_all": "shirts",

    # худи/толстовки
    "худи и толстовки": "hoodies",
    "hoodies": "hoodies",
    "tolstovki": "hoodies",
    "svitsoty-zenskie": "hoodies",
    "xudi-zenskie": "hoodies",
    "tolstovki-zenskie": "hoodies",
    "longslivy-zenskie": "hoodies",
    "толстовки": "hoodies",

    # футболки
    "футболки": "tshirts",
    "tshirts": "tshirts",
    "futbolki-zenskie": "tshirts",
    "polo-zenskie": "tshirts",
    "t_shirts": "tshirts",
    "лонгсливы": "tshirts",

    # юбки
    "юбки": "skirts",
    "skirts": "skirts",
    "iubki": "skirts",
    "women_skirts_shorts": "skirts",

    # шорты
    "шорты": "shorts",
    "shorts": "shorts",
    "sorty-zenskie": "shorts",
    "women_skirts_shorts": "shorts",

    # трикотаж/свитеры
    "вязаный трикотаж": "sweaters",
    "tricot": "sweaters",
    "zen-svitery-i-kardigany": "sweaters",
    "women_sweaters_cardigans": "sweaters",

    # блейзеры/жакеты
    "women_blazers_waistcoats": "blazers",
    "жакеты": "blazers",
    "blazers": "blazers",
    "pidzaki-i-zakety": "blazers",

    # нижнее белье/боди
    "нижнее белье": "lingerie",
    "боди женские": "lingerie",
    "bluzki-bodi": "lingerie",

    # купальники
    "купальники": "swimwear",

    # костюмы
    "костюмы": "suits",

    # обувь
    "all_shoes": "shoes",
}

def normalize_category(cat: str) -> str:
    if not isinstance(cat, str):
        return "other"

    key = cat.strip().lower()
    return CATEGORY_MAP.get(key, "other")

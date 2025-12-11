import re

COLOR_MAP = {

    # White
    "экрю": "white",
    "цвет слоновой кости": "white",
    "небеленое полотно": "white",
    "молочный": "white",
    "молочный меланж": "white",

    # Beige
    "ванильный": "beige",
    "лате": "beige",
    "тауп": "beige",
    "песочный": "beige",
    "карамельный": "beige",
    "верблюжий": "beige",
    "кремовый": "beige",
    "кремовый меланж": "beige",
    "табачный": "beige",

    # Brown
    "каштановый": "brown",
    "шоколад": "brown",
    "какао": "brown",
    "oak": "brown",

    # Grey
    "графит": "grey",
    "графитовый": "grey",
    "каменный": "grey",
    "сизый": "grey",

    # Blue
    "лазурный синий": "blue",
    "чернильный синий": "blue",
    "винтажный синий": "blue",
    "индиго": "blue",

    # Navy
    "blu scuro": "navy",
    "морской синий": "navy",
    "ультрамариновый": "navy",

    # Green
    "бирюзовый": "green",
    "бирюзово зеленый": "green",
    "фисташковый": "green",
    "шалфей": "green",
    "минт": "green",
    "лаймовый": "green",
    "kale": "green",

    # Khaki
    "хаки": "khaki",

    # Red
    "малиновый": "red",
    "виноградно красный": "red",
    "гранатовый": "red",
    "марсала": "red",
    "темный тинт": "red",

    # Pink
    "пудровый": "pink",
    "персиковый": "pink",
    "bonbon": "pink",
    "candy": "pink",

    # Purple
    "лиловый": "purple",
    "лавандовый": "purple",
    "темный пурпурный": "purple",
    "сливовый": "purple",
    "фуксия": "purple",
    "сиреневый": "purple",

    # Yellow
    "лимонный желтый": "yellow",
    "льняной желтый": "yellow",
    "золотой": "yellow",
    "янтарный": "yellow",
    "светлолимонный": "yellow",

    # Orange
    "терракотовый": "orange",
    "светлолососевый": "orange",

    # Multicolor
    "многоцветные": "multicolor",
    "мультиколор": "multicolor",
    "разноцветный": "multicolor",
    "леопардовый": "multicolor",
    "leopard": "multicolor",

    "spirit": "purple",
    "сумерки": "purple",
}

def preprocess(c: str) -> str:
    if not isinstance(c, str):
        return ""

    c = c.lower().strip()

    c = re.sub(r"[^\w\s/]+", "", c)

    c = re.sub(r"[／⁄∕]", "/", c)

    c = c.replace("-", " ")

    c = c.replace("меланж", "")

    c = re.sub(r"\b(светло|темно|ярко)\b\s*", "", c)

    if "/" in c:
        c = c.split("/")[0].strip()

    c = re.sub(r"\s+", " ", c)

    return c.strip()


def auto(c: str) -> str:
    # английские базовые цвета
    ENGLISH = {
        "black": "black",
        "white": "white",
        "grey": "grey",
        "gray": "grey",
        "pink": "pink",
        "red": "red",
        "green": "green",
        "blue": "blue",
        "brown": "brown",
        "beige": "beige",
        "yellow": "yellow",
        "orange": "orange",
        "purple": "purple",
        "navy": "navy",
    }
    if c in ENGLISH:
        return ENGLISH[c]

    # русские корни
    if "черн" in c: return "black"
    if "бел" in c: return "white"
    if "сер" in c: return "grey"
    if "беж" in c or "лате" in c or "тауп" in c: return "beige"
    if "корич" in c or "какао" in c or "шокол" in c: return "brown"
    if "голуб" in c or "син" in c: return "blue"
    if "ультрамар" in c or "морск" in c: return "navy"
    if "зел" in c or "олив" in c or "бирюз" in c or "мят" in c: return "green"
    if "хаки" in c: return "khaki"
    if "крас" in c or "бордо" in c or "винн" in c: return "red"
    if "роз" in c or "пудр" in c or "персик" in c: return "pink"
    if "фиолет" in c or "лаванд" in c or "лилов" in c or "пурпур" in c: return "purple"
    if "желт" in c or "янтар" in c: return "yellow"
    if "оранж" in c or "терракот" in c: return "orange"
    if "разноцвет" in c or "multi" in c: return "multicolor"

    return "other"

def normalize_color(raw):
    c = preprocess(raw)

    if c in COLOR_MAP:
        return COLOR_MAP[c]

    return auto(c)









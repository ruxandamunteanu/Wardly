def clean_name(name: str, shop: str) -> str:
    if not isinstance(name, str):
        return name

    n = name.strip()

    # обработки для Feelz и Befree
    if shop in ["feelz", "befree"]:
        if "," in n:
            n = n.split(",", 1)[0].strip()

    # очистка лишних символов, пробелов
    n = " ".join(n.split())
    return n

import re
import math


def extract_digits(text: str) -> str:
    return re.sub(r"\D+", "", text)


def clean_price(raw):
    if raw is None or (isinstance(raw, float) and math.isnan(raw)):
        return None

    raw = str(raw).strip()

    nums = re.findall(r"\d[\d\s]*", raw)

    if nums:
        digits = extract_digits(nums[0])
    else:
        digits = extract_digits(raw)

    if digits == "":
        return None

    digits_len = len(digits)

    if "-" in raw and "%" in raw:

        if digits_len == 6:
            return int(digits[:3])

        if digits_len == 7:
            return int(digits[:3])

        if digits_len == 8:
            return int(digits[:4])

    return int(digits)


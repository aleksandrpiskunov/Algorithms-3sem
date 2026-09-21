from __future__ import annotations

import hashlib
import random

from data.categories_brands import categories, brand_groups
from data.price_data import (
    BASE_PRICES,
    BRAND_TIER_RANGES,
    PREMIUM_BRANDS,
    BUDGET_BRANDS,
    STORE_COEFFICIENTS,
)


def get_brand_tier(brand: str) -> str:
    """Определяет ценовой уровень бренда: premium / mid / budget."""
    if brand in PREMIUM_BRANDS:
        return "premium"
    if brand in BUDGET_BRANDS:
        return "budget"
    return "mid"


def get_brand_coefficient(category: str, brand: str) -> float:
    """
    Коэффициент бренда для конкретной категории.
    Берётся детерминированное случайное число внутри диапазона тира бренда,
    чтобы бренды одного уровня не были идентичны по цене, но результат был
    воспроизводим при повторном запуске генератора.
    """
    tier = get_brand_tier(brand)
    low, high = BRAND_TIER_RANGES[tier]
    local_rng = random.Random()
    return round(local_rng.uniform(low, high), 3)


def get_store_coefficient(store: str) -> float:
    if store in STORE_COEFFICIENTS:
        return STORE_COEFFICIENTS[store]
    local_rng = random.Random()
    return round(local_rng.uniform(0.85, 1.15), 3)


def generate_price(
    category: str,
    brand: str,
    store: str
) -> int:
    if category not in BASE_PRICES:
        raise ValueError(f"Неизвестная категория: {category!r}")

    base_price = BASE_PRICES[category]
    brand_coef = get_brand_coefficient(category, brand)
    store_coef = get_store_coefficient(store)

    noise_rng = random
    noise = noise_rng.uniform(0.95, 1.05)

    raw_price = base_price * brand_coef * store_coef * noise
    return raw_price


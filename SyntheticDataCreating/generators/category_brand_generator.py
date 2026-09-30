import random


def select_categories_and_brands(
        categories: list[str],
        brand_groups: dict[str, list[str]],
        n_categories: int,
        n_brands: int,
) -> dict[str, list[str]]:
    if not 1 <= n_categories <= len(categories):
        raise ValueError(f"Количество категорий должно быть от 1 до {len(categories)}")

    max_brands = min(len(brand_groups[c]) for c in categories)
    if not 1 <= n_brands <= max_brands:
        raise ValueError(f"Количество брендов должно быть от 1 до {max_brands}")

    chosen_categories = random.sample(categories, n_categories)
    return {
        category: random.sample(brand_groups[category], n_brands)
        for category in chosen_categories
    }


def generate_category(
        store: str,
        stores_data: dict[int, dict],
        brand_groups: dict[str, list[str]],
) -> str:
    store_record = None
    for s in stores_data.values():
        if s.get("name", "").lower() == store.lower():
            store_record = s
            break

    if store_record is None:
        raise ValueError(f"Магазин '{store}' не найден")

    store_categories = store_record.get("categories")
    if not store_categories:
        raise ValueError(f"У магазина '{store_record.get('name', store)}' не заданы категории")

    allowed = [c for c in store_categories if c in brand_groups]
    if not allowed:
        allowed = list(brand_groups)

    return random.choice(allowed)


def generate_brand(
        category: str,
        brand_groups: dict[str, list[str]]
) -> str:
    return random.choice(brand_groups[category])
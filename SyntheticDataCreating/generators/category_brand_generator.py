import random

def generate_category(store: int, stores_data: dict[int, dict]) -> str:

    for s in stores_data.values():
        if s.get("name", "").lower() == store.lower():
            store_record = s

    store_categories = store_record.get("categories")
    if not store_categories:
        raise ValueError(f"У магазина '{store_record.get('name', store)}' не заданы категории")

    return random.choice(store_categories)

def generate_brand(
        category: str,
        brand_groups: dict[str, list[str]] 
)-> str:
    return random.choice(brand_groups[category])

import random

def _resolve_store(store: int | str, stores_data: dict[int, dict]) -> dict:

    if isinstance(store, int):
        found = stores_data.get(store)
        if found is not None:
            return found
        raise ValueError(f"Магазин с id={store} не найден")

    if isinstance(store, str):
        for s in stores_data.values():
            if s.get("name", "").lower() == store.lower():
                return s
        raise ValueError(f"Магазин с названием '{store}' не найден")

    raise TypeError(f"store должен быть int (id) или str (название), получено: {type(store)}")


def generate_category(store: int | str, stores_data: dict[int, dict]) -> str:

    store_record = _resolve_store(store, stores_data)

    store_categories = store_record.get("categories")
    if not store_categories:
        raise ValueError(f"У магазина '{store_record.get('name', store)}' не заданы категории")

    return random.choice(store_categories)

def generate_brand(
        category: str,
        brand_groups: dict[str, list[str]] 
)-> str:
    return random.choice(brand_groups[category])

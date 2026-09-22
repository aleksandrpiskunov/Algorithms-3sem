import random

from generators.store_generator import generate_store, generate_datetime, generate_coords
from generators.category_brand_generator import generate_brand, generate_category
from generators.price_generator import generate_price
from generators.receipt_generator import ReceiptRegistry
from generators.card_generator import CardRegistry

def build_receipt(stores, banks_list, banks_probability, BANKS, categories, brand_groups, CARD_LENGTH, card_registry: CardRegistry, receipt_registry: ReceiptRegistry) -> list[dict]:
    store = generate_store(stores)

    purchase_datetime = generate_datetime(stores)

    card = card_registry.get_card(banks_list, banks_probability, BANKS, CARD_LENGTH)
    num_items = random.choices([2, 3, 4, 5], weights=[50, 30, 15, 5])[0]

    items = []
    for _ in range(num_items):
        category = generate_category(store, stores)
        brand = generate_brand(category, brand_groups)
        price = generate_price(category, brand, store)
        coords = generate_coords(stores)
        
        items.append({
            "category": category,
            "brand": brand,
            "price": price,
        })

    receipt_number = receipt_registry.generate_receipt_number(store)

    total = sum(item["price"] for item in items)

    rows = []
    for item in items:
        rows.append({
            "store_name": store,
            "Coords": f"{coords} и {purchase_datetime}",
            "category": item["category"],
            "brand": item["brand"],
            "price": item["price"],
            "card_number": card,
            "quantity": num_items,
            "receipt_number": receipt_number,
            "total": total
        })

    return rows


def build_dataset(min_rows: int, stores, banks_list, banks_probability, BANKS, categories, brand_groups, CARD_LENGTH) -> list[dict]:
    """Генерировать чеки, пока общее число строк не достигнет min_rows."""
    rows: list[dict] = []
    card_registry = CardRegistry()
    receipt_registry = ReceiptRegistry()
    while len(rows) < min_rows:
        rows.extend(build_receipt(stores, banks_list, banks_probability, BANKS, categories, brand_groups, CARD_LENGTH, card_registry, receipt_registry))
    return rows
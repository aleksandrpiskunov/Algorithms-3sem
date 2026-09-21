import random

def generate_category(
        categories: list[str],
)->str: 
    return random.choice(categories)


def generate_brand(
        category: str,
        brand_groups: dict[str, list[str]] 
)-> str:
    return random.choice(brand_groups[category])

import pandas as pd
from core.dataset_builder import build_dataset
from generators.category_brand_generator import select_categories_and_brands


from data.banks import banks_list, BANKS, CARD_LENGTH
from data.categories_brands import categories, brand_groups
from data.stores import stores

MIN_ROWS = 50000


def ask_int(prompt: str, min_value: int, max_value: int) -> int:
    """Спрашивает число в диапазоне [min_value, max_value], пока не получит корректный ответ."""
    while True:
        try:
            value = int(input(f"{prompt} (от {min_value} до {max_value}): "))
        except ValueError:
            print("Введите целое число.")
            continue
        if min_value <= value <= max_value:
            return value
        print(f"Число должно быть от {min_value} до {max_value}.")


def ask_bank_probabilities(count: int) -> list[float]:
    """Спрашивает вероятности банков в формате '43.51, 22.97, 11.49, ...' (сумма = 100)."""
    prompt = (
        'Введите вероятности появления карт банков через запятую (в %, сумма = 100) '
        'в порядке ["Сбербанк", "ВТБ", "Газпромбанк", "Альфа-Банк", "Т-Банк", '
        '"Россельхозбанк", "Почта Банк", "Промсвязьбанк"]\n'
        'Пример: 43.51, 22.97, 11.49, 8.71, 3.66, 3.55, 0.32, 5.79\n> '
    )
    while True:
        raw = input(prompt)
        try:
            values = [float(part.strip()) for part in raw.split(",")]
        except ValueError:
            print("Ошибка: ожидаются числа через запятую, дробная часть через точку.")
            continue
        if len(values) != count:
            print(f"Ошибка: нужно ровно {count} значений, получено {len(values)}.")
            continue
        if any(v < 0 for v in values):
            print("Ошибка: вероятности не могут быть отрицательными.")
            continue
        total = sum(values)
        if abs(total - 100) > 0.1:
            print(f"Ошибка: сумма вероятностей должна быть 100, сейчас {total:.2f}.")
            continue
        return values


if __name__ == "__main__":
    rows_count = int(input('Введите количество строк: '))
    if rows_count < MIN_ROWS: 
        rows_count = MIN_ROWS
        print(f"Минимальное количество строк - 50000. Будет создан датасет на 50000 строк")

    n_categories = ask_int("Сколько категорий использовать в датасете", 1, len(categories))
    max_brands = min(len(brand_groups[c]) for c in categories)
    n_brands = ask_int("Сколько брендов использовать в каждой категории", 1, max_brands)
    selected_brand_groups = select_categories_and_brands(categories, brand_groups, n_categories, n_brands)

    banks_probability = ask_bank_probabilities(len(banks_list))
    rows = build_dataset(rows_count, stores, banks_list, banks_probability, BANKS, selected_brand_groups, CARD_LENGTH)
    df = pd.DataFrame(rows)
    df.to_csv("dataset.csv", index=False)
    df.to_excel("dataset.xlsx", index=False)
    print(f"Готово: {len(df)} строк сохранено в dataset.csv и dataset.xlsx")
    print(f"Категорий: {df['category'].nunique()}, брендов: {df['brand'].nunique()} (уникальных названий)")
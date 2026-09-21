import pandas as pd
from core.dataset_builder import build_dataset


from data.banks import banks_list, banks_probability, BANKS, CARD_LENGTH
from data.categories_brands import categories, brand_groups
from data.stores import stores
 
MIN_ROWS = 50000
MAX_CARD_REPEAT = 5
MIN_PRODUCT_COUNT = 2
 
if __name__ == "__main__":
    rows = build_dataset(MIN_ROWS, stores, banks_list, banks_probability, BANKS, categories, brand_groups, CARD_LENGTH)
    df = pd.DataFrame(rows)
    df.to_csv("dataset.csv", index=False)
    print(f"Готово: {len(df)} строк сохранено в dataset.csv")
 
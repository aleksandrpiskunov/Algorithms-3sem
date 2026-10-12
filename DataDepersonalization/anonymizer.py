import pandas as pd
from kanon import required_k

# ===== Настройки силы обезличивания (крутите их, пока K не станет приемлемым) =====
COORD_DECIMALS = 0        # 2 ~ 1 км, 1 ~ 10 км, 0 ~ 100 км
DATE_LEVEL = "Y"          # "M" - месяц, "Q" - квартал, "Y" - год
PRICE_GROUPS = 5          # на сколько групп делить price и total (меньше групп = жёстче)


def mask_card(df):
    # 2204132696723478 -> ************3478
    s = df["card_number"].astype(str)
    df["card_number"] = "************" + s.str[-4:]
    return df


def drop_columns(df, cols):
    return df.drop(columns=cols)


def generalize_coords(df, decimals=2):
    df["lat"] = df["lat"].round(decimals)
    df["lon"] = df["lon"].round(decimals)
    return df


def generalize_datetime(df):
    df["date"] = df["datetime"].dt.to_period(DATE_LEVEL).astype(str)
    df["time_of_day"] = pd.cut(df["datetime"].dt.hour, bins=[-1, 5, 11, 17, 23],
                               labels=["ночь", "утро", "день", "вечер"])
    return df.drop(columns="datetime")


def microaggregate(df, col, k):
    # сортируем, режем на группы по k строк, заменяем значение средним группы
    order = df[col].sort_values().index
    groups = pd.Series(range(len(df)), index=order) // k
    last = groups.max()
    if (groups == last).sum() < k and last > 0:  # маленький хвост -> в предыдущую группу
        groups[groups == last] = last - 1
    df[col] = df[col].groupby(groups).transform("mean").round().astype(int)
    return df


def generalize_quantity(df):
    df["quantity"] = pd.cut(df["quantity"], bins=[0, 3, 100], labels=["1-3", "4+"])
    return df


def anonymize(df):
    k = required_k(len(df))                      # минимальный размер группы (пункт 8)
    size = max(k, len(df) // PRICE_GROUPS)       # размер группы микроагрегации
    df = df.copy()
    df = mask_card(df)
    df = drop_columns(df, ["receipt_number", "category", "brand"])
    df = generalize_coords(df, COORD_DECIMALS)
    df = generalize_datetime(df)
    df = microaggregate(df, "price", size)
    df = microaggregate(df, "total", size)
    df = generalize_quantity(df)
    return df
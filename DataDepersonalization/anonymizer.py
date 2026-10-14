import pandas as pd
from kanon import required_k, k_per_row
from hierarchy import STORE_GROUP, GROUP_SUPER

COORDS = 0          # знаков после запятой в lat / lon
DATE = "Y"          # уровень даты: "M" месяц, "Q" квартал, "Y" год
PRICE_GROUPS = 5   # на сколько групп делить price (внутри каждого типа магазина)
TOTAL_GROUPS = 2    # на сколько групп делить total (внутри каждого типа магазина)
STORE = 2           # магазин: 1 - тип магазина, 2 - крупная группа
CARD = 1            # сколько последних цифр карты оставлять
DELETE_MAX = 0.13   # строки с K < порога удаляем, только если их не больше 10% (0 - не удалять)

def mask_card(df, keep):
    # 2204132696723478 -> ***************8 (keep=1)
    tail = df["card_number"].astype(str).str[-keep:] if keep else ""
    df["card_number"] = "*" * (16 - keep) + tail
    return df


def generalize_store(df, level):
    # 1 - тип магазина, 2 - крупная группа; неизвестные названия -> "Прочее"
    df["store_name"] = df["store_name"].map(STORE_GROUP).fillna("Прочее")
    if level >= 2:
        df["store_name"] = df["store_name"].map(GROUP_SUPER).fillna("Прочее")
    return df


def round_col(df, col, decimals):
    df[col] = df[col].round(decimals)
    return df


def generalize_datetime(df, level):
    # datetime -> date (месяц / квартал / год) + time_of_day (день / вечер-ночь)
    df["date"] = df["datetime"].dt.to_period(level).astype(str)
    df["time_of_day"] = df["datetime"].dt.hour.between(6, 17).map({True: "день", False: "вечер/ночь"})
    return df.drop(columns="datetime")


def generalize_quantity(df):
    df["quantity"] = pd.cut(df["quantity"], bins=[0, 3, 100], labels=["1-3", "4+"])
    return df


def microaggregate(df, col, groups, by="store_name"):
    # внутри каждого магазина (или группы магазинов): сортируем, делим на `groups` групп
    # равного размера, значение заменяем средним по группе
    rank = df.groupby(by)[col].rank(method="first")
    size = df.groupby(by)[col].transform("size")
    part = ((rank - 1) * groups // size).astype(int)
    df[col] = df.groupby([by, part])[col].transform("mean").round().astype(int)
    return df


# построчные методы (порядок важен: магазин обобщается раньше, чем идёт микроагрегация)
ROW_METHODS = {
    "store_name": ("обобщение (магазин -> группа)", lambda df: generalize_store(df, STORE)),
    "card_number": (f"маскирование (остаётся цифр: {CARD})", lambda df: mask_card(df, CARD)),
    "lat": (f"обобщение (округление до {COORDS} зн.)", lambda df: round_col(df, "lat", COORDS)),
    "lon": (f"обобщение (округление до {COORDS} зн.)", lambda df: round_col(df, "lon", COORDS)),
    "datetime": (f"обобщение (дата: {DATE}, время суток: 2 части)", lambda df: generalize_datetime(df, DATE)),
    "quantity": ("обобщение (1-3 / 4+)", generalize_quantity),
    "receipt_number": ("удаление атрибута", lambda df: df.drop(columns="receipt_number")),
    "category": ("удаление атрибута", lambda df: df.drop(columns="category")),
    "brand": ("удаление атрибута", lambda df: df.drop(columns="brand")),
}
# методы агрегации: (описание, число групп)
AGG_METHODS = {
    "price": (f"микро-агрегация ({PRICE_GROUPS} групп)", PRICE_GROUPS),
    "total": (f"микро-агрегация ({TOTAL_GROUPS} групп)", TOTAL_GROUPS),
}
METHOD_TEXT = {**{c: m[0] for c, m in ROW_METHODS.items()}, **{c: m[0] for c, m in AGG_METHODS.items()}}


def anonymize(df, selected):
    df = df.copy()
    methods = {c: "не изменялся" for c in df.columns}

    for col, (text, func) in ROW_METHODS.items():
        if col in selected and col in df.columns:
            df = func(df)
            methods[col] = text

    aligned = df.copy()   # то же, но price/total ещё точные: для честного сравнения в метриках

    for col, (text, groups) in AGG_METHODS.items():
        if col in selected and col in df.columns:
            df = microaggregate(df, col, groups)
            methods[col] = text

    k = required_k(len(df))
    bad = k_per_row(df, list(df.columns)) < k
    share = float(bad.mean())
    reached = share <= DELETE_MAX
    result = df[~bad].reset_index(drop=True) if reached else df

    info = {"methods": methods, "aligned": aligned, "k": k, "reached": reached,
            "share": share, "deleted": len(df) - len(result)}
    return result, info
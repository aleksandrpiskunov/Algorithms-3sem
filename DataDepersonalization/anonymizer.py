import pandas as pd
from kanon import required_k, k_per_row
from hierarchy import STORE_GROUP, GROUP_SUPER

COORDS = 0      # знаков после запятой в координатах
DATE = "Y"      # уровень даты: "M" месяц, "Q" квартал, "Y" год
PRICE_GROUPS = 5   # на сколько групп делить price (внутри каждого типа магазина)
TOTAL_GROUPS = 2   # на сколько групп делить total (внутри каждого типа магазина)
STORE = 2       # магазин: 0 - название, 1 - тип магазина, 2 - крупная группа
CARD = 1        # сколько последних цифр карты оставлять (0 - скрыта полностью)
DELETE_MAX = 0.15   # удаляем строки, только если их не больше 10%


def mask_card(df, keep):
    # 2204132696723478 -> **************78 (keep=2); keep=0 -> карта скрыта полностью
    tail = df["card_number"].astype(str).str[-keep:] if keep else ""
    df["card_number"] = "*" * (16 - keep) + tail
    return df


def generalize_store(df, level):
    # 0 - название магазина, 1 - тип магазина, 2 - крупная группа
    if level >= 1:
        df["store_name"] = df["store_name"].map(STORE_GROUP).fillna("Прочее")
    if level >= 2:
        df["store_name"] = df["store_name"].map(GROUP_SUPER).fillna("Прочее")
    return df


def drop_columns(df, cols):
    return df.drop(columns=cols)


def generalize_coords(df, decimals):
    df["lat"] = df["lat"].round(decimals)
    df["lon"] = df["lon"].round(decimals)
    return df


def generalize_datetime(df, level):
    # level: "M" месяц, "Q" квартал, "Y" год
    df["date"] = df["datetime"].dt.to_period(level).astype(str)
    df["time_of_day"] = df["datetime"].dt.hour.between(6, 17).map({True: "день", False: "вечер/ночь"})
    return df.drop(columns="datetime")


def microaggregate(df, col, groups, by="store_name"):
    # внутри каждого типа магазина: сортируем, делим на `groups` групп равного размера,
    # значение заменяем средним по группе (так разброс внутри группы меньше, чем по всему набору)
    rank = df.groupby(by)[col].rank(method="first")
    size = df.groupby(by)[col].transform("size")
    part = ((rank - 1) * groups // size).astype(int)
    df[col] = df.groupby([by, part])[col].transform("mean").round().astype(int)
    return df


def generalize_quantity(df):
    df["quantity"] = pd.cut(df["quantity"], bins=[0, 3, 100], labels=["1-3", "4+"])
    return df


def generalize_all(df, coords, date, price_groups, total_groups, store, card):
    # все методы обезличивания с заданной силой обобщения
    df = df.copy()
    df = mask_card(df, card)
    df = generalize_store(df, store)
    df = drop_columns(df, ["receipt_number", "category", "brand"])
    df = generalize_coords(df, coords)
    df = generalize_datetime(df, date)
    df = microaggregate(df, "price", price_groups)
    df = microaggregate(df, "total", total_groups)
    df = generalize_quantity(df)
    return df


def anonymize(df):
    """Возвращает (обезличенный датасет, информация о настройках).
    Если строк с K < нужного не больше DELETE_MAX, они удаляются, и K >= нужного по ВСЕМ столбцам
    (значит и по любому набору квази-идентификаторов). Если больше, строки не удаляем (reached=False)."""
    k = required_k(len(df))
    g = generalize_all(df, COORDS, DATE, PRICE_GROUPS, TOTAL_GROUPS, STORE, CARD)
    bad = k_per_row(g, list(g.columns)) < k
    share = float(bad.mean())

    reached = share <= DELETE_MAX
    result = g[~bad].reset_index(drop=True) if reached else g

    info = {"coords": COORDS, "date": DATE, "price_groups": PRICE_GROUPS, "total_groups": TOTAL_GROUPS,
            "store": STORE, "card": CARD,
            "k": k, "reached": reached, "share": share, "deleted": len(df) - len(result)}
    return result, info
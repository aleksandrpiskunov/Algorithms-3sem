import pandas as pd
from kanon import required_k, k_per_row
from hierarchy import STORE_GROUP, GROUP_SUPER

# ===== Настройки (одно фиксированное, самое жёсткое обобщение) =====
COORDS = 0      # знаков после запятой в координатах
DATE = "Y"      # уровень даты: "M" месяц, "Q" квартал, "Y" год
GROUPS = 3      # на сколько групп делить price и total
STORE = 2       # магазин: 0 - название, 1 - тип магазина, 2 - крупная группа
CARD = 0        # сколько последних цифр карты оставлять (0 - скрыта полностью)
DELETE_MAX = 0.10   # удаляем строки, только если их не больше 10%


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


def generalize_all(df, k, coords, date, groups, store, card):
    # все методы обезличивания с заданной силой обобщения
    size = max(k, len(df) // groups)
    df = df.copy()
    df = mask_card(df, card)
    df = generalize_store(df, store)
    df = drop_columns(df, ["receipt_number", "category", "brand"])
    df = generalize_coords(df, coords)
    df = generalize_datetime(df, date)
    df = microaggregate(df, "price", size)
    df = microaggregate(df, "total", size)
    df = generalize_quantity(df)
    return df


def anonymize(df):
    """Возвращает (обезличенный датасет, информация о настройках).
    Если строк с K < нужного не больше DELETE_MAX, они удаляются, и K >= нужного по ВСЕМ столбцам
    (значит и по любому набору квази-идентификаторов). Если больше, строки не удаляем (reached=False)."""
    k = required_k(len(df))
    g = generalize_all(df, k, COORDS, DATE, GROUPS, STORE, CARD)
    bad = k_per_row(g, list(g.columns)) < k
    share = float(bad.mean())

    reached = share <= DELETE_MAX
    result = g[~bad].reset_index(drop=True) if reached else g

    info = {"coords": COORDS, "date": DATE, "groups": GROUPS, "store": STORE, "card": CARD,
            "k": k, "reached": reached, "share": share, "deleted": len(df) - len(result)}
    return result, info
import numpy as np
import pandas as pd


def kld(p, q, eps=1e-9):
    """Сама формула KLD(P|Q) = sum(P * log2(P / Q)).
    p, q - счётчики (или доли) по одним и тем же категориям/бинам.
    eps нужен, чтобы не получить log(0), если в обезличенном наборе значение пропало."""
    p = np.asarray(p, float) + eps
    q = np.asarray(q, float) + eps
    p /= p.sum()
    q /= q.sum()
    return float(np.sum(p * np.log2(p / q)))


def kld_column(orig, anon, bins=20):
    """KLD для одного столбца: готовит распределения и вызывает kld().
    Числа (price, total, lat, lon) - режем на одинаковые бины;
    всё остальное (brand, quantity, date...) - считаем частоты значений."""
    if pd.api.types.is_numeric_dtype(orig) and pd.api.types.is_numeric_dtype(anon):
        edges = np.histogram_bin_edges(np.concatenate([orig, anon]), bins=bins)
        return kld(np.histogram(orig, edges)[0], np.histogram(anon, edges)[0])
    p = orig.astype(str).value_counts()
    q = anon.astype(str).value_counts()
    cats = p.index.union(q.index)
    return kld(p.reindex(cats, fill_value=0), q.reindex(cats, fill_value=0))


def stats_compare(orig, anon, cols=("price", "total")):
    """Для исследования полезности: среднее, медиана и std числовых столбцов
    до и после. Показывает, насколько микроагрегация исказила данные."""
    rows = {(c, f): (getattr(orig[c], f)(), getattr(anon[c], f)())
            for c in cols for f in ("mean", "median", "std")}
    return pd.DataFrame(rows, index=["original", "anonymized"]).T
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
        anon = anon.dropna()  # подавленные значения (пустые) в гистограмму не берём
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


def field_metrics(orig, aligned, anon, methods):
    """Таблица по ВСЕМ полям исходного набора: метод, число уникальных значений до и после, KLD.
    aligned - оригинал, приведённый к тому же виду, что и результат (кроме price/total),
    поэтому для обобщённых полей KLD ~ 0, а потерю информации показывают уникальные значения."""
    rows = []
    for c in orig.columns:
        before = orig[c].nunique()
        if c in anon.columns:
            outs = [c]
        elif c == "datetime" and "date" in anon.columns:
            outs = ["date", "time_of_day"]
        else:
            outs = []
        if not outs:
            rows.append((c, methods[c], before, "-", "-"))
        for o in outs:
            rows.append((o, methods[c], before, anon[o].nunique(), f"{kld_column(aligned[o], anon[o]):.4f}"))
    return pd.DataFrame(rows, columns=["поле", "метод", "уник. до", "уник. после", "KLD"])


def table_text(df, left=2):
    """Таблица для моноширинного шрифта: первые `left` столбцов выровнены влево, остальные вправо,
    все столбцы строго друг под другом (в отличие от to_string, где текст выравнивается вправо)."""
    head = [str(c) for c in df.columns]
    rows = [[str(v) for v in r] for r in df.itertuples(index=False)]
    widths = [max([len(head[i])] + [len(r[i]) for r in rows]) for i in range(len(head))]

    def line(cells):
        return "  ".join(c.ljust(w) if i < left else c.rjust(w) for i, (c, w) in enumerate(zip(cells, widths)))

    return "\n".join([line(head), "  ".join("-" * w for w in widths)] + [line(r) for r in rows])
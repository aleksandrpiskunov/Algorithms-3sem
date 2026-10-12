def k_per_row(df, qi):
    # размер класса эквивалентности для каждой строки; K датасета = .min()
    return df.groupby(qi, dropna=False, observed=True)[qi[0]].transform("size")


def top_bad_k(df, qi, n=5):
    # n наименьших значений K: (K, число строк, % от всего датасета)
    counts = k_per_row(df, qi).value_counts().sort_index().head(n)
    return [(int(k), int(c), c / len(df) * 100) for k, c in counts.items()]


def unique_rows(df, qi):
    # строки с K=1
    return df[k_per_row(df, qi) == 1]


def required_k(n_rows):
    # приемлемый K по размеру набора
    if n_rows <= 51000:
        return 10
    if n_rows <= 105000:
        return 7
    return 5
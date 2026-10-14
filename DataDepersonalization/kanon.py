def k_per_row(df, qi):
    return df.groupby(qi, dropna=False, observed=True)[qi[0]].transform("size")


def top_bad_k(df, qi, n=5):
    counts = k_per_row(df, qi).value_counts().sort_index().head(n)
    return [(int(k), int(c), c / len(df) * 100) for k, c in counts.items()]


def unique_rows(df, qi):
    return df[k_per_row(df, qi) == 1]


def required_k(n_rows):
    if n_rows <= 51000:
        return 10
    if n_rows <= 105000:
        return 7
    return 5


def k_report(df, name):
    # K-anonymity по ВСЕМ полям любого датасета: K, вердикт, топ плохих K, уникальные строки
    qi = list(df.columns)
    k = int(k_per_row(df, qi).min())
    need = required_k(len(df))
    lines = [f"Датасет: {name}, строк: {len(df)}, полей: {len(qi)} (K по всем полям)",
             f"K = {k}, нужно >= {need}: {'приемлемо' if k >= need else 'НЕприемлемо'}",
             "", "Топ плохих K (доля строк):"]
    for kv, cnt, pct in top_bad_k(df, qi):
        lines.append(f"  {kv} ({pct:.2f}%)  строк: {cnt}")

    uniq = unique_rows(df, qi)
    lines.append(f"\nУникальных строк (K=1): {len(uniq)}")
    if k == 1:
        lines.append(uniq.head(50).to_string())
        if len(uniq) > 50:
            lines.append(f"... показаны первые 50 из {len(uniq)}")
    return lines
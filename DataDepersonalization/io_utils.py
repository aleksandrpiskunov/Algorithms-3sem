import pandas as pd


def split_coords(df):
    # "[59.927563, 30.360613] и 2025-03-27T20:25:00+03:00" -> lat, lon, datetime
    parts = df["Coords"].str.extract(r"\[(.+?), (.+?)\] и (.+)")
    df["lat"] = parts[0].astype(float)
    df["lon"] = parts[1].astype(float)
    df["datetime"] = pd.to_datetime(parts[2].str[:19], format="%Y-%m-%dT%H:%M:%S")  # везде +03:00, пояс отрезаем
    return df.drop(columns="Coords")


def load_dataset(path):
    # читаем файл из лабы 1 (xlsx или csv); Coords разбираем только в исходном файле
    if path.endswith(".csv"):
        df = pd.read_csv(path, dtype={"card_number": str})
    else:
        df = pd.read_excel(path, dtype={"card_number": str})
    if "Coords" in df.columns:
        df = split_coords(df)
    return df


def save_dataset(df, path):
    if path.endswith(".xlsx"):
        df.to_excel(path, index=False)
    else:
        df.to_csv(path, index=False, encoding="utf-8-sig")
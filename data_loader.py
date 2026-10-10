from pathlib import Path
import gdown
import pandas as pd


def load_data(url):
    """
    Загружает CSV-файл из Google Drive.
    На вход подается ссылка на файл
    На выходе возвращается DataFrame
    """
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    csv_path = gdown.download(
        url=url,
        output=str(data_dir / "credit.csv"),
        quiet=False
    )

    if csv_path is None:
        raise RuntimeError("Не удалось скачать датасет")

    df = pd.read_csv(csv_path)

    return df

def convert_types(df):
    """
    Приводит столбцы DataFrame к подходящим типам данных.
    На вход принимает DF
    """

    df = df.convert_dtypes()
    return df

def save_to_parquet(df, path):
    """
    Сохраняет DataFrame в формате Parquet.
    На вход принимает DF, path
    """
    df.to_parquet(path, index=False)

if __name__ == "__main__":

    url = "https://drive.google.com/file/d/1iQYkrgc5OhsaYX8vjvhIg2rsRqweMSFE/view?usp=drive_link"
    df = load_data(url)
    df = convert_types(df)

    print(df.head(10))
    print(df.dtypes)

    save_to_parquet(df, "data/credit.parquet")

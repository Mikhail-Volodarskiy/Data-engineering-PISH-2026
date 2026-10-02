import gdown
import pandas as pd


def load_data(url):
    """
    Загружает CSV-файл из Google Drive.
    На вход подается ссылка на файл
    На выходе возвращается DataFrame
    """

    gdown.download(
        url=url,
        output="data.csv",
        quiet=False
    )

    df = pd.read_csv("data.csv")
    print(df.head(10))
    return df

if __name__ == "__main__":
    url = "https://drive.google.com/file/d/1iQYkrgc5OhsaYX8vjvhIg2rsRqweMSFE/view?usp=drive_link"

    df = load_data(url)
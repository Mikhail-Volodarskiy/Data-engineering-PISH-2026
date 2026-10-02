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

    df = pd.read_csv(csv_path)
    return df

if __name__ == "__main__":
    url = "https://drive.google.com/file/d/1iQYkrgc5OhsaYX8vjvhIg2rsRqweMSFE/view?usp=drive_link"
    df = load_data(url)
    print(df.head(10))
from pathlib import Path
import gdown
import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_URL = "https://drive.google.com/file/d/1iQYkrgc5OhsaYX8vjvhIg2rsRqweMSFE/view?usp=drive_link"


def load_data(url: str = DATA_URL) -> pd.DataFrame:
    '''
    Загружает CSV-файл из Google Drive.
    На вход подается ссылка на файл
    На выходе возвращается DataFrame
    '''
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = DATA_DIR / "credit.csv"

    if not csv_path.exists():
        downloaded_path = gdown.download(
            url=url,
            output=str(csv_path),
            quiet=False
        )

        if downloaded_path is None:
            raise RuntimeError("Не удалось скачать датасет")

    df = pd.read_csv(csv_path)

    return df

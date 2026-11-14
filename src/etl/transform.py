from pathlib import Path
import pandas as pd


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Приводит столбцы DataFrame к подходящим типам данных.
    На вход принимает DF
    '''
    return df.convert_dtypes()


def save_to_parquet(df: pd.DataFrame, path: Path) -> pd.DataFrame:
    '''
    Сохраняет и возвращает DataFrame в формате Parquet
    На вход принимает DF, path
    '''
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(path, index=False)

    return df

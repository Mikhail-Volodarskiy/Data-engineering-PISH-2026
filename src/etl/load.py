import os
from functools import lru_cache
from pathlib import Path

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL


BASE_DIR = Path(__file__).resolve().parents[2]
TABLE_NAME = 'volodarskiymo'
MAX_ROWS = 100
TARGET_DB = 'homeworks'
load_dotenv(BASE_DIR / ".env")

@lru_cache
def get_engine() -> sqlalchemy.engine.base.Engine:
    '''
    Функция для подключения к БД
    '''
    db_url = URL.create(
        drivername='postgresql+psycopg2',
        username=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=int(os.environ['DB_PORT']),
        database=os.environ['DB_NAME']
    )
    remote_engine = create_engine(db_url)
    return remote_engine


def load_to_db(
        df: pd.DataFrame,
        limit: int = MAX_ROWS
) -> None:
    '''
    Функция принимает DF и количество строк для записи в БД
    '''
    if limit <= 0 or limit > MAX_ROWS:
        raise ValueError('Количество строк должно быть от 1 до 100')
    engine = get_engine()
    part_df = df.head(limit)
    with engine.begin() as conn:
        database = conn.execute(
            text('SELECT current_database()')
        ).scalar_one()

        if database != TARGET_DB:
            raise RuntimeError('Подключение не к homeworks')

        part_df.to_sql(
            name=TABLE_NAME,
            con=conn,
            if_exists="replace",
            index=False
        )


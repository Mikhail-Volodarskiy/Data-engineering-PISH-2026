import pandas as pd
import pandera.pandas as pa
from sqlalchemy import text
from .load import get_engine


def validation_raw(df: pd.DataFrame) -> None:
    '''
    На вход подается сырой DF для
    валидации: проверяется наличие DF,
    корректное число признаков,
    корректный тип данных числовых признаков
    '''
    if df.empty:
        raise ValueError('Датасет пустой')

    if df.shape[1] != 21:
        raise ValueError('Датасет имеет неверное число колонок')

    schema = pa.DataFrameSchema({
        'age': pa.Column(int),
        'amount': pa.Column(int),
        'months_loan_duration': pa.Column(int),
        'default': pa.Column(int)
    })

    schema.validate(df)


def validation_transformed(df: pd.DataFrame) -> None:
    '''
    На вход подается уже трансформированный DF
    валидация: проверяется наличие DF,
    корректное число признаков,
    Далее проверка диапазонов значений
    '''
    if df.empty:
        raise ValueError('Датасет пустой')

    if df.shape[1] != 21:
        raise ValueError('Датасет имеет неверное число колонок')

    schema = pa.DataFrameSchema({
        'default': pa.Column(int, pa.Check.isin([1, 2])),
        'months_loan_duration': pa.Column(int, pa.Check.gt(0)),
        'amount': pa.Column(int, pa.Check.gt(0)),
        'age': pa.Column(int, pa.Check.gt(0))
    })

    schema.validate(df)


def validation_load(
        table_name: str,
        rows: int
) -> None:
    engine = get_engine()
    with engine.connect() as conn:
        rows_count = conn.execute(
            text(f'SELECT COUNT(*) FROM {table_name}')
        ).scalar_one()

        if rows_count != rows:
            raise ValueError(f'В таблице {rows_count}, а ожидалось {rows}')

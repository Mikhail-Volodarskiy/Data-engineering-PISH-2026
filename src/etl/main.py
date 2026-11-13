from pathlib import Path

import click

from .extract import load_data
from .validation import validation_raw, validation_transformed, validation_load
from .transform import convert_types, save_to_parquet
from .load import load_to_db, TABLE_NAME

DATA_PATH = Path(__file__).resolve().parents[2] / 'data' / 'credit.parquet'

@click.command()
@click.option(
    '--limit',
    type=click.IntRange(1, 100),
    required=True,
    help='Количество строк для загрузки в БД (1-100)'
)


def main(limit: int) -> None:
    '''
    Запускает ETL-пайплайн
    :param limit: количество строк для загрузки в БД
    :return: None
    '''
    data = load_data()
    validation_raw(data)
    transformed_data = convert_types(data)
    validation_transformed(transformed_data)
    transformed_data = save_to_parquet(
        transformed_data,
        DATA_PATH
    )
    load_to_db(
        transformed_data,
       limit=limit
    )
    expected_rows = min(limit, len(transformed_data))
    validation_load(
        TABLE_NAME,
        rows=expected_rows,
    )
    print('ETL-пайплайн завершен')

if __name__ == '__main__':
    main()
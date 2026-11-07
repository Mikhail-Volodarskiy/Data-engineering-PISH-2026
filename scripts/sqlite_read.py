from pathlib import Path
from sqlalchemy import create_engine, inspect, text

#получаем путь к кредитам
BASE_DIR = Path(__file__).resolve().parent.parent
db_path = BASE_DIR / "data" / "creds.db"

#запускаем локально credits.db
engine = create_engine(f"sqlite:///{db_path.as_posix()}")

inspector = inspect(engine)
# Получаем названия таблиц
print("Таблицы:", inspector.get_table_names())
columns = inspector.get_columns("access")
for column in columns:
    print(column["name"], column["type"])

with engine.connect() as conn:
    result = conn.execute(
        text("""
            SELECT url, port, user, pass, db_name
            FROM access
            WHERE user = :username AND db_name = :database
        """),
        {"username": "student", "database": "freezone"}
    ).mappings().one()

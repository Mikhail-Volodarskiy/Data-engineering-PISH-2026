import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"]
)
remote_engine = create_engine(db_url)

with remote_engine.connect() as conn:
    result = conn.execute(
        text("SELECT current_database(), current_user")
    )
    print("Подключение:", result.fetchone())

df = pd.read_parquet(BASE_DIR / "data" / "credit.parquet")
df_100 = df.head(100)

with remote_engine.begin() as conn:
    database = conn.execute(
        text("SELECT current_database()")
    ).scalar_one()

    if database != "homeworks":
        raise RuntimeError("Подключение выполнено не к homeworks")

    df_100.to_sql(
        name="volodarskiymo",
        con=conn,
        if_exists="fail",
        index=False
    )

print(database)

with remote_engine.connect() as conn:
    count = conn.execute(
        text("SELECT COUNT(*) FROM volodarskiymo")
    ).scalar_one()

print(count)
import requests
import pandas as pd
from pathlib import Path

url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"

response = requests.get(url)
response.raise_for_status()

data = response.json()

securities = data["securities"]

df = pd.DataFrame(
    securities["data"],
    columns=securities["columns"]
)

print(df.head(20))

data_dir = Path(__file__).resolve().parent.parent / "data"
data_dir.mkdir(exist_ok=True)

df.to_parquet(data_dir / "moex_securities.parquet", index=False)

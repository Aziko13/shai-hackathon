import sqlite3
import pandas as pd
from pathlib import Path


sales_csv = Path("/Users/aziz/Documents/repos/shai-hackathon/data/sales_data.csv")
sku_csv = Path("/Users/aziz/Documents/repos/shai-hackathon/data/sku_reference.csv")
db_path = Path("/Users/aziz/Documents/repos/shai-hackathon/data/retail_demo.db")

sales_df = pd.read_csv(sales_csv, dtype={
    "date": str, "sku": str, "bill_id": str, "amount": float, "count": int
})
sku_df = pd.read_csv(sku_csv, dtype={"SKU": str, "NAME": str, "TYPE": str})

conn = sqlite3.connect(db_path)
cur = conn.cursor()


cur.execute("PRAGMA foreign_keys = ON;")

cur.execute("DROP TABLE IF EXISTS sales;")
cur.execute("DROP TABLE IF EXISTS sku_catalog;")

cur.execute("""
CREATE TABLE sku_catalog (
    sku  TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE sales (
    bill_id TEXT PRIMARY KEY,
    date    TEXT NOT NULL,   -- ISO YYYY-MM-DD
    sku     TEXT NOT NULL,
    amount  REAL NOT NULL,
    count   INTEGER NOT NULL,
    FOREIGN KEY (sku) REFERENCES sku_catalog(sku)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
""")

cur.executemany(
    "INSERT INTO sku_catalog (sku, name, type) VALUES (?, ?, ?);",
    list(
        sku_df.rename(columns={"SKU": "sku", "NAME": "name", "TYPE": "type"})
             .itertuples(index=False, name=None)
    )
)

cur.executemany(
    "INSERT INTO sales (bill_id, date, sku, amount, count) VALUES (?, ?, ?, ?, ?);",
    list(sales_df[["bill_id", "date", "sku", "amount", "count"]]
         .itertuples(index=False, name=None))
)

cur.execute("CREATE INDEX idx_sales_date ON sales(date);")
cur.execute("CREATE INDEX idx_sales_sku  ON sales(sku);")

conn.commit()


for row in cur.execute("""
    SELECT s.date, s.bill_id, s.sku, c.name, c.type, s.count, s.amount
    FROM sales s
    JOIN sku_catalog c ON s.sku = c.sku
    ORDER BY s.date
    LIMIT 5;
"""):
    print(row)

conn.close()
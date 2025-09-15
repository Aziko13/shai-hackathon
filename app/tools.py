from langchain.tools import tool
from datetime import datetime
import pandas as pd
from typing import Optional
import sys
import pandas as pd
import json, hashlib
import os
from app.artifacts import ARTIFACTS
from typing import List, Tuple, Optional

MAX_INLINE_ROWS = 10
STATIC_DIR = os.getenv("STATIC_DIR", "static")
CHARTS_DIR = os.path.join(STATIC_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

import os

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ["MPLBACKEND"] = "Agg"
import matplotlib

if "matplotlib.pyplot" in sys.modules:
    import matplotlib.pyplot as plt  # noqa

    try:
        plt.switch_backend("Agg")
    except Exception:
        pass
else:
    try:
        matplotlib.use("Agg", force=True)
    except Exception:
        pass

import matplotlib.pyplot as plt
import sqlite3

DB_NAME = os.getenv("DB_NAME", "retail_demo.db")

# DB_NAME = "retail_demo.db"

def get_db_conn():
    return sqlite3.connect(f"/Users/aziz/Documents/repos/shai-hackathon/data/{DB_NAME}")


def get_current_date() -> str:
    """Returns the current date in YYYY-MM-DD format."""
    print(" - TOOL CALL: get_current_date()")
    return "2025-09-14" # datetime.now().strftime("%Y-%m-%d")


def list_tables() -> List[str]:
    """Returns the names of all tables in the DB."""
    print(' - TOOL CALL: list_tables()')
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [t[0] for t in cursor.fetchall()]

def describe_table(table_name: str) -> List[tuple[str, str]]:
    """For a given table name returns its schema."""
    print(f' - TOOL CALL: describe_table({table_name})')
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        return [(col[1], col[2]) for col in cursor.fetchall()]


def execute_query(sql: str) -> List[list[str]]:
    """Executes an SQL query and returns the result."""
    print(f' - TOOL CALL: execute_query({sql})')

    conn = get_db_conn()
    df = pd.read_sql_query(sql, conn)
    handle = ARTIFACTS.put(df)

    stats = [
        f'Подробности: "handle {handle}"',
    ]
    preview = df.tail(20)

    return "".join(stats) + f"\n{preview}\n"



def give_column_summary(handle_id: str, col_name: str) -> str:
    """
    Returns a summary of the column in a dataframe.
    Args:
        handle_id: The id of the dataframe artifact.
        col_name: The name of the column to summarize.
    Returns:
        A summary of the column.
    """
    print(f' - TOOL CALL: give_column_summary({handle_id}, {col_name})')

    df = ARTIFACTS.get(handle_id)
    if col_name not in df.columns:
        return "Column not found"

    if df is None:
        return "DataFrame not found"

    summary = df[col_name].describe()

    return f"summary: {summary}"
    

def make_simple_plot(handle: str, x_col: str, y_col: str, x_vertical: str = None, title: str = "Plot", plot_type: str = "bar") -> str:
    """
    Returns a path to a bar/line plot of metric "y" by categories "x"
    Args:
        handle: str - artifact handle of the data to plot
        x_col: str - x column to plot
        y_col: str - y column to plot
        title: str - title of the plot
        plot_type: str - plot type, should be one of ["bar", "line"]
        x_vertical: str - x vertical line to plot, if plot_type is "line" then x_vertical is the date to plot. Can be used to highlight forecasts.
    Returns: 
        String with absolute path to saved PNG
    """
    out_dir = os.getenv("PLOTS_DIR", "data/plots")
    os.makedirs(out_dir, exist_ok=True)
    fname = f"{plot_type}_plot_{x_col}_{y_col}.png"
    path = os.path.join(out_dir, fname)

    df = ARTIFACTS.get(handle)
    if df is None or df.empty:
        return "Artifact not found or empty/expired."

    plt.figure(figsize=(8,5))
    df.plot(kind=plot_type, x=x_col, y=y_col, legend=False, color=plt.cm.Pastel1.colors)
    if x_vertical is not None:
        plt.axvline(x=x_vertical, color='red', linestyle='--')
    plt.ylabel(y_col)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    img_path = os.path.abspath(path)

    return f"Image path: {img_path}"




# def get_sales() -> str:
#     """Returns the sales data."""
#     print(" - TOOL CALL: get_sales()")
    
#     return "Sales are 3000"


# FAKE_SALES = pd.DataFrame([
#     {"date": "2025-09-01", "sku": "A101", "amount": 1000, "qty": 5},
#     {"date": "2025-09-01", "sku": "B202", "amount": 1500, "qty": 3},
#     {"date": "2025-09-02", "sku": "A101", "amount": 700, "qty": 4},
#     {"date": "2025-09-02", "sku": "C303", "amount": 1200, "qty": 6},
#     {"date": "2025-09-03", "sku": "B202", "amount": 900, "qty": 2},
#     {"date": "2025-09-04", "sku": "B202", "amount": 900, "qty": 2},
#     {"date": "2025-09-05", "sku": "B202", "amount": 900, "qty": 2},
#     {"date": "2025-09-06", "sku": "B202", "amount": 900, "qty": 2},
#     {"date": "2025-09-07", "sku": "B202", "amount": 900, "qty": 2},
#     {"date": "2025-09-08", "sku": "B202", "amount": 900, "qty": 2},
#     {"date": "2025-09-09", "sku": "B202", "amount": 900, "qty": 2},
# ])


# def get_sales(date_from: str, date_to: str, sku: Optional[str] = None) -> dict:
#     """
#     Returns total sales amount and quantity for a given date range.
#     Optionally filter by SKU code.
#     Args:
#         date_from: Start date (YYYY-MM-DD)
#         date_to: End date (YYYY-MM-DD)
#         sku: Optional SKU code to filter
#     Returns:
#         dict with total amount and quantity
#     """
#     print(f" - TOOL CALL: get_sales(date_from={date_from}, date_to={date_to}, sku={sku})")

#     df = FAKE_SALES.copy()

#     df["date"] = pd.to_datetime(df["date"])
#     mask = (df["date"] >= pd.to_datetime(date_from)) & (df["date"] <= pd.to_datetime(date_to))
#     df = df.loc[mask]

#     if sku:
#         df = df[df["sku"] == sku]

#     df = df.groupby("date").agg({"amount": "sum", "qty": "sum"}).reset_index()
#     handle = ARTIFACTS.put(df)

#     stats = [
#         f"Период: {date_from}—{date_to}.\n",
#         f'amount_sum: {df["amount"].sum()}\n',
#         f'qty_sum: {df["qty"].sum()}\n',
#         f'amount_max: {df["amount"].max()}\n',
#         f'qty_max: {df["qty"].max()}\n',
#         f'amount_min: {df["amount"].min()}\n',
#         f'qty_min: {df["qty"].min()}\n',
#         f'amount_avg: {df["amount"].mean()}\n',
#         f'qty_avg: {df["qty"].mean()}\n',
#         f'Подробности: "artifact id {handle}"',
#     ]

#     preview = df.tail(5)

#     return "".join(stats) + f"\n{preview}\n"



# def get_top_skus(date_from: str, date_to: str, top_n: int = 5) -> dict:
#     """
#     Returns top-N SKUs by sales amount and quantity for a given date range.
#     Args:
#         date_from: Start date (YYYY-MM-DD)
#         date_to: End date (YYYY-MM-DD)
#         top_n: Number of top SKUs to return (default 5)
#     Returns:
#         dict with top-N SKUs and aggregated metrics
#     """
#     print(f" - TOOL CALL: get_top_skus(date_from={date_from}, date_to={date_to}, top_n={top_n})")

#     df = FAKE_SALES.copy()
#     df["date"] = pd.to_datetime(df["date"])

#     mask = (df["date"] >= pd.to_datetime(date_from)) & (df["date"] <= pd.to_datetime(date_to))
#     df = df.loc[mask]

#     df_grouped = df.groupby("sku").agg({
#         "amount": "sum",
#         "qty": "sum"
#     }).reset_index()


#     df_sorted = df_grouped.sort_values(by="amount", ascending=False).head(top_n)

#     handle = ARTIFACTS.put(df_sorted)

#     stats = [
#         f"Период: {date_from}—{date_to}.\n",
#         f"Всего уникальных SKU: {df_grouped['sku'].nunique()}\n",
#         f"Топ-{top_n} по amount:\n",
#     ]
#     for _, row in df_sorted.iterrows():
#         stats.append(f"  SKU {row['sku']}: amount={row['amount']}, qty={row['qty']}\n")

#     stats.append(f'Подробности: "artifact id {handle}"')

#     preview = df_sorted.head(top_n)

#     return "".join(stats) + f"\n{preview}\n"

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

DB_PATH = os.getenv(
    "DB_PATH", "/Users/aziz/Documents/repos/shai-hackathon/data/data.db"
)


def get_db_conn():
    return sqlite3.connect(DB_PATH)


def get_current_date() -> str:
    """Returns the current date in YYYY-MM-DD format."""
    print(" - TOOL CALL: get_current_date()")
    return "2025-09-14"  # datetime.now().strftime("%Y-%m-%d")


def list_tables() -> List[str]:
    """Returns the names of all tables in the DB."""
    print(" - TOOL CALL: list_tables()")
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [t[0] for t in cursor.fetchall()]


def describe_table(table_name: str) -> List[tuple[str, str]]:
    """For a given table name returns its schema."""
    print(f" - TOOL CALL: describe_table({table_name})")
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        return [(col[1], col[2]) for col in cursor.fetchall()]


def execute_query(sql: str) -> List[list[str]]:
    """Executes an SQL query and returns the result."""
    print(f" - TOOL CALL: execute_query({sql})")

    conn = get_db_conn()
    df = pd.read_sql_query(sql, conn)
    handle = ARTIFACTS.put(df)

    stats = [
        f'Artifact id(handle): "{handle}"',
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
    print(f" - TOOL CALL: give_column_summary({handle_id}, {col_name})")

    df = ARTIFACTS.get(handle_id)
    if col_name not in df.columns:
        return "Column not found"

    if df is None:
        return "DataFrame not found"

    summary = df[col_name].describe()

    return f"summary: {summary}"


def make_simple_plot(
    handle: str,
    x_col: str,
    y_col: str,
    x_vertical: str = None,
    title: str = "Plot",
    plot_type: str = "bar",
) -> str:
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
    print(
        f" - TOOL CALL: make_simple_plot({handle}, {x_col}, {y_col}, {title}, {plot_type}, {x_vertical})"
    )
    out_dir = os.getenv("PLOTS_DIR", "data/plots")
    os.makedirs(out_dir, exist_ok=True)
    fname = f"{plot_type}_plot_{x_col}_{y_col}.png"
    path = os.path.join(out_dir, fname)

    df = ARTIFACTS.get(handle)
    if df is None or df.empty:
        return "Artifact not found or empty/expired."

    plt.figure(figsize=(8, 5))
    df.plot(kind=plot_type, x=x_col, y=y_col, legend=False, color=plt.cm.Pastel1.colors)
    if x_vertical is not None:
        plt.axvline(x=x_vertical, color="red", linestyle="--")
    plt.ylabel(y_col)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    img_path = os.path.abspath(path)

    return f"Image path: {img_path}"

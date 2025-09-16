req_1 = "Какие продажи были 5-го июня 2025?"
req_2 = "Сделай прогноз продаж на следующие 7 дней"
req_3 = "Покажи топ-3 продукта по суммам продаж за последнюю неделю"
req_4 = "Покажи топ-3 продукта по количеству продаж за последнюю неделю"

criteria_1 = """
• Assistant checks whether sales exist for the requested date using an SQL query.
• If no sales exist, assistant explicitly states there are no sales records for that date.
• If sales exist, assistant returns the total sales amount in KZT for that date.
• Assistant uses execute_query with valid SQLite3 syntax.
• Assistant’s answer matches the query results (no guessing).
"""

criteria_2 = """
• Assistant verifies table and column names before writing the query (e.g., using describe_table).
• Assistant prepares SQL returning two columns named dt and y for daily revenue.
• SQL groups by date and orders by date in ascending order using valid SQLite3 syntax.
• Assistant calls daily_forecast_from_db with days_horizont=7.
• Output contains forecast values for exactly 7 distinct future dates.
• Assistant provides a short insight describing the forecast trend (e.g., stable, increasing, seasonal).
"""

criteria_3 = """
• Assistant identifies current date.
• Assistant verifies schemas for needed db tables before querying.
• SQL covers one week period.
• SQL orders results by total revenue descending and limits to 3 rows.
• Assistant outputs both numeric results (in KZT) and a short insight (e.g., sales concentration, price-driven rankings).
"""

criteria_4 = """
• Assistant identifies current date.
• Assistant verifies schemas for needed db tables before querying.
• SQL covers one week of data.
• SQL orders results by quantity descending and limits to 3 rows.
• Assistant outputs both numeric results and a short insight.
"""


tool_req_1 = "Какие таблицы есть в БД?"
tool_req_2 = "Какая структуцра у таблицы с прогнозами?"
tool_req_3 = "Какая последняя дата с таблице с прогнозами?"
tool_req_4 = "Сделай прогноз на следующие 5 дней"


tool_call_1 = ["list_tables"]
tool_call_2 = ["list_tables", "describe_table"]
tool_call_3 = ["list_tables", "describe_table", "execute_query"]
tool_call_4 = [
    "get_current_date",
    "list_tables",
    "describe_table",
    "daily_forecast_from_db",
]


reqsuests = [
    req_1,
    req_2,
    req_3,
    req_4,
]

criterias = [
    criteria_1,
    criteria_2,
    criteria_3,
    criteria_4,
]


tool_requests = [
    tool_req_1,
    tool_req_2,
    tool_req_3,
    tool_req_4,
]

expected_tool_calls = [tool_call_1, tool_call_2, tool_call_3, tool_call_4]

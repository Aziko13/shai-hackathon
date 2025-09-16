req_1 = "Какие таблицы есть в базе данных?"
req_2 = "Покажи схему таблицы fact_sales"
req_3 = "Какая сегодня дата?"
req_4 = "Сколько всего записей в таблице fact_sales?"
req_5 = "Покажи первые 10 записей из таблицы fact_sales"
req_6 = "Какие колонки есть в таблице dict_store?"
req_7 = "Покажи уникальные значения в колонке store_id из таблицы dict_store"
req_8 = "Покажи схему таблицы fact_sales"
req_9 = "Какие колонки есть в таблице fact_sales?"
req_10 = "Покажи сколько всего sku-ов в базе данных?"
req_11 = "Сколько всего магазинов в базе данных?"
req_12 = "Максимальная и минимальная даты в таблице fact_sales?"
req_13 = "Продажи за последние 30 дней"
req_14 = "Дай график подневных продаж за последние 30 дней"
req_15 = "Покажи топ-3 продукта по выручке продаж за последнюю неделю"
req_16 = "Покажи топ-3 продукта по количеству продаж за последнюю неделю"
req_17 = "Дай график топ-5 продукта по выручке продаж за последнюю неделю"
req_18 = "Минимальная дата в таблице fact_sales?"
req_19 = "Максимальная дата в таблице fact_sales?"
req_20 = "Сколько записей в таблице fact_sales?"


criteria_1 = """
• Assistant uses list_tables tool to get table names.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_2 = """
• Assistant uses describe_table tool to get table schema.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_3 = """
• Assistant uses get_current_date tool to get current date.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_4 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_5 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant SQL query limits results to 10 rows.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_6 = """
• Assistant uses describe_table tool to get table schema.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_7 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant's answer based on the query results (no guessing).
"""

criteria_8 = """
• Assistant uses describe_table tool to get table schema.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_9 = """
• Assistant uses describe_table tool to get table schema.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_10 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_11 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant SQL query uses COUNT to count stores.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""

criteria_12 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant SQL query uses MAX/MIN to get dates.
• Assistant's answer based on the query results (no guessing).
• Assistant's answer is in Russian language.
"""


criteria_13 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant’s answer based on the query results (no guessing).
"""

criteria_14 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant uses make_simple_plot tool to create a plot and provide a proper artifact handle.
• Assistant’s answer based on the query results (no guessing).
• Assistant returns image path in the answer.
• The image path in the answer follows the format: IMAGES: ["<url_or_path_1>", "<url_or_path_2>", ...].
"""

criteria_15 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant SQL query orders results by total revenue descending and limits to 3 rows.
• Assistant’s answer matches the query results (no guessing).
• Assistant’s answer is in Russian language.
"""

criteria_16 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant SQL query orders results by total sales descending and limits to 3 rows.
• Assistant’s answer matches the query results (no guessing).
• Assistant’s answer is in Russian language.
"""

criteria_17 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant SQL query orders results by total sales descending and limits to 5 rows.
• Assistant uses make_simple_plot tool to create a plot and provide a proper artifact handle.
• Assistant’s answer matches the query results (no guessing).
• Assistant’s answer is in Russian language.
• Assistant returns image path in the answer.
• The image path in the answer follows the format: IMAGES: ["<url_or_path_1>", "<url_or_path_2>", ...].
"""

criteria_18 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant's answer based on the query results (no guessing).
"""

criteria_19 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant's answer based on the query results (no guessing).
"""

criteria_20 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant's answer based on the query results (no guessing).
"""

reqsuests = [
    req_1,
    req_2,
    req_3,
    req_4,
    req_5,
    req_6,
    req_7,
    req_8,
    req_9,
    req_10,
    req_11,
    req_12,
    req_13,
    req_14,
    req_15,
    req_16,
    req_17,
    req_18,
    req_19,
    req_20,
]

criterias = [
    criteria_1,
    criteria_2,
    criteria_3,
    criteria_4,
    criteria_5,
    criteria_6,
    criteria_7,
    criteria_8,
    criteria_9,
    criteria_10,
    criteria_11,
    criteria_12,
    criteria_13,
    criteria_14,
    criteria_15,
    criteria_16,
    criteria_17,
    criteria_18,
    criteria_19,
    criteria_20,
]

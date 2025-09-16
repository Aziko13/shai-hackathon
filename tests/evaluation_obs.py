req_1 = "Продажи за последние 30 дней"
req_2 = "Дай график подневных продаж за последние 30 дней"
req_3 = "Покажи топ-3 продукта по выручке продаж за последнюю неделю"
req_4 = "Покажи топ-3 продукта по количеству продаж за последнюю неделю"
req_5 = "Дай график топ-5 продукта по выручке продаж за последнюю неделю"


criteria_1 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant’s answer matches the query results (no guessing).
• Assistant’s answer is in Russian language.
"""

criteria_2 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant uses make_simple_plot tool to create a plot and provide a proper artifact handle.
• Assistant’s answer matches the query results (no guessing).
• Assistant’s answer is in Russian language.
• Assistant returns image path in the answer.
• The image path in the answer follows the format: IMAGES: ["<url_or_path_1>", "<url_or_path_2>", ...].
"""

criteria_3 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant SQL query orders results by total revenue descending and limits to 3 rows.
• Assistant’s answer matches the query results (no guessing).
• Assistant’s answer is in Russian language.
"""

criteria_4 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant SQL query orders results by total sales descending and limits to 3 rows.
• Assistant’s answer matches the query results (no guessing).
• Assistant’s answer is in Russian language.
"""

criteria_5 = """
• Assistant uses execute_query tool to execute the query.
• Assistant SQL query follows valid SQLite3 syntax.
• Assistant SQL query orders results by total sales descending and limits to 5 rows.
• Assistant uses make_simple_plot tool to create a plot and provide a proper artifact handle.
• Assistant’s answer matches the query results (no guessing).
• Assistant’s answer is in Russian language.
• Assistant returns image path in the answer.
• The image path in the answer follows the format: IMAGES: ["<url_or_path_1>", "<url_or_path_2>", ...].
"""

reqsuests = [
    req_1,
    req_2,
    req_3,
    req_4,
    req_5,
]

criterias = [
    criteria_1,
    criteria_2,
    criteria_3,
    criteria_4,
    criteria_5,
]

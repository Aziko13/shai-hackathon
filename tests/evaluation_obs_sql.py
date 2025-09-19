sql_req_1 = "Сколько всего магазинов в базе?"
sql_1 = "SELECT COUNT(*) FROM dict_store;"

sql_req_2 = "Сколько всего товаров в базе?"
sql_2 = "SELECT COUNT(*) AS total_sku FROM dict_sku;"

sql_req_3 = "Покажи минимальную и максимальную дату продаж"
sql_3 = "SELECT MIN(order_date) AS min_date, MAX(order_date) AS max_date FROM fact_sales;"

sql_req_4 = "Покажи первые 10 записей из таблицы fact_bal"
sql_4 = "SELECT * FROM fact_bal LIMIT 10;"

sql_req_5 = "Сколько всего чеков в fact_sales?"
sql_5 = "SELECT COUNT(DISTINCT order_id) AS total_orders FROM fact_sales;"

sql_req_6 = "Покажи общую сумму продаж в тенге за все время"
sql_6 = "SELECT SUM(sales_tg) AS total_revenue FROM fact_sales;"

sql_req_7 = "Покажи количество продаж в штуках по каждому магазину"
sql_7 = "SELECT store_id, SUM(sales_unit) AS total_units FROM fact_sales GROUP BY store_id;"

sql_req_8 = "Покажи топ-5 товаров по выручке"
sql_8 = """
SELECT sku_id, SUM(sales_tg) AS total_revenue
FROM fact_sales
GROUP BY sku_id
ORDER BY total_revenue DESC
LIMIT 5;
"""

sql_req_9 = "Покажи названия магазинов и их общую выручку"
sql_9 = """
SELECT ds.store_name, SUM(fs.sales_tg) AS total_revenue
FROM fact_sales fs
JOIN dict_store ds ON fs.store_id = ds.store_id
GROUP BY ds.store_name;
"""

sql_req_10 = "Покажи закупочную цену по каждому товару в каждом магазине"
sql_10 = "SELECT store_id, sku_id, cost FROM fact_cost;"

sql_reqsuests = [
    sql_req_1,
    sql_req_2,
    sql_req_3,
    sql_req_4,
    sql_req_5,
    sql_req_6,
    sql_req_7,
    sql_req_8,
    sql_req_9,
    sql_req_10,
]               

sql_answers = [
    sql_1,
    sql_2,
    sql_3,
    sql_4,
    sql_5,
    sql_6,
    sql_7,
    sql_8,
    sql_9,
    sql_10
]
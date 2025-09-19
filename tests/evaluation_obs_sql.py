sql_req_1 = "Сколько всего магазинов в базе?"
sql_1 = "SELECT COUNT(*) FROM dict_store;"

sql_req_2 = "Сколько всего чеков в fact_sales?"
sql_2 = "SELECT COUNT(DISTINCT order_id) AS total_orders FROM fact_sales;"

sql_req_3 = "Сколько всего товаров в базе?"
sql_3 = "SELECT COUNT(DISTINCT sku_id) AS total_products FROM dict_sku;"

sql_req_4 = "Покажи минимальную и максимальную дату продаж"
sql_4 = "SELECT MIN(order_date) AS min_date, MAX(order_date) AS max_date FROM fact_sales;"

sql_req_5 = "Покажи первые 10 записей из таблицы fact_bal"
sql_5 = "SELECT * FROM fact_bal LIMIT 10;"

sql_req_6 = "Покажи общую сумму продаж в тенге за все время"
sql_6 = "SELECT SUM(sales_tg) AS total_revenue FROM fact_sales;"

sql_req_7 = "Покажи количество продаж в штуках по каждому магазину"
sql_7 = """
SELECT 
    fs.store_id,
    ds.store_name,
    SUM(fs.sales_unit) AS total_sales_units
FROM fact_sales fs
JOIN dict_store ds ON fs.store_id = ds.store_id
GROUP BY fs.store_id, ds.store_name;
"""

sql_req_8 = "Покажи топ-5 товаров по выручке"
sql_8 = """
SELECT 
    fs.sku_id,
    sk.sku_name,
    SUM(fs.sales_tg) AS revenue
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
GROUP BY fs.sku_id, sk.sku_name
ORDER BY revenue DESC
LIMIT 5;
"""

sql_req_9 = "Покажи названия магазинов и их общую выручку"
sql_9 = """
SELECT 
    ds.store_id,
    ds.store_name,
    SUM(fs.sales_tg) AS total_revenue
FROM fact_sales fs
JOIN dict_store ds ON fs.store_id = ds.store_id
GROUP BY ds.store_id, ds.store_name
ORDER BY total_revenue DESC;
"""

sql_req_10 = "Покажи закупочную цену по каждому товару в каждом магазине"
sql_10 = """
SELECT 
    ds.store_id,
    ds.store_name,
    sk.sku_id,
    sk.sku_name,
    fc.cost AS purchase_price
FROM fact_cost fc
JOIN dict_store ds ON fc.store_id = ds.store_id
JOIN dict_sku sk ON fc.sku_id = sk.sku_id
ORDER BY ds.store_id, sk.sku_id;
"""

sql_req_11 = "Покажи остатки по каждому товару в каждом магазине на последнюю дату"
sql_11 = """
SELECT 
    ds.store_id,
    ds.store_name,
    sk.sku_id,
    sk.sku_name,
    fb.rep_date,
    fb.quantity_warehouse
FROM fact_bal fb
JOIN dict_store ds ON fb.store_id = ds.store_id
JOIN dict_sku sk ON fb.sku_id = sk.sku_id
WHERE fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
ORDER BY ds.store_id, sk.sku_id;
"""

sql_req_12 = "Сколько всего товаров по категории Чай и кофе?"
sql_12 = """
SELECT COUNT(DISTINCT sk.sku_id) AS total_sku
FROM dict_sku sk
WHERE LOWER(TRIM(sk.level2_name)) = LOWER(TRIM('Чай и кофе'));
"""

sql_req_13 = "Покажи все товары из категории БЕЗАЛКОГОЛЬНЫЕ НАПИТКИ"
sql_13 = """
SELECT 
    sk.sku_id,
    sk.sku_name,
    sk.level2_id,
    sk.level2_name
FROM dict_sku sk
WHERE LOWER(TRIM(sk.level2_name)) = LOWER(TRIM('БЕЗАЛКОГОЛЬНЫЕ НАПИТКИ'));
"""

sql_req_14 = "Покажи все товары из категории МОЛОЧНЫЕ ПРОДУКТЫ"
sql_14 = """
SELECT 
    sk.sku_id,
    sk.sku_name,
    sk.level2_id,
    sk.level2_name
FROM dict_sku sk
WHERE LOWER(TRIM(sk.level2_name)) = LOWER(TRIM('МОЛОЧНЫЕ ПРОДУКТЫ'));
"""

sql_req_15 = "Найди все товары бренда Orbit"
sql_15 = """
SELECT 
    sk.sku_id,
    sk.sku_name,
    sk.level2_id,
    sk.level2_name
FROM dict_sku sk
WHERE LOWER(TRIM(sk.sku_name)) LIKE '%orbit%';
"""

sql_req_16 = "Найди все товары бренда Tassay"
sql_16 = """
SELECT 
    sk.sku_id,
    sk.sku_name,
    sk.level2_id,
    sk.level2_name
FROM dict_sku sk
WHERE LOWER(TRIM(sk.sku_name)) LIKE '%tassay%';
"""

sql_req_17 = "Сколько уникальных категорий товаров есть в справочнике?"
sql_17 = "SELECT COUNT(DISTINCT sk.level2_id) AS unique_category_count FROM dict_sku sk;"

sql_req_18 = "Сколько товаров относится к категории КОНДИТЕРСКИЕ ИЗДЕЛИЯ?"
sql_18 = """
SELECT COUNT(DISTINCT sk.sku_id) AS product_count
FROM dict_sku sk
WHERE LOWER(TRIM(sk.level2_name)) = LOWER(TRIM('КОНДИТЕРСКИЕ ИЗДЕЛИЯ'));
"""

sql_req_19 = "Сколько товаров относится к каждой категории второго уровня?"
sql_19 = """
SELECT 
    sk.level2_id,
    sk.level2_name,
    COUNT(DISTINCT sk.sku_id) AS total_sku
FROM dict_sku sk
GROUP BY sk.level2_id, sk.level2_name
ORDER BY total_sku DESC;
"""

sql_req_20 = "В какой категории второго уровня больше всего товаров?"
sql_20 = """
SELECT 
    sk.level2_id,
    sk.level2_name,
    COUNT(DISTINCT sk.sku_id) AS total_sku
FROM dict_sku sk
GROUP BY sk.level2_id, sk.level2_name
ORDER BY total_sku DESC
LIMIT 1;
"""

sql_req_21 = "Найди все товары бренда Coca-Cola"
sql_21 = """
SELECT 
    sk.sku_id,
    sk.sku_name,
    sk.level2_id,
    sk.level2_name
FROM dict_sku sk
WHERE LOWER(TRIM(sk.sku_name)) LIKE '%coca-cola%';
"""

sql_req_22 = "Найди все товары бренда Lipton"
sql_22 = """
SELECT 
    sk.sku_id,
    sk.sku_name,
    sk.level2_id,
    sk.level2_name
FROM dict_sku sk
WHERE LOWER(TRIM(sk.sku_name)) LIKE '%lipton%';
"""

sql_req_23 = "Покажи все товары, название которых начинается на ВОДА"
sql_23 = """
SELECT 
    sk.sku_id,
    sk.sku_name,
    sk.level2_id,
    sk.level2_name
FROM dict_sku sk
WHERE LOWER(TRIM(sk.sku_name)) LIKE 'вода%';
"""

sql_req_24 = "Сколько товаров из категории Напитки принадлежит бренду Pepsi?"
sql_24 = """
SELECT COUNT(DISTINCT sk.sku_id) AS total_sku
FROM dict_sku sk
WHERE LOWER(TRIM(sk.level2_name)) = 'напитки'
  AND LOWER(TRIM(sk.sku_name)) LIKE '%pepsi%';
"""

sql_req_25 = "В каких категориях встречается бренд Nestlé?"
sql_25 = """
SELECT 
    sk.level2_id,
    sk.level2_name,
    COUNT(DISTINCT sk.sku_id) AS total_sku
FROM dict_sku sk
WHERE LOWER(TRIM(sk.sku_name)) LIKE '%nestlé%'
   OR LOWER(TRIM(sk.sku_name)) LIKE '%nestle%'
GROUP BY sk.level2_id, sk.level2_name;
"""

sql_req_26 = "Покажи остатки товара Coca-Cola 0.5л в каждом магазине"
sql_26 = """
SELECT 
    fb.store_id,
    ds.store_name,
    fb.sku_id,
    sk.sku_name,
    fb.quantity_warehouse
FROM fact_bal fb
JOIN dict_store ds ON fb.store_id = ds.store_id
JOIN dict_sku sk ON fb.sku_id = sk.sku_id
WHERE fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
  AND LOWER(TRIM(sk.sku_name)) = 'coca-cola 0.5л';
"""

sql_req_27 = "Найди товары, у которых остаток равен нулю"
sql_27 = """
SELECT 
    fb.store_id,
    ds.store_name,
    fb.sku_id,
    sk.sku_name,
    fb.quantity_warehouse
FROM fact_bal fb
JOIN dict_store ds ON fb.store_id = ds.store_id
JOIN dict_sku sk ON fb.sku_id = sk.sku_id
WHERE fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
  AND fb.quantity_warehouse = 0;
"""

sql_req_28 = "Покажи все товары, остатки которых превышают 1000 единиц"
sql_28 = """
SELECT 
    fb.store_id,
    ds.store_name,
    fb.sku_id,
    sk.sku_name,
    fb.quantity_warehouse
FROM fact_bal fb
JOIN dict_store ds ON fb.store_id = ds.store_id
JOIN dict_sku sk ON fb.sku_id = sk.sku_id
WHERE fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
  AND fb.quantity_warehouse > 1000;
"""

sql_req_29 = "Сколько уникальных товаров имеют остатки меньше 10 единиц?"
sql_29 = """
SELECT COUNT(DISTINCT fb.sku_id) AS total_sku
FROM fact_bal fb
WHERE fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
  AND fb.quantity_warehouse < 10;
"""

sql_req_30 = "Найди топ-5 товаров с наибольшими остатками в магазине АФ10"
sql_30 = """
SELECT 
    fb.sku_id,
    sk.sku_name,
    fb.store_id,
    ds.store_name,
    fb.quantity_warehouse
FROM fact_bal fb
JOIN dict_store ds ON fb.store_id = ds.store_id
JOIN dict_sku sk ON fb.sku_id = sk.sku_id
WHERE fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
  AND LOWER(TRIM(ds.store_name)) = 'аф10'
ORDER BY fb.quantity_warehouse DESC
LIMIT 5;
"""

sql_req_31 = "Сколько всего товаров категории Молочные продукты хранится на складах сети?"
sql_31 = """
SELECT SUM(fb.quantity_warehouse) AS total_quantity
FROM fact_bal fb
JOIN dict_sku sk ON fb.sku_id = sk.sku_id
WHERE fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
  AND LOWER(TRIM(sk.level2_name)) = 'молочные продукты';
"""

sql_req_32 = "Покажи топ-10 категорий с наибольшими остатками"
sql_32 = """
SELECT 
    sk.level2_id,
    sk.level2_name,
    SUM(fb.quantity_warehouse) AS total_quantity
FROM fact_bal fb
JOIN dict_sku sk ON fb.sku_id = sk.sku_id
WHERE fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
GROUP BY sk.level2_id, sk.level2_name
ORDER BY total_quantity DESC
LIMIT 10;
"""

sql_req_33 = "Покажи прибыль по каждому товару в магазине АФ10"
sql_33 = """
SELECT 
    fs.sku_id,
    sk.sku_name,
    fs.store_id,
    ds.store_name,
    SUM(fs.sales_tg - fc.cost * fs.sales_unit) AS profit
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
JOIN dict_store ds ON fs.store_id = ds.store_id
JOIN fact_cost fc ON fs.sku_id = fc.sku_id AND fs.store_id = fc.store_id
WHERE LOWER(TRIM(ds.store_name)) = 'аф10'
GROUP BY fs.sku_id, sk.sku_name, fs.store_id, ds.store_name
ORDER BY profit DESC;
"""

sql_req_34 = "Какая категория товаров приносит наибольшую прибыль?"
sql_34 = """
SELECT 
    sk.level2_id,
    sk.level2_name,
    SUM(fs.sales_tg - fc.cost * fs.sales_unit) AS total_profit
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
JOIN fact_cost fc ON fs.sku_id = fc.sku_id AND fs.store_id = fc.store_id
GROUP BY sk.level2_id, sk.level2_name
ORDER BY total_profit DESC
LIMIT 1;
"""

sql_req_35 = "Найди топ-10 товаров по прибыли за сентябрь"
sql_35 = """
SELECT 
    fs.sku_id,
    sk.sku_name,
    SUM(fs.sales_tg - fc.cost * fs.sales_unit) AS profit
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
JOIN fact_cost fc ON fs.sku_id = fc.sku_id AND fs.store_id = fc.store_id
WHERE strftime('%Y-%m', fs.order_date) = '2025-09'
GROUP BY fs.sku_id, sk.sku_name
ORDER BY profit DESC
LIMIT 10;
"""

sql_req_36 = "Какие товары оказались убыточными (revenue < cost)?"
sql_36 = """
SELECT 
    fs.sku_id,
    sk.sku_name,
    SUM(fs.sales_tg - fc.cost * fs.sales_unit) AS profit
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
JOIN fact_cost fc ON fs.sku_id = fc.sku_id AND fs.store_id = fc.store_id
GROUP BY fs.sku_id, sk.sku_name
HAVING profit < 0
ORDER BY profit ASC;
"""

sql_req_37 = "Какие товары дали максимальную маржу в процентах (profit / revenue)?"
sql_37 = """
SELECT 
    fs.sku_id,
    sk.sku_name,
    SUM(fs.sales_tg - fc.cost * fs.sales_unit) * 1.0 / SUM(fs.sales_tg) AS margin_pct
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
JOIN fact_cost fc ON fs.sku_id = fc.sku_id AND fs.store_id = fc.store_id
GROUP BY fs.sku_id, sk.sku_name
ORDER BY margin_pct DESC
LIMIT 10;
"""

sql_req_38 = "Покажи среднюю наценку по каждому товару"
sql_38 = """
SELECT 
    fs.sku_id,
    sk.sku_name,
    AVG((fs.sales_tg / fs.sales_unit - fc.cost) / fc.cost * 100.0) AS avg_markup_pct
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
JOIN fact_cost fc ON fs.sku_id = fc.sku_id AND fs.store_id = fc.store_id
GROUP BY fs.sku_id, sk.sku_name
ORDER BY avg_markup_pct DESC;
"""

sql_req_39 = "Какая категория товаров имеет наибольшую наценку?"
sql_39 = """
SELECT 
    sk.level2_id,
    sk.level2_name,
    AVG((fs.sales_tg / fs.sales_unit - fc.cost) / fc.cost * 100.0) AS avg_markup_pct
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
JOIN fact_cost fc ON fs.sku_id = fc.sku_id AND fs.store_id = fc.store_id
GROUP BY sk.level2_id, sk.level2_name
ORDER BY avg_markup_pct DESC
LIMIT 1;
"""

sql_req_40 = "Найди топ-10 товаров с максимальной наценкой"
sql_40 = """
SELECT 
    fs.sku_id,
    sk.sku_name,
    AVG((fs.sales_tg / fs.sales_unit - fc.cost) / fc.cost * 100.0) AS avg_markup_pct
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
JOIN fact_cost fc ON fs.sku_id = fc.sku_id AND fs.store_id = fc.store_id
GROUP BY fs.sku_id, sk.sku_name
ORDER BY avg_markup_pct DESC
LIMIT 10;
"""

sql_req_41 = "Какие категории имеют наценку выше 50%?"
sql_41 = """
SELECT 
    sk.level2_id,
    sk.level2_name,
    AVG((fs.sales_tg / fs.sales_unit - fc.cost) / fc.cost * 100.0) AS avg_markup_pct
FROM fact_sales fs
JOIN dict_sku sk ON fs.sku_id = sk.sku_id
JOIN fact_cost fc ON fs.sku_id = fc.sku_id AND fs.store_id = fc.store_id
GROUP BY sk.level2_id, sk.level2_name
HAVING AVG((fs.sales_tg / fs.sales_unit - fc.cost) / fc.cost * 100.0) > 50
ORDER BY avg_markup_pct DESC;
"""

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
    sql_req_11,
    sql_req_12,
    sql_req_13,
    sql_req_14,
    sql_req_15,
    sql_req_16,
    sql_req_17,
    sql_req_18,
    sql_req_19,
    sql_req_20,
    sql_req_21,
    sql_req_22,
    sql_req_23,
    sql_req_24,
    sql_req_25,
    sql_req_26,
    sql_req_27,
    sql_req_28,
    sql_req_29,
    sql_req_30,
    sql_req_31,
    sql_req_32,
    sql_req_33,
    sql_req_34,
    sql_req_35,
    sql_req_36,
    sql_req_37,
    sql_req_38,
    sql_req_39,
    sql_req_40,
    sql_req_41
]

sql_answers = [sql_1, sql_2, sql_3, sql_4, sql_5, sql_6, sql_7, sql_8, sql_9, sql_10, sql_11, sql_12, sql_13, sql_14, sql_15, sql_16, sql_17, sql_18, sql_19, sql_20, sql_21, sql_22, sql_23, sql_24, sql_25, sql_26, sql_27, sql_28, sql_29, sql_30, sql_31, sql_32, sql_33, sql_34, sql_35, sql_36, sql_37, sql_38, sql_39, sql_40, sql_41]

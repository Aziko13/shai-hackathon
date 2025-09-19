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

sql_req_11 = "Покажи остатки по каждому товару в каждом магазине на последнюю дату"
sql_11 = """
SELECT store_id, sku_id, quantity_warehouse
FROM fact_bal
WHERE rep_date = (SELECT MAX(rep_date) FROM fact_bal);
"""

sql_req_12 = "Сколько всего товаров по категории Чай и кофе?"
sql_12 = """
SELECT COUNT(*)
FROM dict_sku
WHERE LOWER(category) = LOWER('Чай и кофе');
"""

sql_req_13 = "Покажи все товары из категории БЕЗАЛКОГОЛЬНЫЕ НАПИТКИ"
sql_13 = """
SELECT *
FROM dict_sku
WHERE LOWER(category) = LOWER('БЕЗАЛКОГОЛЬНЫЕ НАПИТКИ');
"""

sql_req_14 = "Покажи все товары из категории МОЛОЧНЫЕ ПРОДУКТЫ"
sql_14 = """
SELECT *
FROM dict_sku
WHERE LOWER(category) = LOWER('МОЛОЧНЫЕ ПРОДУКТЫ');
"""

sql_req_15 = "Найди все товары бренда Orbit"
sql_15 = """
SELECT *
FROM dict_sku
WHERE LOWER(brand) = LOWER('Orbit');
"""

sql_req_16 = "Найди все товары бренда Tassay"
sql_16 = """
SELECT *
FROM dict_sku
WHERE LOWER(brand) = LOWER('Tassay');
"""

sql_req_17 = "Сколько уникальных категорий товаров есть в справочнике?"
sql_17 = """
SELECT COUNT(DISTINCT LOWER(category)) AS unique_categories
FROM dict_sku;
"""             

sql_req_18 = "Сколько товаров относится к категории КОНДИТЕРСКИЕ ИЗДЕЛИЯ?"
sql_18 = """
SELECT COUNT(*)
FROM dict_sku
WHERE LOWER(category) = LOWER('КОНДИТЕРСКИЕ ИЗДЕЛИЯ');
"""

sql_req_19 = "Найди все товары, в названии которых встречается слово шоколад"
sql_19 = """
SELECT *
FROM dict_sku
WHERE LOWER(name) LIKE LOWER('%шоколад%');
"""

sql_req_20 = "Сколько уникальных брендов содержится в справочнике?"
sql_20 = """
SELECT COUNT(DISTINCT LOWER(brand)) AS unique_brands
FROM dict_sku;
"""

sql_req_21 = "Сколько товаров относится к каждой категории второго уровня?"
sql_21 = """
SELECT LOWER(category_level2) AS category_level2, COUNT(*) AS product_count
FROM dict_sku
GROUP BY LOWER(category_level2);
"""

sql_req_22 = "В какой категории второго уровня больше всего товаров?"
sql_22 = """
SELECT LOWER(category_level2) AS category_level2, COUNT(*) AS product_count
FROM dict_sku
GROUP BY LOWER(category_level2)
ORDER BY product_count DESC
LIMIT 1;
"""

sql_req_23 = "Найди все товары бренда Coca-Cola"
sql_23 = """
SELECT *
FROM dict_sku
WHERE LOWER(brand) = LOWER('Coca-Cola');
"""     

sql_req_24 = "Найди все товары бренда Lipton"
sql_24 = """
SELECT *
FROM dict_sku
WHERE LOWER(brand) = LOWER('Lipton');
"""

sql_req_25 = "Покажи все товары, название которых начинается на ВОДА"
sql_25 = """
SELECT *
FROM dict_sku
WHERE LOWER(name) LIKE LOWER('вода%');
"""

sql_req_26 = "Сколько товаров из категории Напитки принадлежит бренду Pepsi?"
sql_26 = """
SELECT COUNT(*)
FROM dict_sku
WHERE LOWER(category) = LOWER('Напитки')
  AND LOWER(brand) = LOWER('Pepsi');
"""

sql_req_27 = "В каких категориях встречается бренд Nestlé?"
sql_27 = """
SELECT DISTINCT LOWER(category) AS category
FROM dict_sku
WHERE LOWER(brand) = LOWER('Nestlé');
"""

sql_req_28 = "Покажи остатки товара Coca-Cola 0.5л в каждом магазине"
sql_28 = """
SELECT fb.store_id, fb.sku_id, fb.quantity_warehouse
FROM fact_bal fb
JOIN dict_sku ds ON fb.sku_id = ds.sku_id
WHERE LOWER(ds.name) = LOWER('Coca-Cola 0.5л')
  AND fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal);
"""

sql_req_29 = "Найди товары, у которых остаток равен нулю"
sql_29 = """
SELECT fb.store_id, fb.sku_id, fb.quantity_warehouse
FROM fact_bal fb
WHERE fb.quantity_warehouse = 0
  AND fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal);
"""     

sql_req_30 = "Покажи все товары, остатки которых превышают 1000 единиц"
sql_30 = """
SELECT fb.store_id, fb.sku_id, fb.quantity_warehouse
FROM fact_bal fb
WHERE fb.quantity_warehouse > 1000
  AND fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal);
"""

sql_req_31 = "Сколько уникальных товаров имеют остатки меньше 10 единиц?"
sql_31 = """
SELECT COUNT(DISTINCT fb.sku_id)
FROM fact_bal fb
WHERE fb.quantity_warehouse < 10
  AND fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal);
"""

sql_req_32 = "Найди топ-5 товаров с наибольшими остатками в магазине АФ10"
sql_32 = """
SELECT fb.sku_id, ds.name, fb.quantity_warehouse
FROM fact_bal fb
JOIN dict_sku ds ON fb.sku_id = ds.sku_id
WHERE fb.store_id = 'АФ10'
  AND fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
ORDER BY fb.quantity_warehouse DESC
LIMIT 5;
"""

sql_req_33 = "Какие товары полностью закончились на 2025-09-05?"
sql_33 = """
SELECT fb.store_id, fb.sku_id, ds.name
FROM fact_bal fb
JOIN dict_sku ds ON fb.sku_id = ds.sku_id
WHERE fb.quantity_warehouse = 0
  AND fb.rep_date = '2025-09-05';
"""

sql_req_34 = "Сколько всего товаров категории Молочные продукты хранится на складах сети?"
sql_34 = """
SELECT SUM(fb.quantity_warehouse) AS total_qty
FROM fact_bal fb
JOIN dict_sku ds ON fb.sku_id = ds.sku_id
WHERE LOWER(ds.category) = LOWER('Молочные продукты')
  AND fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal);
"""

sql_req_35 = "Покажи топ-10 категорий с наибольшими остатками"
sql_35 = """
SELECT LOWER(ds.category) AS category, SUM(fb.quantity_warehouse) AS total_qty
FROM fact_bal fb
JOIN dict_sku ds ON fb.sku_id = ds.sku_id
WHERE fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal)
GROUP BY LOWER(ds.category)
ORDER BY total_qty DESC
LIMIT 10;
"""         

sql_req_36 = "Какие товары имеют самую высокую закупочную цену?"
sql_36 = """
SELECT ds.sku_id, ds.name, fc.cost
FROM fact_cost fc
JOIN dict_sku ds ON fc.sku_id = ds.sku_id
ORDER BY fc.cost DESC
LIMIT 10;
"""

sql_req_37 = "Найди товары, закупочная цена которых ниже 100 тенге"
sql_37 = """
SELECT ds.sku_id, ds.name, fc.cost
FROM fact_cost fc
JOIN dict_sku ds ON fc.sku_id = ds.sku_id
WHERE fc.cost < 100;
"""

sql_req_38 = "Покажи закупочную цену товара Coca-Cola 0.5л в каждом магазине"
sql_38 = """
SELECT fc.store_id, ds.sku_id, ds.name, fc.cost
FROM fact_cost fc
JOIN dict_sku ds ON fc.sku_id = ds.sku_id
WHERE LOWER(ds.name) = LOWER('Coca-Cola 0.5л');
"""

sql_req_39 = "Покажи прибыль по каждому товару в магазине Алматы 1"
sql_39 = """
SELECT ds.sku_id, ds.name, SUM(fs.profit) AS total_profit
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
WHERE fs.store_id = 'Алматы 1'
GROUP BY ds.sku_id, ds.name;
"""

sql_req_40 = "Какая категория товаров приносит наибольшую прибыль?"
sql_40 = """
SELECT LOWER(ds.category) AS category, SUM(fs.profit) AS total_profit
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY LOWER(ds.category)
ORDER BY total_profit DESC
LIMIT 1;
"""

sql_req_41 = "Сравни прибыль от продаж Coca-Cola 0.5л и Pepsi 1л в августе"
sql_41 = """
SELECT ds.name, SUM(fs.profit) AS total_profit
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
WHERE (LOWER(ds.name) = LOWER('Coca-Cola 0.5л')
    OR LOWER(ds.name) = LOWER('Pepsi 1л'))
  AND DATE_TRUNC('month', fs.order_date) = '2025-08-01'
GROUP BY ds.name;
"""     

sql_req_42 = "Найди топ-10 товаров по прибыли за сентябрь"
sql_42 = """
SELECT ds.sku_id, ds.name, SUM(fs.profit) AS total_profit
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
WHERE DATE_TRUNC('month', fs.order_date) = '2025-09-01'
GROUP BY ds.sku_id, ds.name
ORDER BY total_profit DESC
LIMIT 10;
"""

sql_req_43 = "Какие товары оказались убыточными (revenue < cost)?"
sql_43 = """
SELECT ds.sku_id, ds.name, SUM(fs.revenue) AS total_revenue, SUM(fs.cost) AS total_cost
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY ds.sku_id, ds.name
HAVING SUM(fs.revenue) < SUM(fs.cost);
"""

sql_req_44 = "Какая доля категории Алкогольные напитки в общей прибыли сети?"
sql_44 = """
SELECT
  SUM(CASE WHEN LOWER(ds.category) = LOWER('Алкогольные напитки') THEN fs.profit ELSE 0 END)::DECIMAL
  / NULLIF(SUM(fs.profit),0) AS share_alcohol
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id;
"""

sql_req_45 = "Какие товары дали максимальную маржу в процентах (profit / revenue)?"
sql_45 = """
SELECT ds.sku_id, ds.name,
       SUM(fs.profit) / NULLIF(SUM(fs.revenue),0) AS margin_pct
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY ds.sku_id, ds.name
ORDER BY margin_pct DESC
LIMIT 10;
"""

sql_req_46 = "Покажи среднюю наценку по каждому товару"
sql_46 = """
SELECT ds.sku_id, ds.name,
       AVG((fs.revenue - fs.cost) / NULLIF(fs.cost,0)) AS avg_markup
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY ds.sku_id, ds.name;
"""

sql_req_47 = "Какая категория товаров имеет наибольшую наценку?"
sql_47 = """
SELECT LOWER(ds.category) AS category,
       AVG((fs.revenue - fs.cost) / NULLIF(fs.cost,0)) AS avg_markup
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY LOWER(ds.category)
ORDER BY avg_markup DESC
LIMIT 1;
"""     

sql_req_48 = "Сравни наценку на Coca-Cola 0.5л и Pepsi 1л"
sql_48 = """
SELECT ds.name,
       AVG((fs.revenue - fs.cost) / NULLIF(fs.cost,0)) AS avg_markup
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
WHERE LOWER(ds.name) IN (LOWER('Coca-Cola 0.5л'), LOWER('Pepsi 1л'))
GROUP BY ds.name;
"""

sql_req_49 = "Найди топ-10 товаров с максимальной наценкой"
sql_49 = """
SELECT ds.sku_id, ds.name,
       AVG((fs.revenue - fs.cost) / NULLIF(fs.cost,0)) AS avg_markup
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY ds.sku_id, ds.name
ORDER BY avg_markup DESC
LIMIT 10;
"""

sql_req_50 = "Какие категории имеют наценку выше 50%?"
sql_50 = """
SELECT LOWER(ds.category) AS category,
       AVG((fs.revenue - fs.cost) / NULLIF(fs.cost,0)) AS avg_markup
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY LOWER(ds.category)
HAVING AVG((fs.revenue - fs.cost) / NULLIF(fs.cost,0)) > 0.5;
"""

sql_req_51 = "Сколько всего позиций у нас в молочке?"
sql_51 = """
SELECT COUNT(DISTINCT ds.sku_id)
FROM dict_sku ds
WHERE LOWER(ds.category) = LOWER('Молочные продукты');
"""

sql_req_52 = "Вытащи все товары из газировки"
sql_52 = """
SELECT ds.sku_id, ds.name
FROM dict_sku ds
WHERE LOWER(ds.category) = LOWER('Безалкогольные напитки');
"""

sql_req_53 = "Какие у нас есть позиции по коле?"
sql_53 = """
SELECT ds.sku_id, ds.name
FROM dict_sku ds
WHERE LOWER(ds.name) LIKE LOWER('%кола%');
""" 

sql_req_54 = "Найди все товары бренда Орбит"
sql_54 = """
SELECT ds.sku_id, ds.name
FROM dict_sku ds
WHERE LOWER(ds.brand) = LOWER('Orbit');
"""

sql_req_55 = "Сколько всего SKU у бренда Тасай?"
sql_55 = """
SELECT COUNT(DISTINCT ds.sku_id)
FROM dict_sku ds
WHERE LOWER(ds.brand) = LOWER('Tassay');
"""

sql_req_56 = "Какие товары сейчас в нуле по остаткам?"
sql_56 = """
SELECT fb.sku_id, ds.name, fb.store_id
FROM fact_bal fb
JOIN dict_sku ds ON fb.sku_id = ds.sku_id
WHERE fb.quantity_warehouse = 0
  AND fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal);
"""

sql_req_57 = "Сколько всего молочки лежит на складах по сети?"
sql_57 = """
SELECT SUM(fb.quantity_warehouse) AS total_qty
FROM fact_bal fb
JOIN dict_sku ds ON fb.sku_id = ds.sku_id
WHERE LOWER(ds.category) = LOWER('Молочные продукты')
  AND fb.rep_date = (SELECT MAX(rep_date) FROM fact_bal);
"""

sql_req_58 = "Какие товары самые дорогие по закупу?"
sql_58 = """
SELECT ds.sku_id, ds.name, fc.cost
FROM fact_cost fc
JOIN dict_sku ds ON fc.sku_id = ds.sku_id
ORDER BY fc.cost DESC
LIMIT 10;
"""

sql_req_59 = "Какие товары у нас в минусе?"
sql_59 = """
SELECT ds.sku_id, ds.name, SUM(fs.revenue) AS total_revenue, SUM(fs.cost) AS total_cost
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY ds.sku_id, ds.name
HAVING SUM(fs.revenue) < SUM(fs.cost);
""" 

sql_req_60 = "Какая доля алкашки в общей прибыли сети?"
sql_60 = """
SELECT
  SUM(CASE WHEN LOWER(ds.category) = LOWER('Алкогольные напитки') THEN fs.profit ELSE 0 END)::DECIMAL
  / NULLIF(SUM(fs.profit),0) AS share_alcohol
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id;
"""

sql_req_61 = "Какие товары дали самую жирную маржу в процентах?"
sql_61 = """
SELECT ds.sku_id, ds.name,
       SUM(fs.profit) / NULLIF(SUM(fs.revenue),0) AS margin_pct
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY ds.sku_id, ds.name
ORDER BY margin_pct DESC
LIMIT 10;
"""

sql_req_62 = "Какие категории дают наценку больше 50%?"
sql_62 = """
SELECT LOWER(ds.category) AS category,
       AVG((fs.revenue - fs.cost) / NULLIF(fs.cost,0)) AS avg_markup
FROM fact_sales fs
JOIN dict_sku ds ON fs.sku_id = ds.sku_id
GROUP BY LOWER(ds.category)
HAVING AVG((fs.revenue - fs.cost) / NULLIF(fs.cost,0)) > 0.5;
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
    sql_req_41,
    sql_req_42,
    sql_req_43,
    sql_req_44,
    sql_req_45,
    sql_req_46,
    sql_req_47,
    sql_req_48,
    sql_req_49,
    sql_req_50,
    sql_req_51,
    sql_req_52,
    sql_req_53,
    sql_req_54,
    sql_req_55,
    sql_req_56,
    sql_req_57,
    sql_req_58,
    sql_req_59,
    sql_req_60,
    sql_req_61,
    sql_req_62,
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
    sql_10,
    sql_11,
    sql_12,
    sql_13,
    sql_14,
    sql_15,
    sql_16,
    sql_17,
    sql_18,
    sql_19,
    sql_20,
    sql_21,
    sql_22,
    sql_23,
    sql_24,
    sql_25,
    sql_26,
    sql_27,
    sql_28,
    sql_29,
    sql_30,
    sql_31,
    sql_32,
    sql_33,
    sql_34,
    sql_35,
    sql_36,
    sql_37,
    sql_38,
    sql_39,
    sql_40,
    sql_41,
    sql_42,
    sql_43,
    sql_44,
    sql_45,
    sql_46,
    sql_47,
    sql_48,
    sql_49,
    sql_50,
    sql_51,
    sql_52,
    sql_53,
    sql_54,
    sql_55,
    sql_56,
    sql_57,
    sql_58,
    sql_59,
    sql_60,
    sql_61,
    sql_62,
]
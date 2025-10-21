import sqlite3
import pandas as pd
from ds_helper import visualize

# Create the database from SQL file
conn = sqlite3.connect('retail_sales.db')
with open('retail_sales.sql', 'r') as f:
    sql_script = f.read()
conn.executescript(sql_script)
conn.commit()

# Function to execute query and visualize
def execute_and_visualize(query, name):
    df = pd.read_sql_query(query, conn)
    print(f"Results for {name}:")
    print(df)
    visualize(df)
    print(f"Visualizations saved for {name}")

# Query 1: Best-selling product
query1 = """
SELECT p.name, SUM(s.quantity) AS total_quantity
FROM Sales s
JOIN Products p ON s.product_id = p.id
GROUP BY p.id, p.name
ORDER BY total_quantity DESC
LIMIT 1;
"""
execute_and_visualize(query1, "Best-Selling Product")

# Query 2: Total sales per product category
query2 = """
SELECT p.category, SUM(s.total_amount) AS total_sales
FROM Sales s
JOIN Products p ON s.product_id = p.id
GROUP BY p.category
ORDER BY total_sales DESC;
"""
execute_and_visualize(query2, "Total Sales per Category")

# Query 3: Average purchase per customer
query3 = """
SELECT c.name, AVG(s.total_amount) AS avg_purchase
FROM Sales s
JOIN Customers c ON s.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY avg_purchase DESC;
"""
execute_and_visualize(query3, "Average Purchase per Customer")

# Query 4: Daily sales trends
query4 = """
SELECT sale_date, SUM(total_amount) AS daily_sales
FROM Sales
GROUP BY sale_date
ORDER BY sale_date;
"""
execute_and_visualize(query4, "Daily Sales Trends")

# Query 5: Monthly sales trends
query5 = """
SELECT strftime('%Y-%m', sale_date) AS month, SUM(total_amount) AS monthly_sales
FROM Sales
GROUP BY month
ORDER BY month;
"""
execute_and_visualize(query5, "Monthly Sales Trends")

# Close the connection
conn.close()

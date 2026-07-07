"""
Q9: MONTHLY REVENUE TREND
Category: Sales Analytics
Insight: Oct 2025 peak (2.8Cr). Dec 2025 dropped 66%.
Output: monthly_revenue.csv
"""

import sqlite3
import pandas as pd
import os

# Get script's directory for reliable paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to script location
db_path = os.path.abspath(os.path.join(script_dir, '..', 'hyundai_dealership.db'))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'dashboard_data'))
output_path = os.path.join(output_dir, 'monthly_revenue.csv')

print(f"DB: {db_path}")
print(f"Output: {output_path}")

# Connect to DB
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT 
    strftime('%Y-%m', i.invoice_date) as month,
    COUNT(*) as vehicles_sold,
    ROUND(SUM(i.ex_showroom_price), 0) as sales_revenue,
    ROUND(SUM(i.accessories_amount), 0) as accessories_revenue,
    ROUND(SUM(i.total_amount), 0) as total_revenue
FROM invoices i
GROUP BY strftime('%Y-%m', i.invoice_date)
ORDER BY month
"""

df = pd.read_sql(query, conn)

print("\nQ9: MONTHLY REVENUE TREND")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\nExported to: {output_path}")

conn.close()
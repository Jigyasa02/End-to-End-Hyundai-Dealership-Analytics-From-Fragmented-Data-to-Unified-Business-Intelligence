"""
Q6: MODEL-WISE SALES PERFORMANCE
Category: Sales Analytics
Insight: Creta dominates (31% of sales). Tucson is premium niche.
Output: model_sales.csv
"""

import sqlite3
import pandas as pd
import os

# Get script's directory for reliable paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to script location
db_path = os.path.abspath(os.path.join(script_dir, '..', 'hyundai_dealership.db'))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'dashboard_data'))
output_path = os.path.join(output_dir, 'model_sales.csv')

print(f"DB: {db_path}")
print(f"Output: {output_path}")

# Connect to DB
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT 
    b.model_name,
    COUNT(*) as units_sold,
    ROUND(AVG(i.ex_showroom_price), 0) as avg_ex_price,
    ROUND(SUM(i.total_amount), 0) as total_revenue,
    ROUND(SUM(i.discount_amount), 0) as total_discounts,
    ROUND(AVG(i.accessories_amount), 0) as avg_accessories
FROM bookings b
JOIN vehicle_allocations va ON b.booking_id = va.booking_id
JOIN invoices i ON va.allocation_id = i.allocation_id
WHERE b.status IN ('Confirmed', 'Delivered')
GROUP BY b.model_name
ORDER BY units_sold DESC
"""

df = pd.read_sql(query, conn)

print("\nQ6: MODEL-WISE SALES PERFORMANCE")
print("-" * 50)
print(df.to_string(index=False))
print("\n Query executed successfully!")

# Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\n Exported to: {output_path}")

conn.close()
"""
Q10: COLOR PREFERENCE ANALYSIS
Category: Sales Analytics
Insight: Dark colors (Black + Grey) = 37%. White is classic choice.
Output: color_distribution.csv
"""

import sqlite3
import pandas as pd
import os

# Get script's directory for reliable paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to script location
db_path = os.path.abspath(os.path.join(script_dir, '..', 'hyundai_dealership.db'))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'dashboard_data'))
output_path = os.path.join(output_dir, 'color_distribution.csv')

print(f"DB: {db_path}")
print(f"Output: {output_path}")

# Connect to DB
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT 
    v.color,
    COUNT(*) as units_sold,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM vehicles v
JOIN vehicle_allocations va ON v.vehicle_id = va.vehicle_id
JOIN bookings b ON va.booking_id = b.booking_id
WHERE b.status IN ('Confirmed', 'Delivered')
GROUP BY v.color
ORDER BY units_sold DESC
"""

df = pd.read_sql(query, conn)

print("\nQ10: COLOR PREFERENCE ANALYSIS")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\nExported to: {output_path}")

conn.close()
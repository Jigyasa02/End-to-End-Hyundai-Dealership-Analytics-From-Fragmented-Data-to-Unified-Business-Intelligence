"""
Q5: MONTHLY BOOKING TREND
Category: Sales Analytics
Insight: Seasonal pattern: Peak Oct 2025, dip Dec 2025
Output: q05_monthly_booking_trend.csv
"""

import sqlite3
import pandas as pd
import os

# Get script's directory for reliable paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to script location
db_path = os.path.abspath(os.path.join(script_dir, '..', 'hyundai_dealership.db'))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'dashboard_data'))
output_path = os.path.join(output_dir, 'q05_monthly_booking_trend.csv')

print(f"DB: {db_path}")
print(f"Output: {output_path}")

# Connect to DB
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT 
    strftime('%Y-%m', booking_date) as month,
    COUNT(*) as total_bookings,
    SUM(CASE WHEN status IN ('Confirmed', 'Delivered') THEN 1 ELSE 0 END) as active_bookings,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
    ROUND(SUM(booking_amount), 0) as total_booking_amount
FROM bookings
GROUP BY strftime('%Y-%m', booking_date)
ORDER BY month
"""

df = pd.read_sql(query, conn)

print("\nQ5: MONTHLY BOOKING TREND")
print("-" * 50)
print(df.to_string(index=False))
print("\n Query executed successfully!")

# Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\n Exported to: {output_path}")
print(" This data is also included in monthly_revenue.csv (Q9)")

conn.close()
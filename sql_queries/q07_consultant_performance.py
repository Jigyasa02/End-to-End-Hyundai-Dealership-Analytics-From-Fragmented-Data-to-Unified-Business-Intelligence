"""
Q7: TOP 10 SALES CONSULTANT PERFORMANCE
Category: Sales Analytics
Insight: Top 3 generate 25% of revenue. Rahul Mehta highest avg deal.
Output: consultant_performance.csv
"""

import sqlite3
import pandas as pd
import os

# Get script's directory for reliable paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to script location
db_path = os.path.abspath(os.path.join(script_dir, '..', 'hyundai_dealership.db'))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'dashboard_data'))
output_path = os.path.join(output_dir, 'consultant_performance.csv')

print(f"DB: {db_path}")
print(f"Output: {output_path}")

# Connect to DB
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT 
    e.first_name || ' ' || e.last_name as consultant,
    e.designation,
    COUNT(DISTINCT b.booking_id) as bookings_closed,
    ROUND(SUM(i.total_amount), 0) as total_revenue,
    ROUND(AVG(i.total_amount), 0) as avg_deal_size,
    COUNT(DISTINCT e2.enquiry_id) as enquiries_handled,
    ROUND(100.0 * COUNT(DISTINCT b.booking_id) / NULLIF(COUNT(DISTINCT e2.enquiry_id), 0), 2) as conversion_rate
FROM employees e
LEFT JOIN bookings b ON e.employee_id = b.employee_id AND b.status IN ('Confirmed', 'Delivered')
LEFT JOIN invoices i ON b.booking_id = i.booking_id
LEFT JOIN enquiries e2 ON e.employee_id = e2.employee_id
WHERE e.department = 'Sales'
GROUP BY e.employee_id
ORDER BY total_revenue DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

print("\nQ7: TOP 10 SALES CONSULTANT PERFORMANCE")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\nExported to: {output_path}")

conn.close()
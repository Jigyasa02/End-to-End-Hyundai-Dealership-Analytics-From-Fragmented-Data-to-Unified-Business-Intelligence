"""
Q4: OVERALL SALES FUNNEL
Category: Sales Analytics
Insight: Major drop at Enquiry->TD (65% loss). Focus on TD scheduling.
Output: sales_funnel.csv
"""

import sqlite3
import pandas as pd
import os

# Get script's directory for reliable paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to script location
db_path = os.path.abspath(os.path.join(script_dir, '..', 'hyundai_dealership.db'))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'dashboard_data'))
output_path = os.path.join(output_dir, 'sales_funnel.csv')

print(f"DB: {db_path}")
print(f"Output: {output_path}")

# Connect to DB
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT 'Enquiries' as stage, COUNT(*) as count FROM enquiries
UNION ALL
SELECT 'Test Drives', COUNT(*) FROM test_drives
UNION ALL
SELECT 'Bookings (Active)', COUNT(*) FROM bookings WHERE status IN ('Confirmed', 'Delivered')
UNION ALL
SELECT 'Bookings (Delivered)', COUNT(*) FROM bookings WHERE status = 'Delivered'
UNION ALL
SELECT 'Invoices', COUNT(*) FROM invoices
"""

df = pd.read_sql(query, conn)

print("\nQ4: OVERALL SALES FUNNEL")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\nExported to: {output_path}")

conn.close()
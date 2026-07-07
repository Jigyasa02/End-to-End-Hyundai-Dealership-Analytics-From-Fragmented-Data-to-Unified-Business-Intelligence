"""
Q2: ENQUIRY TO TEST DRIVE CONVERSION
Category: Sales Analytics
Insight: 35% TD rate - opportunity to improve scheduling
Output: q02_td_conversion.csv
"""

import sqlite3
import pandas as pd
import os

# Get script's directory for reliable paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to script location
db_path = os.path.abspath(os.path.join(script_dir, '..', 'hyundai_dealership.db'))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'dashboard_data'))
output_path = os.path.join(output_dir, 'q02enquiries_td_conversion.csv')

print(f"DB: {db_path}")
print(f"Output: {output_path}")

# Connect to DB
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT 
    (SELECT COUNT(*) FROM enquiries) as total_enquiries,
    (SELECT COUNT(*) FROM test_drives) as test_drives_done,
    ROUND(100.0 * (SELECT COUNT(*) FROM test_drives) / (SELECT COUNT(*) FROM enquiries), 2) as td_conversion_rate
"""

df = pd.read_sql(query, conn)

print("\nQ2: ENQUIRY TO TEST DRIVE CONVERSION")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\nExported to: {output_path}")
print("Note: Combine with Q3 and Q4 to create sales_funnel.csv")

conn.close()
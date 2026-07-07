"""
Q8: ENQUIRY SOURCE ANALYSIS
Category: Sales Analytics
Insight: CarWale highest conversion (26%) but low volume. Walk-in has volume.
Output: source_analysis.csv
"""

import sqlite3
import pandas as pd
import os

# Get script's directory for reliable paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to script location
db_path = os.path.abspath(os.path.join(script_dir, '..', 'hyundai_dealership.db'))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'dashboard_data'))
output_path = os.path.join(output_dir, 'enquiries_ssource_analysis.csv')

print(f"DB: {db_path}")
print(f"Output: {output_path}")

# Connect to DB
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT 
    source,
    COUNT(*) as total_enquiries,
    SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) as converted,
    ROUND(100.0 * SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) / COUNT(*), 2) as conversion_rate
FROM enquiries
GROUP BY source
ORDER BY total_enquiries DESC
"""

df = pd.read_sql(query, conn)

print("\nQ8: ENQUIRY SOURCE ANALYSIS")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Export
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\nExported to: {output_path}")

conn.close()
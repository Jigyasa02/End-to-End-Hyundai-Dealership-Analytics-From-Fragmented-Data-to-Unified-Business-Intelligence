"""
Q1: LEAD CONVERSION RATE
Category: Sales Analytics
Insight: Industry benchmark 10-15%. Your 14.7% is healthy.
Output: source_analysis.csv
"""

import sqlite3
import pandas as pd
import os

# Step 1: Connect to database (db is in parent folder)
conn = sqlite3.connect('hyundai_dealership.db')

# Step 2: Write SQL query
query = """
SELECT 
    COUNT(*) as total_enquiries,
    SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) as converted,
    ROUND(100.0 * SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) / COUNT(*), 2) as conversion_rate
FROM enquiries
"""

# Step 3: Run SQL and store in DataFrame
df = pd.read_sql(query, conn)

# Step 4: Verify output
print("Q1: LEAD CONVERSION RATE")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 5: Export to CSV (dashboard_data is sibling folder)
output_path = 'dashboard_data/lead_conversion.csv' 
df.to_csv(output_path, index=False)
print(f"Exported to: {output_path}")

# Close connection
conn.close()
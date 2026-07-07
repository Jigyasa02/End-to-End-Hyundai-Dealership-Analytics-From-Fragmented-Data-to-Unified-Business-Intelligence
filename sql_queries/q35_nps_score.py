import sqlite3
import pandas as pd
import os

# Get project paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

# Connect to database
db_path = os.path.join(project_dir, 'hyundai_dealership.db')
conn = sqlite3.connect(db_path)

# SQL Query
query = """
SELECT *
FROM customer_feedback
"""

# Execute query
df = pd.read_sql(query, conn)

# Verify output
print("CUSTOMER FEEDBACK DATA")
print("-" * 50)

print("\nColumns in customer_feedback table:")
print(df.columns.tolist())

print(f"\nTotal Records: {len(df)}")

# Check if is_nps exists
if 'is_nps' in df.columns:
    print("\n'is_nps' column FOUND")
    print("\nSample is_nps values:")
    print(df['is_nps'].head(10))
else:
    print("\n'is_nps' column NOT FOUND")

# Show first 5 rows
print("\nFirst 5 Rows:")
print(df.head())

# Create dashboard_data folder if needed
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Export CSV
output_file = os.path.join(
    dashboard_dir,
    'customer_feedback.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Close connection
conn.close()
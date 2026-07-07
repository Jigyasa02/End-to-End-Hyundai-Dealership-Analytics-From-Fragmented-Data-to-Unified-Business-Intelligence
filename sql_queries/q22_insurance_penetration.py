import sqlite3
import pandas as pd
import os

# Step 1: Get project paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

# Step 2: Connect to database
db_path = os.path.join(project_dir, 'hyundai_dealership.db')
conn = sqlite3.connect(db_path)

# Step 3: SQL Query
query = """
SELECT 
    (SELECT COUNT(*) FROM invoices) as total_sales,
    (SELECT COUNT(*) 
     FROM insurance_policies 
     WHERE status = 'Active') as policies_sold,
    ROUND(
        100.0 *
        (SELECT COUNT(*) 
         FROM insurance_policies 
         WHERE status = 'Active')
        /
        (SELECT COUNT(*) FROM invoices),
        2
    ) as insurance_penetration
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q22: INSURANCE PENETRATION RATE")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'q22_insurance_penetration.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
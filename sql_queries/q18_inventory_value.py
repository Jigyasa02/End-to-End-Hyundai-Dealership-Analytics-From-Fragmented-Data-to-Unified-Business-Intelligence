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
    SUM(CASE WHEN status = 'Available' THEN cost_price ELSE 0 END) as available_stock_value,
    SUM(CASE WHEN status = 'Allocated' THEN cost_price ELSE 0 END) as allocated_stock_value,
    SUM(cost_price) as total_inventory_value,
    COUNT(CASE WHEN status = 'Available' THEN 1 END) as available_units,
    COUNT(CASE WHEN status = 'Allocated' THEN 1 END) as allocated_units
FROM vehicles
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q18: INVENTORY VALUE")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(dashboard_dir, 'q18_inventory_value.csv')
df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
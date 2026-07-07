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
    model_name,
    COUNT(*) as units,
    ROUND(AVG(julianday('now') - julianday(arrival_date)), 0) as avg_age_days,
    CASE 
        WHEN AVG(julianday('now') - julianday(arrival_date)) < 30 THEN 'Fast Moving'
        WHEN AVG(julianday('now') - julianday(arrival_date)) < 60 THEN 'Normal'
        ELSE 'Slow Moving'
    END as stock_category
FROM vehicles
WHERE status = 'Available'
GROUP BY model_name
ORDER BY avg_age_days DESC
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q17: STOCK AGING ANALYSIS")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(dashboard_dir, 'stock_aging.csv')
df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
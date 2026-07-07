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
    gender,
    COUNT(*) as count,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER(),
        2
    ) as percentage,
    ROUND(
        AVG(
            CASE 
                WHEN income_bracket = '< 5 LPA' THEN 1 
                ELSE 0 
            END
        ),
        2
    ) as pct_below_5lpa,
    ROUND(
        AVG(
            CASE 
                WHEN income_bracket IN ('15-25 LPA', '25-40 LPA', '> 40 LPA')
                THEN 1
                ELSE 0
            END
        ),
        2
    ) as pct_high_income
FROM customers
GROUP BY gender
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q27: CUSTOMER DEMOGRAPHICS")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'q27_customer_demographics.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
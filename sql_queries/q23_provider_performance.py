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
    insurance_provider,
    COUNT(*) as policies_sold,
    ROUND(SUM(premium_amount), 0) as total_premium,
    ROUND(SUM(commission_amount), 0) as total_commission,
    ROUND(AVG(premium_amount), 0) as avg_premium,
    ROUND(AVG(commission_amount), 0) as avg_commission,
    ROUND(
        100.0 * SUM(commission_amount) / SUM(premium_amount),
        2
    ) as commission_pct
FROM insurance_policies
WHERE status = 'Active'
GROUP BY insurance_provider
ORDER BY policies_sold DESC
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q23: INSURANCE PROVIDER PERFORMANCE")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'provider_performance.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
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
    ro_type,
    COUNT(*) as job_count,
    ROUND(SUM(actual_cost), 0) as total_revenue,
    ROUND(AVG(actual_cost), 0) as avg_cost,
    ROUND(
        AVG(
            CASE 
                WHEN customer_feedback_rating IS NOT NULL 
                THEN customer_feedback_rating 
            END
        ), 2
    ) as avg_rating
FROM repair_orders
WHERE status = 'Completed'
GROUP BY ro_type
ORDER BY job_count DESC
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q12: SERVICE TYPE BREAKDOWN")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(dashboard_dir, 'service_types.csv')
df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
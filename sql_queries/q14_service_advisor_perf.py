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
    e.first_name || ' ' || e.last_name as advisor,
    COUNT(*) as jobs_handled,
    ROUND(SUM(ro.actual_cost), 0) as revenue_generated,
    ROUND(AVG(ro.customer_feedback_rating), 2) as avg_customer_rating
FROM employees e
JOIN repair_orders ro 
    ON e.employee_id = ro.employee_id
WHERE ro.status = 'Completed'
GROUP BY e.employee_id
ORDER BY revenue_generated DESC
LIMIT 8
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q14: SERVICE ADVISOR PERFORMANCE")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(dashboard_dir, 'q14_advisor_performance.csv')
df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
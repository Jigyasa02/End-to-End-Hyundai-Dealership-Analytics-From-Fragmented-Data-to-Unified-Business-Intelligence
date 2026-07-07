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
    (
        SELECT ROUND(SUM(actual_cost), 0)
        FROM repair_orders
        WHERE status = 'Completed'
    ) as service_revenue,

    (
        SELECT ROUND(SUM(salary * 12), 0)
        FROM employees
        WHERE is_active = 1
    ) as annual_payroll,

    (
        SELECT ROUND(SUM(cost_price), 0)
        FROM vehicles
        WHERE status = 'Available'
    ) * 0.10 as est_overhead,

    ROUND(
        100.0 *
        (
            SELECT SUM(actual_cost)
            FROM repair_orders
            WHERE status = 'Completed'
        )
        /
        (
            (
                SELECT SUM(salary * 12)
                FROM employees
                WHERE is_active = 1
            )
            +
            (
                SELECT SUM(cost_price)
                FROM vehicles
                WHERE status = 'Available'
            ) * 0.10
        ),
        2
    ) as service_absorption_pct
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q34: SERVICE ABSORPTION RATE")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'q34_service_absorption.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
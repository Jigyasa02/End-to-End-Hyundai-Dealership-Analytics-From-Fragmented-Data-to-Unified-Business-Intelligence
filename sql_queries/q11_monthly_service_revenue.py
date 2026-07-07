

import sqlite3
import pandas as pd
import os

# Get current script location
script_dir = os.path.dirname(os.path.abspath(__file__))

# Project folder (parent of sql_scripts)
project_dir = os.path.dirname(script_dir)

# Database path
db_path = os.path.join(project_dir, "hyundai_dealership.db")

print("Database Path:")
print(db_path)

# Connect to database
conn = sqlite3.connect(db_path)

# SQL Query
query = """
SELECT 
    strftime('%Y-%m', ro_date) AS month,
    COUNT(*) AS total_jobs,
    SUM(CASE WHEN status = 'Completed' THEN actual_cost ELSE 0 END) AS completed_revenue,
    SUM(CASE WHEN status = 'Completed' THEN estimated_cost ELSE 0 END) AS estimated_revenue,
    ROUND(AVG(CASE WHEN status = 'Completed' THEN actual_cost END), 0) AS avg_ticket_size
FROM repair_orders
GROUP BY strftime('%Y-%m', ro_date)
ORDER BY month;
"""

# Execute Query
df = pd.read_sql(query, conn)

# Display Results
print("\nQ11: MONTHLY SERVICE REVENUE")
print("-" * 60)
print(df.to_string(index=False))

# Create dashboard_data folder if it doesn't exist
dashboard_dir = os.path.join(project_dir, "dashboard_data")
os.makedirs(dashboard_dir, exist_ok=True)

# CSV Output Path
output_file = os.path.join(dashboard_dir, "monthly_service.csv")

# Export CSV
df.to_csv(output_file, index=False)

print("\nCSV Created Successfully!")
print("Saved to:")
print(output_file)

# Close Connection
conn.close()
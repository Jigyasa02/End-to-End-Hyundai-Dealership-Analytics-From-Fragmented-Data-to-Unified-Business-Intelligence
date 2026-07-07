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
    strftime('%Y-%m', application_date) as month,
    COUNT(*) as applications,
    SUM(processing_fee) as processing_fee_revenue,
    SUM(loan_amount) as total_disbursed,
    ROUND(AVG(emi_amount), 0) as avg_emi
FROM finance_applications
WHERE status = 'Disbursed'
GROUP BY strftime('%Y-%m', application_date)
ORDER BY month
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q21: MONTHLY FINANCE PERFORMANCE")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'monthly_finance.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
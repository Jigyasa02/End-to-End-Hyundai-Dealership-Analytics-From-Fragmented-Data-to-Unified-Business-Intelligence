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
    bank_name,
    COUNT(*) as applications,
    SUM(CASE WHEN status = 'Disbursed' THEN 1 ELSE 0 END) as disbursed,
    SUM(CASE WHEN status = 'Approved' THEN 1 ELSE 0 END) as approved,
    SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END) as rejected,
    ROUND(SUM(loan_amount), 0) as total_loan_amount,
    ROUND(AVG(interest_rate), 2) as avg_interest_rate,
    ROUND(
        100.0 * 
        SUM(CASE WHEN status = 'Disbursed' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) as success_rate
FROM finance_applications
GROUP BY bank_name
ORDER BY applications DESC
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q20: BANK-WISE FINANCE PERFORMANCE")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'bank_performance.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
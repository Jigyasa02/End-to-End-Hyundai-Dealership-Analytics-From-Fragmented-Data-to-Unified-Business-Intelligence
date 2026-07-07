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
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', invoice_date) as month,
        SUM(total_amount) as sales_revenue
    FROM invoices
    GROUP BY strftime('%Y-%m', invoice_date)
),

monthly_service AS (
    SELECT 
        strftime('%Y-%m', ro_date) as month,
        SUM(actual_cost) as service_revenue
    FROM repair_orders
    WHERE status = 'Completed'
    GROUP BY strftime('%Y-%m', ro_date)
),

monthly_insurance AS (
    SELECT 
        strftime('%Y-%m', start_date) as month,
        SUM(commission_amount) as insurance_commission
    FROM insurance_policies
    WHERE status = 'Active'
    GROUP BY strftime('%Y-%m', start_date)
),

monthly_finance AS (
    SELECT 
        strftime('%Y-%m', application_date) as month,
        SUM(processing_fee) as finance_revenue
    FROM finance_applications
    WHERE status = 'Disbursed'
    GROUP BY strftime('%Y-%m', application_date)
)

SELECT 
    COALESCE(s.month, sv.month, i.month, f.month) as month,
    
    ROUND(COALESCE(s.sales_revenue, 0), 0) as sales_revenue,
    
    ROUND(COALESCE(sv.service_revenue, 0), 0) as service_revenue,
    
    ROUND(COALESCE(i.insurance_commission, 0), 0) as insurance_commission,
    
    ROUND(COALESCE(f.finance_revenue, 0), 0) as finance_revenue,
    
    ROUND(
        COALESCE(s.sales_revenue, 0) +
        COALESCE(sv.service_revenue, 0) +
        COALESCE(i.insurance_commission, 0) +
        COALESCE(f.finance_revenue, 0),
        0
    ) as total_revenue

FROM monthly_sales s
LEFT JOIN monthly_service sv
    ON s.month = sv.month
LEFT JOIN monthly_insurance i
    ON s.month = i.month
LEFT JOIN monthly_finance f
    ON s.month = f.month

ORDER BY month
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q30: MONTHLY REVENUE MIX")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'monthly_revenue.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
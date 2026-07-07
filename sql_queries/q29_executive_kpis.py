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
    (SELECT COUNT(*)
    FROM invoices
    ) as total_vehicles_sold,
     
    (SELECT ROUND(SUM(total_amount), 0) 
     FROM invoices) as total_sales_revenue,

    (SELECT ROUND(SUM(actual_cost), 0) 
     FROM repair_orders 
     WHERE status = 'Completed') as total_service_revenue,

    (SELECT ROUND(SUM(commission_amount), 0) 
     FROM insurance_policies 
     WHERE status = 'Active') as total_insurance_commission,

    (SELECT ROUND(SUM(processing_fee), 0) 
     FROM finance_applications 
     WHERE status = 'Disbursed') as total_finance_revenue,

    (SELECT ROUND(
        SUM(total_amount) - 
        SUM(ex_showroom_price + tax_amount + rto_charges),
        0
     )
     FROM invoices) as total_accessories_revenue,

    (SELECT COUNT(*) 
     FROM repair_orders 
     WHERE status = 'Completed') as total_service_jobs,

    (SELECT COUNT(*) 
     FROM customers) as total_customers,

    (SELECT COUNT(*) 
     FROM vehicles 
     WHERE status = 'Available') as available_stock
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q29: EXECUTIVE DASHBOARD KPIs")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'executive_kpis.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
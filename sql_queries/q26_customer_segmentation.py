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
WITH customer_sales AS (
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name as customer_name,
        c.income_bracket,
        MAX(i.invoice_date) as last_purchase_date,
        COUNT(DISTINCT i.invoice_id) as frequency,
        ROUND(SUM(i.total_amount), 0) as monetary
    FROM customers c
    LEFT JOIN invoices i 
        ON c.customer_id = i.customer_id
    GROUP BY c.customer_id
)
SELECT 
    customer_name,
    income_bracket,
    last_purchase_date,
    frequency,
    monetary,
    CASE 
        WHEN julianday('now') - julianday(last_purchase_date) <= 60 
             AND frequency >= 2 
             AND monetary >= 2000000 
            THEN 'Champions'
        WHEN julianday('now') - julianday(last_purchase_date) <= 60 
             AND frequency >= 1 
            THEN 'Loyal Customers'
        WHEN julianday('now') - julianday(last_purchase_date) <= 90 
             AND monetary >= 1500000 
            THEN 'Potential Loyalists'
        WHEN julianday('now') - julianday(last_purchase_date) <= 180 
            THEN 'Recent Customers'
        WHEN julianday('now') - julianday(last_purchase_date) <= 365 
             AND frequency >= 2 
            THEN 'Promising'
        WHEN julianday('now') - julianday(last_purchase_date) <= 365 
             AND monetary >= 1500000 
            THEN 'Need Attention'
        WHEN julianday('now') - julianday(last_purchase_date) > 365 
            THEN 'At Risk'
        ELSE 'New'
    END as segment
FROM customer_sales
WHERE monetary > 0
ORDER BY monetary DESC
LIMIT 15
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q26: CUSTOMER SEGMENTATION (RFM)")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'q26_customer_segmentation.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
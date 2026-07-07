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
    b.model_name,
    COUNT(*) as units,

    ROUND(
        AVG(
            julianday(i.invoice_date) - julianday(b.booking_date)
        ),
        1
    ) as avg_days_to_invoice,

    ROUND(
        MIN(
            julianday(i.invoice_date) - julianday(b.booking_date)
        ),
        1
    ) as min_days,

    ROUND(
        MAX(
            julianday(i.invoice_date) - julianday(b.booking_date)
        ),
        1
    ) as max_days,

    ROUND(
        AVG(
            julianday(va.allocated_date) - julianday(b.booking_date)
        ),
        1
    ) as avg_days_to_allocate

FROM bookings b

JOIN vehicle_allocations va
    ON b.booking_id = va.booking_id

JOIN invoices i
    ON va.allocation_id = i.allocation_id

WHERE b.status IN ('Confirmed', 'Delivered')

GROUP BY b.model_name

ORDER BY avg_days_to_invoice DESC
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q33: MODEL-WISE DELIVERY SPEED")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'q33_model_wise_btd.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
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
    b.booking_id,
    b.model_name,
    b.variant,
    b.booking_date,
    b.expected_delivery_date,
    va.allocated_date,
    i.invoice_date,

    ROUND(
        julianday(
            COALESCE(
                va.allocated_date,
                b.expected_delivery_date
            )
        ) - julianday(b.booking_date),
        1
    ) as days_to_allocate,

    ROUND(
        julianday(i.invoice_date) - julianday(b.booking_date),
        1
    ) as days_to_invoice,

    CASE
        WHEN julianday(i.invoice_date) - julianday(b.booking_date) <= 14
            THEN 'Fast (<14 days)'

        WHEN julianday(i.invoice_date) - julianday(b.booking_date) <= 21
            THEN 'Normal (14-21 days)'

        ELSE 'Slow (>21 days)'
    END as delivery_speed

FROM bookings b

JOIN vehicle_allocations va
    ON b.booking_id = va.booking_id

JOIN invoices i
    ON va.allocation_id = i.allocation_id

WHERE b.status IN ('Confirmed', 'Delivered')

ORDER BY days_to_invoice DESC
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q31: BOOKING-TO-DELIVERY TIME ANALYSIS")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'booking_to_delivery.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
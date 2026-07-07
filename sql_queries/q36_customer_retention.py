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
WITH customer_activity AS (
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name as customer_name,
        COUNT(DISTINCT b.booking_id) as purchases,
        COUNT(DISTINCT ro.ro_id) as service_visits,
        MAX(i.invoice_date) as last_purchase,
        MAX(ro.ro_date) as last_service,
        julianday('now') - julianday(
            MAX(
                COALESCE(i.invoice_date, ro.ro_date)
            )
        ) as days_since_last_activity

    FROM customers c

    LEFT JOIN bookings b
        ON c.customer_id = b.customer_id
        AND b.status IN ('Confirmed', 'Delivered')

    LEFT JOIN invoices i
        ON b.booking_id = i.booking_id

    LEFT JOIN repair_orders ro
        ON c.customer_id = ro.customer_id

    GROUP BY c.customer_id
)

SELECT 
    CASE
        WHEN days_since_last_activity <= 90
            THEN 'Active (0-90 days)'

        WHEN days_since_last_activity <= 180
            THEN 'Warm (91-180 days)'

        WHEN days_since_last_activity <= 365
            THEN 'Cold (181-365 days)'

        ELSE 'Dormant (>365 days)'
    END as retention_status,

    COUNT(*) as customer_count,

    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER(),
        2
    ) as percentage

FROM customer_activity

GROUP BY retention_status

ORDER BY customer_count DESC
"""

# Step 4: Execute Query
df = pd.read_sql(query, conn)

# Step 5: Verify Output
print("Q36: CUSTOMER RETENTION STATUS")
print("-" * 50)
print(df.to_string(index=False))
print("\nQuery executed successfully!")

# Step 6: Create dashboard_data folder if missing
dashboard_dir = os.path.join(project_dir, 'dashboard_data')
os.makedirs(dashboard_dir, exist_ok=True)

# Step 7: Export CSV
output_file = os.path.join(
    dashboard_dir,
    'q36_customer_retention.csv'
)

df.to_csv(output_file, index=False)

print(f"\nCSV Created: {output_file}")

# Step 8: Close Connection
conn.close()
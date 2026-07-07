import sqlite3
import pandas as pd
import os

# Connect to your database
db_path = 'Hyundai_dealership.db'  # Change this if your DB file has a different name
conn = sqlite3.connect(db_path)

# Create output directory if it doesn't exist
output_dir = 'dashboard\data'
os.makedirs(output_dir, exist_ok=True)

# List of tables to export
tables = [
    'repair_orders',
    'repair_order_items',
    # Add more tables if needed:
    # 'customers',
    # 'employees',
    # 'vehicles',
    # 'enquiries',
    # 'test_drives',
    # 'bookings',
    # 'vehicle_allocations',
    # 'invoices',
    # 'insurance_policies',
    # 'payments',
    # 'finance_applications',
    # 'customer_feedback'
]

# Export each table to CSV
for table in tables:
    try:
        # Read table into DataFrame
        df = pd.read_sql_query(f" SELECT * FROM {table}", conn)
        
        # Export to CSV
        csv_path = os.path.join(output_dir, f"{table}.csv")
        df.to_csv(csv_path, index=False)
        
        print(f" Exported {table}: {len(df)} rows → {csv_path}")
        
    except Exception as e:
        print(f" Failed to export {table}: {e}")

# Close connection
conn.close()
print("\n All exports completed!")
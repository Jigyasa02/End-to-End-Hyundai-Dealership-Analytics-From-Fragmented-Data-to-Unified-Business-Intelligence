"""
Q3: TEST DRIVE TO BOOKING CONVERSION
Category: Sales Analytics
Insight: 79.4% - excellent test drive quality
Output: q03_td_to_booking.csv
"""

import sqlite3
import pandas as pd
import os

# Get script's directory for reliable paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to script location
db_path = os.path.abspath(os.path.join(script_dir, '..', 'hyundai_dealership.db'))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'dashboard_data'))
output_path = os.path.join(output_dir, 'q03_td_to_booking.csv')

print(f"DB: {db_path}")
print(f"Output: {output_path}")

# Connect to DB
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT 
    (SELECT COUNT(*) FROM test_drives WHERE outcome IN ('Booked', 'Interested')) as positive_td,
    (SELECT COUNT(*) FROM bookings WHERE test_drive_id IS NOT NULL AND status IN ('Confirmed', 'Delivered')) as bookings_from_td,
    ROUND(100.0 * (SELECT COUNT(*) FROM bookings WHERE test_drive_id IS NOT NULL AND status IN ('Confirmed', 'Delivered')) / 
          NULLIF((SELECT COUNT(*) FROM test_drives WHERE outcome IN ('Booked', 'Interested')), 0), 2) as booking_conversion_rate
"""

df = pd.read_sql(query, conn)

print("\nQ3: TEST DRIVE TO BOOKING CONVERSION")
print("-" * 50)
print(df.to_string(index=False))
print("\n Query executed successfully!")

# Export
output_path = 'dashboard_data/source_analysis.csv'  # 
os.makedirs(output_dir, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\n Exported to: {output_path}")

conn.close()
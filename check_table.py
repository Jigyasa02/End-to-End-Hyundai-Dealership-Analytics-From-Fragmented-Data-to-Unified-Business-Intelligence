import sqlite3

# Connect to database
conn = sqlite3.connect('hyundai_dealership.db')
cursor = conn.cursor()

print("=" * 50)
print("DATABASE TABLE RECORD COUNTS")
print("=" * 50)

tables = [
    "customers",
    "employees",
    "vehicles",
    "enquiries",
    "test_drives",
    "bookings",
    "vehicle_allocations",
    "invoices",
    "insurance_policies",
    "payments",
    "finance_applications",
    "repair_orders",
    "repair_order_items",
    "customer_feedback"
]

for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} : {count}")
    except Exception as e:
        print(f"{table:<25} : ERROR - {e}")

print("=" * 50)

# Extra checks for vehicle status
print("\nVEHICLE STATUS BREAKDOWN")
print("-" * 50)

try:
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM vehicles
        GROUP BY status
    """)

    for status, count in cursor.fetchall():
        print(f"{status:<15} : {count}")

except Exception as e:
    print("Error:", e)

print("\nBOOKING STATUS BREAKDOWN")
print("-" * 50)

try:
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM bookings
        GROUP BY status
    """)

    for status, count in cursor.fetchall():
        print(f"{status:<15} : {count}")

except Exception as e:
    print("Error:", e)

print("\nINVOICE PAYMENT STATUS BREAKDOWN")
print("-" * 50)

try:
    cursor.execute("""
        SELECT payment_status, COUNT(*)
        FROM invoices
        GROUP BY payment_status
    """)

    for status, count in cursor.fetchall():
        print(f"{status:<15} : {count}")

except Exception as e:
    print("Error:", e)

conn.close()

print("\nDatabase check completed.")
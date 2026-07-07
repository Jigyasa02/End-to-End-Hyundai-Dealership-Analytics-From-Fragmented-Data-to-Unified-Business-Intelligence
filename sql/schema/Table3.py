
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('hyundai_dealership.db')
cursor = conn.cursor()

print("=" * 60)
print("PHASE 3 (CONTINUED): FIXING DEPENDENCY CHAIN")
print("Vehicle Allocations ,Invoices ,Insurance ,Payments ,Finance ,Service ,Feedback")
print("=" * 60)
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 6, 15)

# # ============================================================
# # STEP 1: VEHICLE ALLOCATIONS
# # ============================================================
# print("\n STEP 1: Vehicle Allocations...")

# # Get Confirmed/Delivered bookings that don't have allocations yet
# cursor.execute("""
#     SELECT b.booking_id, b.model_name, b.variant, b.color_preference, b.fuel_type, b.transmission, b.booking_date
#     FROM bookings b
#     LEFT JOIN vehicle_allocations va ON b.booking_id = va.booking_id
#     WHERE b.status IN ('Confirmed', 'Delivered')
#     AND va.allocation_id IS NULL
# """)
# unallocated_bookings = cursor.fetchall()

# # Get available vehicles matching the booking requirements
# cursor.execute("SELECT vehicle_id, model_name, variant, color, fuel_type, transmission, ex_showroom_price FROM vehicles WHERE status = 'Available'")
# available_vehicles = cursor.fetchall()

# allocations_data = []
# used_vehicle_ids = set()

# for booking in unallocated_bookings:
#     booking_id, model, variant, color, fuel, trans, booking_date_str = booking
#     booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d')
    
#     # Find matching vehicle
#     matching = [v for v in available_vehicles 
#                 if v[1] == model and v[0] not in used_vehicle_ids]
    
#     if not matching:
#         matching = [v for v in available_vehicles 
#                     if v[1] == model and v[0] not in used_vehicle_ids]
    
#     if not matching:
#         matching = [v for v in available_vehicles if v[0] not in used_vehicle_ids]
    
#     if matching:
#         vehicle = random.choice(matching)
#         vehicle_id = vehicle[0]
#         used_vehicle_ids.add(vehicle_id)
        
#         allocated_date = booking_date + timedelta(days=random.randint(1, 5))
#         if allocated_date > END_DATE:
#             allocated_date = END_DATE - timedelta(days=1)
        
#         allocations_data.append((
#             booking_id, vehicle_id, allocated_date.strftime('%Y-%m-%d'), 'Allocated'
#         ))

# cursor.executemany("""
#     INSERT INTO vehicle_allocations (booking_id, vehicle_id, allocated_date, allocation_status)
#     VALUES (?, ?, ?, ?)
# """, allocations_data)
# conn.commit()
# print(f"    {cursor.rowcount} vehicle allocations created")

# # Update vehicle status to Allocated
# for _, vehicle_id, _, _ in allocations_data:
#     cursor.execute("UPDATE vehicles SET status = 'Allocated' WHERE vehicle_id = ?", (vehicle_id,))
# conn.commit()

# # ============================================================
# # STEP 2: INVOICES
# # ============================================================
# print("\n STEP 2: Invoices...")

# cursor.execute("""
#     SELECT va.allocation_id, va.booking_id, va.vehicle_id, va.allocated_date,
#            b.customer_id, b.employee_id, b.model_name, b.booking_amount,
#            v.ex_showroom_price, v.color, v.fuel_type, v.transmission
#     FROM vehicle_allocations va
#     JOIN bookings b ON va.booking_id = b.booking_id
#     JOIN vehicles v ON va.vehicle_id = v.vehicle_id
#     WHERE b.status IN ('Confirmed', 'Delivered')
# """)
# allocation_rows = cursor.fetchall()

# invoices_data = []
# invoice_num = 10001

# for alloc in allocation_rows:
#     alloc_id, booking_id, vehicle_id, alloc_date_str, cust_id, emp_id, model, booking_amt, ex_price, color, fuel, trans = alloc
#     alloc_date = datetime.strptime(alloc_date_str, '%Y-%m-%d')
    
#     invoice_date = alloc_date + timedelta(days=random.randint(1, 3))
#     if invoice_date > END_DATE:
#         invoice_date = END_DATE - timedelta(days=1)
    
#     rto = round(ex_price * 0.10, 2)
#     insurance_premium = round(ex_price * random.uniform(0.025, 0.04), 2)
#     accessories = round(random.uniform(15000, 80000), 2)
#     discount = round(ex_price * random.uniform(0.01, 0.05), 2)
#     tax = round((ex_price + rto + accessories - discount) * 0.28, 2)  # GST ~28% on cars
#     total = round(ex_price + rto + insurance_premium + accessories + tax - discount, 2)
    
#     invoices_data.append((
#         booking_id, alloc_id, cust_id, emp_id,
#         f"INV-{invoice_num}", invoice_date.strftime('%Y-%m-%d'),
#         ex_price, rto, insurance_premium, accessories, discount, tax, total,
#         random.choice(['Pending', 'Partial', 'Paid'])
#     ))
#     invoice_num += 1

# cursor.executemany("""
#     INSERT INTO invoices (booking_id, allocation_id, customer_id, employee_id, invoice_number,
#                          invoice_date, ex_showroom_price, rto_charges, insurance_premium, 
#                          accessories_amount, discount_amount, tax_amount, total_amount, payment_status)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# """, invoices_data)
# conn.commit()
# print(f"    {cursor.rowcount} invoices generated")

# ============================================================
# STEP 3: INSURANCE POLICIES
# ============================================================
print("\n STEP 3: Insurance Policies...")

cursor.execute("""
    SELECT
        i.invoice_id,
        i.customer_id,
        va.vehicle_id,
        i.invoice_date,
        i.ex_showroom_price,
        i.insurance_premium
    FROM invoices i
    JOIN vehicle_allocations va
        ON i.allocation_id = va.allocation_id
""")           
    

invoice_rows = cursor.fetchall()

print("Insurance Source Rows:", len(invoice_rows))

INSURANCE_PROVIDERS = ['HDFC Ergo', 'ICICI Lombard', 'Bajaj Allianz', 'TATA AIG', 'New India Assurance', 'Oriental Insurance']
INSURANCE_WEIGHTS = [0.25, 0.22, 0.18, 0.15, 0.12, 0.08]

insurance_data = []
policy_num = 50001

for inv in invoice_rows:
    inv_id, cust_id, vehicle_id, inv_date_str, ex_price, premium = inv
    inv_date = datetime.strptime(inv_date_str, '%Y-%m-%d')
    
    provider = random.choices(INSURANCE_PROVIDERS, INSURANCE_WEIGHTS)[0]
    policy_type = random.choices(['Comprehensive', 'Third Party', 'Zero Dep', 'Return to Invoice'], [0.55, 0.15, 0.20, 0.10])[0]
    
    # Commission is ~10-15% of premium
    commission = round(premium * random.uniform(0.10, 0.15), 2)
    idv = round(ex_price * random.uniform(0.85, 0.95), 2)
    
    start_date = inv_date
    end_date = start_date + timedelta(days=365)
    
    insurance_data.append((
        inv_id, cust_id, vehicle_id,
        f"POL-{policy_num}", provider, policy_type,
        premium, idv, commission,
        start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), 'Active'
    ))
    policy_num += 1

cursor.executemany("""
    INSERT INTO insurance_policies (invoice_id, customer_id, vehicle_id, policy_number, 
                                   insurance_provider, policy_type, premium_amount, idv_amount, 
                                   commission_amount, start_date, end_date, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", insurance_data)
conn.commit()
print(f"    {cursor.rowcount} insurance policies generated")

# ============================================================
# STEP 4: PAYMENTS
# ============================================================
print("\n STEP 4: Payments...")

cursor.execute("""
    SELECT invoice_id, customer_id, total_amount, invoice_date, payment_status
    FROM invoices
""")
inv_payment_rows = cursor.fetchall()

payments_data = []
payment_num = 1

for inv in inv_payment_rows:
    inv_id, cust_id, total, inv_date_str, pay_status = inv
    inv_date = datetime.strptime(inv_date_str, '%Y-%m-%d')
    
    if pay_status == 'Paid':
        # Full payment
        payments_data.append((
            inv_id, cust_id, inv_date.strftime('%Y-%m-%d'), total,
            random.choice(['UPI', 'Card', 'Bank Transfer', 'Cheque']),
            f"TXN{payment_num:06d}", 'Full Payment', 'Completed'
        ))
        payment_num += 1
    elif pay_status == 'Partial':
        # Multiple payments
        first_amount = round(total * random.uniform(0.30, 0.60), 2)
        remaining = round(total - first_amount, 2)
        
        payments_data.append((
            inv_id, cust_id, inv_date.strftime('%Y-%m-%d'), first_amount,
            random.choice(['UPI', 'Card', 'Bank Transfer']),
            f"TXN{payment_num:06d}", 'Down Payment', 'Completed'
        ))
        payment_num += 1
        
        second_date = inv_date + timedelta(days=random.randint(7, 30))
        if second_date <= END_DATE:
            payments_data.append((
                inv_id, cust_id, second_date.strftime('%Y-%m-%d'), remaining,
                random.choice(['UPI', 'Card', 'Bank Transfer', 'Cheque']),
                f"TXN{payment_num:06d}", 'Full Payment', 'Completed'
            ))
            payment_num += 1
    else:  # Pending - just booking amount paid
        booking_paid = random.choice([25000, 50000])
        payments_data.append((
            inv_id, cust_id, inv_date.strftime('%Y-%m-%d'), booking_paid,
            random.choice(['Cash', 'UPI', 'Card']),
            f"TXN{payment_num:06d}", 'Booking', 'Completed'
        ))
        payment_num += 1

cursor.executemany("""
    INSERT INTO payments (invoice_id, customer_id, payment_date, amount, payment_mode, 
                         transaction_reference, payment_type, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", payments_data)
conn.commit()
print(f"    {cursor.rowcount} payments generated")

# ============================================================
# STEP 5: FINANCE APPLICATIONS
# ============================================================
print("\n STEP 5: Finance Applications...")

# 40% of invoices have finance
cursor.execute("SELECT invoice_id, customer_id, total_amount, invoice_date FROM invoices")
all_invoices = cursor.fetchall()
financed_invoices = random.sample(all_invoices, int(len(all_invoices) * 0.40))

BANKS = ['HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank', 'Kotak Mahindra', 'Bank of Baroda', 'Canara Bank']
BANK_WEIGHTS = [0.25, 0.22, 0.20, 0.15, 0.10, 0.05, 0.03]

finance_data = []
for inv in financed_invoices:
    inv_id, cust_id, total, inv_date_str = inv
    inv_date = datetime.strptime(inv_date_str, '%Y-%m-%d')
    
    bank = random.choices(BANKS, BANK_WEIGHTS)[0]
    loan_amount = round(total * random.uniform(0.60, 0.85), 2)
    interest_rate = round(random.uniform(8.5, 12.5), 2)
    tenure = random.choice([36, 48, 60, 72, 84])
    
    # EMI = P * r * (1+r)^n / ((1+r)^n - 1)
    r = interest_rate / (12 * 100)
    emi = round(loan_amount * r * (1 + r)**tenure / ((1 + r)**tenure - 1), 2)
    processing_fee = round(loan_amount * 0.015, 2)
    
    app_date = inv_date - timedelta(days=random.randint(3, 10))
    
    status_roll = random.random()
    if status_roll < 0.75:
        status = 'Disbursed'
        approval_date = app_date + timedelta(days=random.randint(2, 5))
        disbursement_date = approval_date + timedelta(days=random.randint(1, 3))
    elif status_roll < 0.90:
        status = 'Approved'
        approval_date = app_date + timedelta(days=random.randint(2, 5))
        disbursement_date = None
    elif status_roll < 0.95:
        status = 'Applied'
        approval_date = None
        disbursement_date = None
    else:
        status = 'Rejected'
        approval_date = app_date + timedelta(days=random.randint(3, 7))
        disbursement_date = None
    
    finance_data.append((
        inv_id, cust_id, bank, loan_amount, interest_rate, tenure, emi, processing_fee,
        app_date.strftime('%Y-%m-%d'),
        approval_date.strftime('%Y-%m-%d') if approval_date else None,
        disbursement_date.strftime('%Y-%m-%d') if disbursement_date else None,
        status
    ))

cursor.executemany("""
    INSERT INTO finance_applications (invoice_id, customer_id, bank_name, loan_amount, 
                                      interest_rate, tenure_months, emi_amount, processing_fee,
                                      application_date, approval_date, disbursement_date, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", finance_data)
conn.commit()
print(f"    {cursor.rowcount} finance applications generated")

# ============================================================
# STEP 6: REPAIR ORDERS (SERVICE)
# ============================================================
print("\n STEP 6: Repair Orders (Service)...")

cursor.execute("SELECT customer_id FROM customers")
all_customers = [r[0] for r in cursor.fetchall()]

cursor.execute("SELECT employee_id FROM employees WHERE department = 'Service'")
service_emps = [r[0] for r in cursor.fetchall()]

cursor.execute("SELECT vehicle_id FROM vehicles WHERE status IN ('Allocated', 'Sold')")
service_vehicles = [r[0] for r in cursor.fetchall()]

RO_TYPES = ['Scheduled Service', 'General Repair', 'Body Shop', 'Warranty', 'Recall']
RO_WEIGHTS = [0.55, 0.25, 0.10, 0.07, 0.03]

repair_orders_data = []
ro_num = 1001

for i in range(400):
    cust_id = random.choice(all_customers)
    vehicle_id = random.choice(service_vehicles) if service_vehicles else None
    emp_id = random.choice(service_emps)
    
    ro_date = random_date(START_DATE, END_DATE)
    ro_type = random.choices(RO_TYPES, RO_WEIGHTS)[0]
    mileage = random.randint(1000, 150000)
    
    est_cost = round(random.uniform(1500, 25000), 2)
    actual_cost = round(est_cost * random.uniform(0.85, 1.25), 2)
    
    status_roll = random.random()
    if status_roll < 0.70:
        status = 'Completed'
        completion = ro_date + timedelta(days=random.randint(0, 3))
        if completion > END_DATE:
            completion = END_DATE
        rating = random.choices([5, 4, 3, 2, 1], [0.40, 0.35, 0.15, 0.07, 0.03])[0]
    elif status_roll < 0.85:
        status = 'In Progress'
        completion = None
        rating = None
    elif status_roll < 0.95:
        status = 'Open'
        completion = None
        rating = None
    else:
        status = 'Cancelled'
        completion = None
        rating = None
    
    repair_orders_data.append((
        cust_id, vehicle_id, emp_id, f"RO-{ro_num}",
        ro_date.strftime('%Y-%m-%d'), ro_type, mileage,
        est_cost, actual_cost, status,
        completion.strftime('%Y-%m-%d') if completion else None,
        rating
    ))
    ro_num += 1

cursor.executemany("""
    INSERT INTO repair_orders (customer_id, vehicle_id, employee_id, ro_number, ro_date, 
                              ro_type, mileage_km, estimated_cost, actual_cost, status, 
                              completion_date, customer_feedback_rating)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", repair_orders_data)
conn.commit()
print(f" {cursor.rowcount} repair orders generated")

# ============================================================
# STEP 7: REPAIR ORDER ITEMS
# ============================================================
print("\n STEP 7: Repair Order Items...")

cursor.execute("SELECT ro_id, actual_cost, ro_type FROM repair_orders WHERE status = 'Completed'")
completed_ros = cursor.fetchall()

cursor.execute("SELECT employee_id FROM employees WHERE department = 'Service' AND designation LIKE '%Technician%'")
techs = [r[0] for r in cursor.fetchall()]
if not techs:
    cursor.execute("SELECT employee_id FROM employees WHERE department = 'Service'")
    techs = [r[0] for r in cursor.fetchall()]

SERVICE_ITEMS = {
    'Scheduled Service': [
        ('Labour', 'General Service Labour', 0.30),
        ('Oil', 'Engine Oil 5W-30', 0.15),
        ('Part', 'Oil Filter', 0.05),
        ('Part', 'Air Filter', 0.05),
        ('Part', 'Cabin Filter', 0.05),
        ('Consumable', 'Brake Fluid', 0.05),
        ('Consumable', 'Coolant', 0.05),
        ('Labour', 'Washing & Polishing', 0.10),
        ('Part', 'Spark Plugs', 0.08),
        ('Consumable', 'Grease & Lubricants', 0.12)
    ],
    'General Repair': [
        ('Labour', 'Diagnostic Labour', 0.20),
        ('Part', 'Brake Pads', 0.20),
        ('Part', 'Clutch Plate', 0.15),
        ('Part', 'Battery', 0.15),
        ('Labour', 'Repair Labour', 0.20),
        ('Consumable', 'Wiring & Connectors', 0.10)
    ],
    'Body Shop': [
        ('Labour', 'Denting Labour', 0.25),
        ('Labour', 'Painting Labour', 0.25),
        ('Part', 'Bumper', 0.15),
        ('Part', 'Fender', 0.10),
        ('Consumable', 'Paint & Polish', 0.15),
        ('Part', 'Headlight Assembly', 0.10)
    ],
    'Warranty': [
        ('Labour', 'Warranty Labour', 0.40),
        ('Part', 'Warranty Part Replacement', 0.35),
        ('Consumable', 'Sealants & Gaskets', 0.25)
    ],
    'Recall': [
        ('Labour', 'Recall Service Labour', 0.50),
        ('Part', 'Recall Part Replacement', 0.30),
        ('Consumable', 'Miscellaneous', 0.20)
    ]
}

ro_items_data = []
for ro in completed_ros:
    ro_id, actual_cost, ro_type = ro
    items = SERVICE_ITEMS.get(ro_type, SERVICE_ITEMS['General Repair'])
    
    # Select 3-6 items per RO
    num_items = random.randint(3, min(6, len(items)))
    selected_items = random.sample(items, num_items)
    
    for item_type, item_name, weight in selected_items:
        qty = random.randint(1, 3) if item_type in ['Part', 'Oil', 'Consumable'] else 1
        unit_price = round((actual_cost * weight) / qty, 2)
        total = round(unit_price * qty, 2)
        tech_id = random.choice(techs) if techs else None
        
        ro_items_data.append((ro_id, item_type, item_name, qty, unit_price, total, tech_id))

cursor.executemany("""
    INSERT INTO repair_order_items (ro_id, item_type, item_name, quantity, unit_price, total_price, technician_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", ro_items_data)
conn.commit()
print(f"    {cursor.rowcount} repair order items generated")

# ============================================================
# STEP 8: CUSTOMER FEEDBACK
# ============================================================
print("\n STEP 8: Customer Feedback...")

cursor.execute("SELECT booking_id, customer_id FROM bookings WHERE status = 'Delivered'")
delivered_bookings = cursor.fetchall()

cursor.execute("SELECT ro_id, customer_id FROM repair_orders WHERE status = 'Completed'")
completed_service = cursor.fetchall()

feedback_data = []

# Sales feedback
for booking in delivered_bookings:
    booking_id, cust_id = booking
    fb_date = random_date(START_DATE, END_DATE)
    
    overall = random.choices([5, 4, 3, 2, 1], [0.45, 0.30, 0.15, 0.07, 0.03])[0]
    staff = random.choices([5, 4, 3, 2, 1], [0.40, 0.35, 0.15, 0.07, 0.03])[0]
    process = random.choices([5, 4, 3, 2, 1], [0.35, 0.35, 0.18, 0.08, 0.04])[0]
    facility = random.choices([5, 4, 3, 2, 1], [0.40, 0.30, 0.18, 0.08, 0.04])[0]
    nps = random.choices([9, 10, 8, 7, 6, 5, 4, 3, 2, 1, 0], 
                         [0.25, 0.30, 0.15, 0.10, 0.07, 0.05, 0.03, 0.02, 0.01, 0.01, 0.01])[0]
    
    comments = random.choice([
        'Excellent experience!', 'Very satisfied with the service', 'Smooth process',
        'Staff was very helpful', 'Good value for money', 'Would recommend to friends',
        'Delivery was on time', 'Some delays in paperwork', 'Overall good experience',
        'Showroom is well maintained', 'Finance process was smooth'
    ])
    
    feedback_data.append((
        cust_id, booking_id, None, 'Sales', overall, staff, process, facility, comments, fb_date.strftime('%Y-%m-%d'), nps
    ))

# Service feedback
for ro in completed_service:
    ro_id, cust_id = ro
    fb_date = random_date(START_DATE, END_DATE)
    
    overall = random.choices([5, 4, 3, 2, 1], [0.40, 0.32, 0.18, 0.07, 0.03])[0]
    staff = random.choices([5, 4, 3, 2, 1], [0.38, 0.33, 0.17, 0.08, 0.04])[0]
    process = random.choices([5, 4, 3, 2, 1], [0.35, 0.32, 0.20, 0.09, 0.04])[0]
    facility = random.choices([5, 4, 3, 2, 1], [0.38, 0.30, 0.20, 0.08, 0.04])[0]
    nps = random.choices([9, 10, 8, 7, 6, 5, 4, 3, 2, 1, 0], 
                         [0.22, 0.28, 0.16, 0.12, 0.08, 0.05, 0.03, 0.02, 0.02, 0.01, 0.01])[0]
    
    comments = random.choice([
        'Service was quick', 'Technician explained everything well', 'Waiting area is comfortable',
        'Car was cleaned properly', 'Minor issues still persist', 'Good quality service',
        'Transparent pricing', 'Will come back for next service', 'Satisfied with the repair',
        'Service advisor was knowledgeable'
    ])
    
    feedback_data.append((
        cust_id, None, ro_id, 'Service', overall, staff, process, facility, comments, fb_date.strftime('%Y-%m-%d'), nps
    ))

cursor.executemany("""
    INSERT INTO customer_feedback (customer_id, booking_id, ro_id, feedback_type, overall_rating, 
                                  staff_knowledge_rating, process_rating, facility_rating, 
                                  comments, feedback_date, is_nps)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", feedback_data)
conn.commit()
print(f"    {cursor.rowcount} customer feedback records generated")

print("\n" + "=" * 60)
print("PHASE 3 COMPLETE: ALL TABLES POPULATED SUCCESSFULLY!")
print("=" * 60)

# Verify all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print("\n TABLE COUNTS:")
for table in tables:
    tname = table[0]
    if tname != 'sqlite_sequence':
        cursor.execute(f"SELECT COUNT(*) FROM {tname}")
        count = cursor.fetchone()[0]
        print(f"   {tname:30s}: {count:4d} records")

conn.close()

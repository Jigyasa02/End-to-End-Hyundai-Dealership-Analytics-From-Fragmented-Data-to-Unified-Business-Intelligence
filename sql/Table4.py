
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('hyundai_dealership.db')
cursor = conn.cursor()

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 6, 15)

print("=" * 60)
print("PHASE 3 (CONTINUED): ENQUIRIES, TEST DRIVES, BOOKINGS")
print("=" * 60)

# ============================================================
# GENERATE ENQUIRIES (500 enquiries)
# ============================================================
print("\n Generating Enquiries...")

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


# Get customer IDs and sales employee IDs
cursor.execute("SELECT customer_id FROM customers")
customer_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT employee_id FROM employees WHERE department = 'Sales'")
sales_emp_ids = [row[0] for row in cursor.fetchall()]

ENQUIRY_SOURCES = ['Walk-in', 'Phone', 'Website', 'Referral', 'Google Ads', 'Social Media', 'CarDekho', 'CarWale']
SOURCE_WEIGHTS = [0.30, 0.15, 0.15, 0.12, 0.10, 0.08, 0.05, 0.05]

PURCHASE_TIMELINES = ['Immediate', '1-3 months', '3-6 months', '6+ months']
TIMELINE_WEIGHTS = [0.15, 0.35, 0.30, 0.20]

MODELS_LIST = ['Creta', 'Venue', 'Verna', 'i20', 'Alcazar', 'Exter', 'Tucson', 'i10']
MODEL_WEIGHTS = [0.35, 0.20, 0.12, 0.10, 0.08, 0.07, 0.05, 0.03]

enquiries_data = []
for i in range(500):
    cust_id = random.choice(customer_ids)
    emp_id = random.choice(sales_emp_ids)
    source = random.choices(ENQUIRY_SOURCES, SOURCE_WEIGHTS)[0]
    model = random.choices(MODELS_LIST, MODEL_WEIGHTS)[0]
    budget = random.choice(['< 10 Lakh', '10-15 Lakh', '15-20 Lakh', '20-30 Lakh', '> 30 Lakh'])
    timeline = random.choices(PURCHASE_TIMELINES, TIMELINE_WEIGHTS)[0]
    
    # Status: 15% Immediate convert, 35% follow-up, 30% open, 20% lost
    status_roll = random.random()
    if status_roll < 0.15:
        status = 'Converted'
    elif status_roll < 0.50:
        status = 'Follow-up'
    elif status_roll < 0.80:
        status = 'Open'
    else:
        status = 'Lost'

        
    
    enquiry_date = random_date(START_DATE, END_DATE)
    follow_up = enquiry_date + timedelta(days=random.randint(3, 14)) if status in ['Open', 'Follow-up'] else None
    
    enquiries_data.append((
        cust_id, emp_id, source, model, budget, timeline, status,
        enquiry_date.strftime('%Y-%m-%d'),
        follow_up.strftime('%Y-%m-%d') if follow_up else None,
        f"Customer interested in {model}. Budget: {budget}."
    ))

cursor.executemany("""
    INSERT INTO enquiries (customer_id, employee_id, source, interested_model, budget_range, 
                          purchase_timeline, status, enquiry_date, follow_up_date, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", enquiries_data)
conn.commit()
print(f" {cursor.rowcount} enquiries generated")

# ============================================================
# GENERATE TEST DRIVES (350 test drives from enquiries)
# ============================================================
print("\n Generating Test Drives...")

# Get converted and follow-up enquiries
cursor.execute("SELECT enquiry_id, customer_id, employee_id, interested_model, enquiry_date FROM enquiries WHERE status IN ('Converted', 'Follow-up', 'Open')")
enquiry_rows = cursor.fetchall()

# Get demo vehicles (first 20 vehicles marked as demo)
cursor.execute("SELECT vehicle_id, model_name FROM vehicles LIMIT 20")
demo_vehicles = cursor.fetchall()

test_drives_data = []
selected_enquiries = random.sample(enquiry_rows, min(350, len(enquiry_rows)))

for enquiry in selected_enquiries:
    enquiry_id, cust_id, emp_id, model, enquiry_date = enquiry

    # Convert SQLite string to datetime
    enquiry_date = datetime.strptime(enquiry_date, '%Y-%m-%d')

    # Test drive happens 1-7 days after enquiry
    td_date = enquiry_date + timedelta(days=random.randint(1, 7))
    if td_date > END_DATE:
        td_date = END_DATE - timedelta(days=1)
    
    # Find matching demo vehicle or random
    matching_demos = [v for v in demo_vehicles if v[1] == model]
    vehicle_id = random.choice(matching_demos)[0] if matching_demos else random.choice(demo_vehicles)[0]
    
    duration = random.randint(15, 60)
    rating = random.choices([5, 4, 3, 2, 1], [0.45, 0.30, 0.15, 0.07, 0.03])[0]
    
    # Outcome based on rating
    if rating >= 4:
        outcome = random.choices(['Booked', 'Interested', 'Follow-up'], [0.40, 0.35, 0.25])[0]
    elif rating == 3:
        outcome = random.choices(['Interested', 'Follow-up', 'Not Interested'], [0.30, 0.40, 0.30])[0]
    else:
        outcome = random.choices(['Not Interested', 'Follow-up'], [0.70, 0.30])[0]
    
    comments = random.choice([
        'Loved the driving experience', 'Good pickup and comfort', 'Suspension felt smooth',
        'Interior quality is excellent', 'Mileage seems good', 'Features are impressive',
        'Price is slightly high', 'Comparing with competitors', 'Need to discuss with family',
        'Will decide after finance approval'
    ])
    
    test_drives_data.append((
        enquiry_id, cust_id, emp_id, vehicle_id,
        td_date.strftime('%Y-%m-%d'), duration, rating, comments, outcome
    ))

cursor.executemany("""
    INSERT INTO test_drives (enquiry_id, customer_id, employee_id, vehicle_id, 
                            test_drive_date, duration_minutes, feedback_rating, 
                            feedback_comments, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", test_drives_data)
conn.commit()
print(f" {cursor.rowcount} test drives generated")

# ============================================================
# GENERATE BOOKINGS (180 bookings from test drives)
# ============================================================
print("\n Generating Bookings...")

# Get test drives that resulted in booking or interest
cursor.execute("""
    SELECT td.test_drive_id, td.enquiry_id, td.customer_id, td.employee_id, 
           td.test_drive_date, e.interested_model
    FROM test_drives td
    JOIN enquiries e ON td.enquiry_id = e.enquiry_id
    WHERE td.outcome IN ('Booked', 'Interested')
""")
td_rows = cursor.fetchall()

# Select ~180 bookings (50% conversion from test drives with positive outcome)
booking_candidates = random.sample(td_rows, min(180, len(td_rows)))

bookings_data = []
for td in booking_candidates:
    td_id, enq_id, cust_id, emp_id, td_date, model = td

    # Convert SQLite string to datetime
    td_date = datetime.strptime(td_date, '%Y-%m-%d')

    # Booking happens 0-5 days after test drive
    booking_date = td_date + timedelta(days=random.randint(0, 5))
    if booking_date > END_DATE:
        booking_date = END_DATE - timedelta(days=2)
    
    # Get model details
    cursor.execute("SELECT variant, fuel_type, transmission, color FROM vehicles WHERE model_name = ? LIMIT 5", (model,))
    model_vehicles = cursor.fetchall()
    if model_vehicles:
        variant, fuel, trans, color = random.choice(model_vehicles)
    else:
        variant, fuel, trans, color = 'SX', 'Petrol', 'Manual', 'Polar White'
    
    booking_amount = random.choice([25000, 50000, 75000, 100000])
    
    # Expected delivery: 7-30 days after booking
    expected_delivery = booking_date + timedelta(days=random.randint(7, 30))
    
    # 5% cancelled, 85% confirmed, 10% delivered
    status_roll = random.random()
    if status_roll < 0.05:
        status = 'Cancelled'
    elif status_roll < 0.15:
        status = 'Delivered'
    else:
        status = 'Confirmed'
    
    bookings_data.append((
        cust_id, emp_id, enq_id, td_id, model, variant, color, fuel, trans,
        booking_amount, booking_date.strftime('%Y-%m-%d'),
        expected_delivery.strftime('%Y-%m-%d'), status,
        random.choice(['Cash', 'Cheque', 'UPI', 'Card', 'Bank Transfer'])
    ))

cursor.executemany("""
    INSERT INTO bookings (customer_id, employee_id, enquiry_id, test_drive_id, model_name, 
                         variant, color_preference, fuel_type, transmission, booking_amount, 
                         booking_date, expected_delivery_date, status, payment_mode)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", bookings_data)
conn.commit()
print(f"{cursor.rowcount} bookings generated")

print("\n Phase 3 Part 2 Complete: Enquiries, Test Drives, Bookings created!")




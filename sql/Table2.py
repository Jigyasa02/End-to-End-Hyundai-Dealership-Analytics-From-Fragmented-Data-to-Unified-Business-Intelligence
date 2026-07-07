
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Create database
conn = sqlite3.connect('hyundai_dealership.db')
cursor = conn.cursor()

print("=" * 60)
print("PHASE 1 & 2: DATABASE SCHEMA CREATION")
print("=" * 60)

# Drop all existing tables to start fresh
cursor.executescript("""
DROP TABLE IF EXISTS customer_feedback;
DROP TABLE IF EXISTS finance_applications;
DROP TABLE IF EXISTS repair_order_items;
DROP TABLE IF EXISTS repair_orders;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS insurance_policies;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS vehicle_allocations;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS test_drives;
DROP TABLE IF EXISTS enquiries;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;
""")

# ============================================================
# TABLE 1: CUSTOMERS
# ============================================================
cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT UNIQUE,
    address TEXT,
    city TEXT,
    state TEXT,
    pincode TEXT,
    date_of_birth DATE,
    gender TEXT,
    occupation TEXT,
    income_bracket TEXT,
    customer_type TEXT, -- New, Returning, Referral
    created_at DATE DEFAULT CURRENT_DATE,
    updated_at DATE DEFAULT CURRENT_DATE
);
""")

# ============================================================
# TABLE 2: EMPLOYEES
# ============================================================
cursor.execute("""
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    department TEXT, -- Sales, Service, Insurance, Finance, Inventory, Customer Relations
    designation TEXT, -- Manager, Consultant, Advisor, Technician, Executive
    date_of_joining DATE,
    salary DECIMAL(10,2),
    is_active INTEGER DEFAULT 1,
    created_at DATE DEFAULT CURRENT_DATE
);
""")

# ============================================================
# TABLE 3: VEHICLES (INVENTORY)
# ============================================================
cursor.execute("""
CREATE TABLE vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vin TEXT UNIQUE NOT NULL,
    model_name TEXT NOT NULL, -- Creta, Venue, Tucson, Verna, i20, i10, Alcazar, Exter
    variant TEXT, -- SX, SX(O), EX, S, Magna, Sportz
    fuel_type TEXT, -- Petrol, Diesel, CNG, Electric
    transmission TEXT, -- Manual, Automatic, IMT, DCT
    color TEXT,
    manufacturing_year INTEGER,
    ex_showroom_price DECIMAL(12,2),
    cost_price DECIMAL(12,2),
    status TEXT DEFAULT 'Available', -- Available, Allocated, Sold, Reserved, Demo
    arrival_date DATE,
    created_at DATE DEFAULT CURRENT_DATE
);
""")

# ============================================================
# TABLE 4: ENQUIRIES (LEADS)
# ============================================================
cursor.execute("""
CREATE TABLE enquiries (
    enquiry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    employee_id INTEGER, -- Assigned sales consultant
    source TEXT, -- Walk-in, Phone, Website, Referral, Google Ads, Social Media
    interested_model TEXT,
    budget_range TEXT,
    purchase_timeline TEXT, -- Immediate, 1-3 months, 3-6 months, 6+ months
    status TEXT DEFAULT 'Open', -- Open, Converted, Lost, Follow-up
    enquiry_date DATE,
    follow_up_date DATE,
    notes TEXT,
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
""")

# ============================================================
# TABLE 5: TEST DRIVES
# ============================================================
cursor.execute("""
CREATE TABLE test_drives (
    test_drive_id INTEGER PRIMARY KEY AUTOINCREMENT,
    enquiry_id INTEGER,
    customer_id INTEGER,
    employee_id INTEGER, -- Accompanying consultant
    vehicle_id INTEGER, -- Demo vehicle used
    test_drive_date DATE,
    duration_minutes INTEGER,
    feedback_rating INTEGER, -- 1-5
    feedback_comments TEXT,
    outcome TEXT, -- Booked, Interested, Not Interested, Follow-up
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (enquiry_id) REFERENCES enquiries(enquiry_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);
""")

# ============================================================
# TABLE 6: BOOKINGS
# ============================================================
cursor.execute("""
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    employee_id INTEGER, -- Sales consultant who closed
    enquiry_id INTEGER,
    test_drive_id INTEGER,
    model_name TEXT,
    variant TEXT,
    color_preference TEXT,
    fuel_type TEXT,
    transmission TEXT,
    booking_amount DECIMAL(10,2),
    booking_date DATE,
    expected_delivery_date DATE,
    status TEXT DEFAULT 'Confirmed', -- Confirmed, Cancelled, Delivered, Pending
    payment_mode TEXT, -- Cash, Cheque, UPI, Card, Bank Transfer
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (enquiry_id) REFERENCES enquiries(enquiry_id),
    FOREIGN KEY (test_drive_id) REFERENCES test_drives(test_drive_id)
);
""")

# ============================================================
# TABLE 7: VEHICLE ALLOCATIONS
# ============================================================
cursor.execute("""
CREATE TABLE vehicle_allocations (
    allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER UNIQUE,
    vehicle_id INTEGER UNIQUE,
    allocated_date DATE,
    allocation_status TEXT DEFAULT 'Allocated', -- Allocated, Delivered, Cancelled
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);
""")

# ============================================================
# TABLE 8: INVOICES
# ============================================================
cursor.execute("""
CREATE TABLE invoices (
    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    allocation_id INTEGER,
    customer_id INTEGER,
    employee_id INTEGER,
    invoice_number TEXT UNIQUE,
    invoice_date DATE,
    ex_showroom_price DECIMAL(12,2),
    rto_charges DECIMAL(10,2),
    insurance_premium DECIMAL(10,2),
    accessories_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    total_amount DECIMAL(12,2),
    payment_status TEXT DEFAULT 'Pending', -- Pending, Partial, Paid
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (allocation_id) REFERENCES vehicle_allocations(allocation_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
""")

# ============================================================
# TABLE 9: INSURANCE POLICIES
# ============================================================
cursor.execute("""
CREATE TABLE insurance_policies (
    policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    customer_id INTEGER,
    vehicle_id INTEGER,
    policy_number TEXT UNIQUE,
    insurance_provider TEXT, -- HDFC Ergo, ICICI Lombard, Bajaj Allianz, TATA AIG, New India Assurance
    policy_type TEXT, -- Comprehensive, Third Party, Zero Dep, Return to Invoice
    premium_amount DECIMAL(10,2),
    idv_amount DECIMAL(12,2), -- Insured Declared Value
    commission_amount DECIMAL(10,2),
    start_date DATE,
    end_date DATE,
    status TEXT DEFAULT 'Active', -- Active, Expired, Cancelled, Renewed
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);
""")

# ============================================================
# TABLE 10: PAYMENTS
# ============================================================
cursor.execute("""
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    customer_id INTEGER,
    payment_date DATE,
    amount DECIMAL(12,2),
    payment_mode TEXT, -- Cash, Cheque, UPI, Card, Bank Transfer, Finance
    transaction_reference TEXT,
    payment_type TEXT, -- Booking, Down Payment, Full Payment, EMI, Service
    status TEXT DEFAULT 'Completed', -- Completed, Failed, Pending, Refunded
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
""")

# ============================================================
# TABLE 11: REPAIR ORDERS (SERVICE)
# ============================================================
cursor.execute("""
CREATE TABLE repair_orders (
    ro_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    vehicle_id INTEGER,
    employee_id INTEGER, -- Service advisor
    ro_number TEXT UNIQUE,
    ro_date DATE,
    ro_type TEXT, -- Scheduled Service, General Repair, Body Shop, Warranty, Recall
    mileage_km INTEGER,
    estimated_cost DECIMAL(10,2),
    actual_cost DECIMAL(10,2),
    status TEXT DEFAULT 'Open', -- Open, In Progress, Completed, Cancelled
    completion_date DATE,
    customer_feedback_rating INTEGER,
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
""")

# ============================================================
# TABLE 12: REPAIR ORDER ITEMS
# ============================================================
cursor.execute("""
CREATE TABLE repair_order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ro_id INTEGER,
    item_type TEXT, -- Labour, Part, Oil, Consumable
    item_name TEXT,
    quantity DECIMAL(8,2),
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2),
    technician_id INTEGER,
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (ro_id) REFERENCES repair_orders(ro_id),
    FOREIGN KEY (technician_id) REFERENCES employees(employee_id)
);
""")

# ============================================================
# TABLE 13: FINANCE APPLICATIONS
# ============================================================
cursor.execute("""
CREATE TABLE finance_applications (
    finance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    customer_id INTEGER,
    bank_name TEXT, -- HDFC Bank, ICICI Bank, SBI, Axis Bank, Kotak Mahindra
    loan_amount DECIMAL(12,2),
    interest_rate DECIMAL(5,2),
    tenure_months INTEGER,
    emi_amount DECIMAL(10,2),
    processing_fee DECIMAL(10,2),
    application_date DATE,
    approval_date DATE,
    disbursement_date DATE,
    status TEXT DEFAULT 'Applied', -- Applied, Approved, Rejected, Disbursed, Closed
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
""")

# ============================================================
# TABLE 14: CUSTOMER FEEDBACK
# ============================================================
cursor.execute("""
CREATE TABLE customer_feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    booking_id INTEGER,
    ro_id INTEGER,
    feedback_type TEXT, -- Sales, Service, Delivery, General
    overall_rating INTEGER, -- 1-5
    staff_knowledge_rating INTEGER,
    process_rating INTEGER,
    facility_rating INTEGER,
    comments TEXT,
    feedback_date DATE,
    is_nps INTEGER, -- Net Promoter Score 0-10
    created_at DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (ro_id) REFERENCES repair_orders(ro_id)
);
""")

conn.commit()
print("All 14 tables created successfully!")
print("   - customers, employees, vehicles, enquiries, test_drives")
print("   - bookings, vehicle_allocations, invoices, insurance_policies")
print("   - payments, repair_orders, repair_order_items, finance_applications, customer_feedback")

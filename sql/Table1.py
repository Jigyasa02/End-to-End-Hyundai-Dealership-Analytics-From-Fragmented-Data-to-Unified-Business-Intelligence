
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('hyundai_dealership.db')
cursor = conn.cursor()

print("=" * 60)
print("PHASE 3: DATA GENERATION - REALISTIC DEALERSHIP DATA")
print("=" * 60)

# ============================================================
# CONFIGURATION
# ============================================================
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 6, 15)
DATE_RANGE = (END_DATE - START_DATE).days

# Hyundai models with realistic pricing
MODELS = {
    'Creta': {'variants': ['E', 'S', 'SX', 'SX(O)'], 'price_range': (1150000, 2100000), 'popularity': 0.35},
    'Venue': {'variants': ['E', 'S', 'SX', 'SX(O)'], 'price_range': (800000, 1350000), 'popularity': 0.20},
    'Verna': {'variants': ['EX', 'S', 'SX', 'SX(O)'], 'price_range': (1100000, 1700000), 'popularity': 0.12},
    'i20': {'variants': ['Magna', 'Sportz', 'Asta', 'Asta(O)'], 'price_range': (720000, 1150000), 'popularity': 0.10},
    'Alcazar': {'variants': ['Prestige', 'Platinum', 'Signature'], 'price_range': (1650000, 2150000), 'popularity': 0.08},
    'Exter': {'variants': ['EX', 'S', 'SX', 'SX(O)'], 'price_range': (650000, 1050000), 'popularity': 0.07},
    'Tucson': {'variants': ['GLS', 'GLS(O)'], 'price_range': (2900000, 3600000), 'popularity': 0.05},
    'i10': {'variants': ['Era', 'Magna', 'Sportz', 'Asta'], 'price_range': (550000, 850000), 'popularity': 0.03}
}

COLORS = ['Polar White', 'Phantom Black', 'Typhoon Silver', 'Titan Grey', 'Star Gaze Blue', 
          'Fiery Red', 'Atlas White', 'Abyss Black', 'Olive Green', 'Midnight Blue']
COLOR_WEIGHTS = [0.25, 0.18, 0.15, 0.12, 0.10, 0.08, 0.05, 0.04, 0.02, 0.01]  # White most common

FUEL_TYPES = ['Petrol', 'Diesel', 'CNG', 'Electric']
FUEL_WEIGHTS = [0.55, 0.25, 0.15, 0.05]

TRANSMISSIONS = ['Manual', 'Automatic', 'IMT', 'DCT']
TRANSMISSION_WEIGHTS = [0.40, 0.35, 0.15, 0.10]

FIRST_NAMES_M = ['Rahul', 'Amit', 'Vikram', 'Rajesh', 'Suresh', 'Anil', 'Deepak', 'Sanjay', 
                 'Manish', 'Karan', 'Arjun', 'Nikhil', 'Rohit', 'Vivek', 'Pankaj', 'Sandeep',
                 'Abhishek', 'Siddharth', 'Aditya', 'Harsh', 'Kunal', 'Gaurav', 'Varun', 'Ashish']
FIRST_NAMES_F = ['Priya', 'Neha', 'Anjali', 'Pooja', 'Sneha', 'Divya', 'Shweta', 'Kavita',
                 'Ritu', 'Meera', 'Aarti', 'Sunita', 'Nisha', 'Rekha', 'Geeta', 'Monica',
                 'Rashmi', 'Jyoti', 'Sonia', 'Deepika', 'Kriti', 'Ananya', 'Isha', 'Tanvi']
LAST_NAMES = ['Sharma', 'Kumar', 'Singh', 'Patel', 'Gupta', 'Verma', 'Reddy', 'Nair',
              'Joshi', 'Desai', 'Mehta', 'Shah', 'Rao', 'Iyer', 'Agarwal', 'Bansal',
              'Choudhary', 'Yadav', 'Pandey', 'Mishra', 'Tiwari', 'Dubey', 'Saxena', 'Malhotra']

CITIES = ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Thane', 'Aurangabad', 'Solapur', 'Kolhapur']
STATES = ['Maharashtra']

OCCUPATIONS = ['IT Professional', 'Business Owner', 'Government Employee', 'Doctor', 'Engineer',
               'Teacher', 'Accountant', 'Sales Manager', 'Consultant', 'Architect', 'Lawyer',
               'Bank Manager', 'Real Estate Agent', 'Retired', 'Student', 'Freelancer']

INCOME_BRACKETS = ['< 5 LPA', '5-10 LPA', '10-15 LPA', '15-25 LPA', '25-40 LPA', '> 40 LPA']
INCOME_WEIGHTS = [0.10, 0.25, 0.30, 0.20, 0.10, 0.05]

ENQUIRY_SOURCES = ['Walk-in', 'Phone', 'Website', 'Referral', 'Google Ads', 'Social Media', 'CarDekho', 'CarWale']
SOURCE_WEIGHTS = [0.30, 0.15, 0.15, 0.12, 0.10, 0.08, 0.05, 0.05]

PURCHASE_TIMELINES = ['Immediate', '1-3 months', '3-6 months', '6+ months']
TIMELINE_WEIGHTS = [0.15, 0.35, 0.30, 0.20]

INSURANCE_PROVIDERS = ['HDFC Ergo', 'ICICI Lombard', 'Bajaj Allianz', 'TATA AIG', 'New India Assurance', 'Oriental Insurance']
INSURANCE_WEIGHTS = [0.25, 0.22, 0.18, 0.15, 0.12, 0.08]

BANKS = ['HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank', 'Kotak Mahindra', 'Bank of Baroda', 'Canara Bank']
BANK_WEIGHTS = [0.25, 0.22, 0.20, 0.15, 0.10, 0.05, 0.03]

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def random_phone():
    return f"9{random.randint(100000000, 999999999)}"

def random_email(first, last):
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'rediffmail.com']
    return f"{first.lower()}.{last.lower()}{random.randint(1,999)}@{random.choice(domains)}"

def random_pincode():
    return f"{random.randint(400000, 445000)}"

# ============================================================
# GENERATE CUSTOMERS (300 customers)
# ============================================================
print("\n Generating Customers...")
customers_data = []
for i in range(300):
    gender = random.choice(['M', 'F'])
    first = random.choice(FIRST_NAMES_M if gender == 'M' else FIRST_NAMES_F)
    last = random.choice(LAST_NAMES)
    dob = random_date(datetime(1965, 1, 1), datetime(2005, 12, 31))
    city = random.choice(CITIES)
    income = random.choices(INCOME_BRACKETS, INCOME_WEIGHTS)[0]
    
    customers_data.append((
        first, last, random_email(first, last), random_phone(),
        f"{random.randint(1, 999)}, {random.choice(['Main Road', 'Station Road', 'Market Area', 'Residential Colony', 'High Street'])}",
        city, 'Maharashtra', random_pincode(),
        dob.strftime('%Y-%m-%d'), 'Male' if gender == 'M' else 'Female',
        random.choice(OCCUPATIONS), income,
        random.choice(['New', 'Returning', 'Referral']),
        random_date(START_DATE, END_DATE).strftime('%Y-%m-%d')
    ))

cursor.executemany("""
    INSERT INTO customers (first_name, last_name, email, phone, address, city, state, pincode, 
                          date_of_birth, gender, occupation, income_bracket, customer_type, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", customers_data)
conn.commit()
print(f" {cursor.rowcount} customers generated")

# ============================================================
# GENERATE EMPLOYEES (25 employees)
# ============================================================
print("\nGenerating Employees...")
departments = {
    'Sales': ['Manager', 'Senior Consultant', 'Sales Consultant', 'Sales Executive'],
    'Service': ['Manager', 'Service Advisor', 'Senior Technician', 'Technician', 'Detailing Expert'],
    'Insurance': ['Manager', 'Insurance Advisor', 'Insurance Executive'],
    'Finance': ['Manager', 'Finance Advisor', 'Finance Executive'],
    'Inventory': ['Manager', 'Inventory Executive', 'Logistics Coordinator'],
    'Customer Relations': ['Manager', 'CRM Executive', 'Receptionist']
}

employees_data = []
emp_id = 1
for dept, roles in departments.items():
    for role in roles:
        count = 1 if 'Manager' in role else random.randint(1, 3)
        for _ in range(count):
            gender = random.choice(['M', 'F'])
            first = random.choice(FIRST_NAMES_M if gender == 'M' else FIRST_NAMES_F)
            last = random.choice(LAST_NAMES)
            doj = random_date(datetime(2018, 1, 1), datetime(2025, 12, 31))
            salary = 25000 if 'Manager' in role else (18000 if 'Senior' in role else 15000)
            salary += random.randint(-3000, 15000)
            
            employees_data.append((
                first, last, f"{first.lower()}.{last.lower()}{emp_id}@gurukripahyundai.com",
                random_phone(), dept, role, doj.strftime('%Y-%m-%d'), salary, 1,
                doj.strftime('%Y-%m-%d')
            ))
            emp_id += 1

cursor.executemany("""
    INSERT INTO employees (first_name, last_name, email, phone, department, designation, 
                          date_of_joining, salary, is_active, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", employees_data)
conn.commit()
print(f" {cursor.rowcount} employees generated")

# ============================================================
# GENERATE VEHICLES (200 vehicles)
# ============================================================
print("\n Generating Vehicles...")
vehicles_data = []
for i in range(200):
    model = random.choices(list(MODELS.keys()), [MODELS[m]['popularity'] for m in MODELS])[0]
    variant = random.choice(MODELS[model]['variants'])
    fuel = random.choices(FUEL_TYPES, FUEL_WEIGHTS)[0]
    trans = random.choices(TRANSMISSIONS, TRANSMISSION_WEIGHTS)[0]
    color = random.choices(COLORS, COLOR_WEIGHTS)[0]
    
    # Price based on variant and fuel
    base_price = MODELS[model]['price_range'][0]
    max_price = MODELS[model]['price_range'][1]
    variant_idx = MODELS[model]['variants'].index(variant)
    price = base_price + (max_price - base_price) * (variant_idx / max(1, len(MODELS[model]['variants']) - 1))
    if fuel == 'Diesel':
        price += 150000
    elif fuel == 'Electric':
        price += 300000
    if trans == 'Automatic':
        price += 100000
    elif trans == 'DCT':
        price += 150000
    
    price = round(price + random.randint(-20000, 50000), 2)
    cost_price = round(price * 0.82, 2)
    
    # VIN generation
    vin = f"MAL{random.randint(10000000000000000, 99999999999999999)}"
    
    arrival = random_date(START_DATE, END_DATE)
    
    vehicles_data.append((
        vin, model, variant, fuel, trans, color,
        random.choice([2024, 2025, 2026]), price, cost_price,
        'Available', arrival.strftime('%Y-%m-%d'), arrival.strftime('%Y-%m-%d')
    ))

cursor.executemany("""
    INSERT INTO vehicles (vin, model_name, variant, fuel_type, transmission, color, 
                         manufacturing_year, ex_showroom_price, cost_price, status, arrival_date, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", vehicles_data)
conn.commit()
print(f"s {cursor.rowcount} vehicles generated")

print("\nPhase 3 Part 1 Complete: Customers, Employees, Vehicles created!")

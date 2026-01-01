# generate_data.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_fraud_data(num_rows=20000):
    print(f"Generating synthetic dataset with {num_rows} rows...")
    
    # 1. Setup Categories and Options
    categories = ['personal_care', 'health_fitness', 'misc_pos', 'travel', 
                  'kids_pets', 'shopping_pos', 'food_dining', 'home', 
                  'entertainment', 'grocery_pos', 'gas_transport', 'misc_net']
    
    genders = ['M', 'F']
    
    jobs = ['Scientist', 'Engineer', 'Teacher', 'Artist', 'Manager', 
            'Developer', 'Doctor', 'Sales', 'Driver', 'Accountant']
    
    merchants = ['fraud_Rippin, Kub and Mann', 'fraud_Heller, Gutmann and Zieme', 
                 'fraud_Lind-Buckridge', 'fraud_Kutch, Hermiston and Farrell', 
                 'fraud_Keeling-Crist', 'fraud_Misc_Store']

    data = []

    # 2. Generate Rows
    for i in range(num_rows):
        is_fraud = 0
        
        # Date generation (last 2 years)
        random_days = random.randint(0, 730)
        date = datetime.now() - timedelta(days=random_days)
        trans_date_trans_time = date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Categorical choices
        category = random.choice(categories)
        gender = random.choice(genders)
        job = random.choice(jobs)
        merchant = random.choice(merchants)
        
        # Amount logic: Fraud often has higher or specific amounts, but we keep it random for demo
        # Normal transaction: $1 - $200
        amt = round(random.uniform(1.0, 200.0), 2)
        
        # Inject some fraud cases (roughly 5% of data)
        if random.random() < 0.05:
            is_fraud = 1
            # Fraud transactions might be higher value
            amt = round(random.uniform(100.0, 1000.0), 2)

        # 3. Append row matching the original dataset structure
        row = {
            'Unnamed: 0': i,
            'trans_date_trans_time': trans_date_trans_time,
            'cc_num': random.randint(100000000000, 999999999999),
            'merchant': merchant,
            'category': category,
            'amt': amt,
            'first': 'Fname', # Placeholder
            'last': 'Lname',  # Placeholder
            'gender': gender,
            'street': '123 Fake St',
            'city': 'Cityville',
            'state': 'CA',
            'zip': 90210,
            'lat': 34.0,
            'long': -118.0,
            'city_pop': random.randint(1000, 1000000),
            'job': job,
            'dob': '1980-01-01',
            'trans_num': f'trans_{i}',
            'unix_time': int(date.timestamp()),
            'merch_lat': 34.0,
            'merch_long': -118.0,
            'is_fraud': is_fraud
        }
        data.append(row)

    # 4. Save to CSV
    df = pd.DataFrame(data)
    df.to_csv('fraudTrain.csv', index=False)
    print("Success! 'fraudTrain.csv' has been created.")

if __name__ == "__main__":
    generate_fraud_data()
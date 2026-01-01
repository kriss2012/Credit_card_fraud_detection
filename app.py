# app.py
from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np
import time

app = Flask(__name__)

# Load model and encoders once when app starts
model = joblib.load('fraud_model.pkl')
encoders = joblib.load('encoders.pkl')

@app.route('/')
def home():
    # Pass categories and genders to dropdowns
    categories = encoders['category'].classes_.tolist()
    return render_template('index.html', categories=categories)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # 1. Get User Input
        try:
            category = request.form['category']
            amt = float(request.form['amt'])
            gender = request.form['gender']
            
            # 2. Simulate/Default Hidden Features (Crucial for Demo)
            # We assume a standard user profile for the demo
            merchant = encoders['merchant'].classes_[0] # Default to first merchant
            job = encoders['job'].classes_[0]           # Default to first job
            
            # Randomize location slightly to simulate real transactions
            lat = 40.7128 + np.random.uniform(-0.1, 0.1)
            long = -74.0060 + np.random.uniform(-0.1, 0.1)
            merch_lat = lat + np.random.uniform(-0.05, 0.05) # Merchant is close
            merch_long = long + np.random.uniform(-0.05, 0.05)
            city_pop = 100000
            unix_time = int(time.time())

            # 3. Encode Categorical Data
            # Helper to handle unseen labels gracefully
            def safe_encode(col, val):
                if val in encoders[col].classes_:
                    return encoders[col].transform([val])[0]
                return 0 # Fallback

            input_data = pd.DataFrame({
                'merchant': [safe_encode('merchant', merchant)],
                'category': [safe_encode('category', category)],
                'amt': [amt],
                'gender': [safe_encode('gender', gender)],
                'lat': [lat],
                'long': [long],
                'city_pop': [city_pop],
                'job': [safe_encode('job', job)],
                'unix_time': [unix_time],
                'merch_lat': [merch_lat],
                'merch_long': [merch_long]
            })

            # 4. Predict
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1] * 100

            result = "Fraud" if prediction == 1 else "Legitimate"
            color = "red" if prediction == 1 else "green"

            return render_template('index.html', 
                                   categories=encoders['category'].classes_.tolist(),
                                   prediction_text=f'{result} Transaction',
                                   probability=f'Confidence: {probability:.2f}%',
                                   result_color=color)

        except Exception as e:
            return render_template('index.html', 
                                   categories=encoders['category'].classes_.tolist(),
                                   prediction_text=f'Error: {str(e)}',
                                   result_color="black")

if __name__ == '__main__':
    app.run(debug=True)
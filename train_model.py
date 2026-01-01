# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load Data (Change path to where you have fraudTrain.csv)
print("Loading dataset...")
df = pd.read_csv("fraudTrain.csv")

# 2. Preprocessing
# Convert time to unix like in your notebook
df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
df['unix_time'] = (df['trans_date_trans_time'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

# Drop unnecessary columns
drop_cols = ['Unnamed: 0', 'trans_date_trans_time', 'cc_num', 'first', 'last', 
             'street', 'city', 'state', 'zip', 'dob', 'trans_num']
df = df.drop(columns=drop_cols)

# 3. Handle Imbalanced Data (CRITICAL for 512MB RAM Limit)
# We keep all fraud cases (approx 7500) and sample 7500 non-fraud cases
fraud = df[df['is_fraud'] == 1]
non_fraud = df[df['is_fraud'] == 0].sample(n=len(fraud), random_state=42)
balanced_df = pd.concat([fraud, non_fraud]).sample(frac=1, random_state=42)

print(f"Training on balanced dataset: {balanced_df.shape}")

# 4. Encoding
# We must save these encoders to use them in the web app
encoders = {}
cat_cols = ['merchant', 'category', 'gender', 'job']

for col in cat_cols:
    le = LabelEncoder()
    balanced_df[col] = le.fit_transform(balanced_df[col])
    encoders[col] = le

# 5. Train Model
X = balanced_df.drop('is_fraud', axis=1)
y = balanced_df['is_fraud']

model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
model.fit(X, y)

# 6. Save Model and Encoders
print("Saving model and encoders...")
joblib.dump(model, 'fraud_model.pkl', compress=3)
joblib.dump(encoders, 'encoders.pkl', compress=3)
print("Done! Files saved.")
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

print("Loading dataset...")
df = pd.read_csv('final_dataset.csv')

# Handle NaNs if any
df.fillna(0, inplace=True)

cat_cols = ['merchant_category', 'transaction_type', 'merchant_country_x', 'income_band', 'home_country']
num_cols = ['transaction_amount', 'hours_since_last_txn', 'is_foreign_transaction', 'age', 'credit_score', 'avg_transaction_value', 'merchant_risk_score']

encoders = {}
print("Encoding categorical columns...")
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

X = df[cat_cols + num_cols]
y = df['is_fraud']

print("Training model...")
model = RandomForestClassifier(n_estimators=10, max_depth=10, random_state=42, n_jobs=-1)
model.fit(X, y)

print("Saving artifacts...")
joblib.dump(model, 'fraud_model.joblib')
joblib.dump(encoders, 'encoders.joblib')
print("Model and Encoders saved successfully.")

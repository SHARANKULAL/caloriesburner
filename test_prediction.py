# test_prediction.py
import pandas as pd
import joblib

try:
    imputer = joblib.load('models/imputer.pkl')
    scaler = joblib.load('models/scaler.pkl')
    model = joblib.load('models/calorie_model.pkl')
    print("Models loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    raise

data = pd.DataFrame([{
    'Gender': 1,
    'Age': 30,
    'Height': 175,
    'Weight': 70,
    'Duration': 60,
    'Heart_Rate': 120,
    'Body_Temp': 37.5
}])

print("Input data:", data)
data_imputed = imputer.transform(data)
print("After imputer:", data_imputed)
data_scaled = scaler.transform(data_imputed)
print("After scaler:", data_scaled)
prediction = model.predict(data_scaled)[0]
print(f"Predicted Calories: {prediction:.2f}")
import pandas as pd
import joblib
imputer = joblib.load('models/imputer.pkl')
scaler = joblib.load('models/scaler.pkl')
data = pd.DataFrame([{
    'Gender': 1,
    'Age': 30,
    'Height': 175,
    'Weight': 70,
    'Duration': 60,
    'Heart_Rate': 120,
    'Body_Temp': 37.5
}])
print("Before imputer:", data)
print("After imputer:", imputer.transform(data))
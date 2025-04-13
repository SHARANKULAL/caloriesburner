import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import os

# Load data
data = pd.read_csv('data/calories.csv')

# Drop User_ID and Calories
X = data.drop(['User_ID', 'Calories'], axis=1)
y = data['Calories']

# Verify Gender
print("Gender values:", X['Gender'].unique())  # Should show [1 0]

# Imputation
imputer = SimpleImputer(strategy='mean')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Scaling
scaler = StandardScaler()
X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save models
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/calorie_model.pkl')
joblib.dump(imputer, 'models/imputer.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

print("Model and preprocessors saved successfully")
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import joblib
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load model and preprocessors
try:
    model = joblib.load('models/calorie_model.pkl')
    imputer = joblib.load('models/imputer.pkl')
    scaler = joblib.load('models/scaler.pkl')
    print("Models loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    raise

# MongoDB connection
load_dotenv()
try:
    client = MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client['calorie_db']
    collection = db['users']
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    raise

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict_calories(
    request: Request,
    user_id: str = Form(...),
    gender: str = Form(...),
    age: float = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    duration: float = Form(...),
    heart_rate: float = Form(...),
    body_temp: float = Form(...)
):
    try:
        # Input validation
        if (age < 0 or age > 120 or
            height <= 100 or height > 250 or
            weight <= 20 or weight > 300 or
            duration < 0 or duration > 300 or
            heart_rate <= 30 or heart_rate > 220 or
            body_temp <= 35 or body_temp > 42):
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "Invalid input: Please enter realistic values."}
            )
        if gender not in ['Male', 'Female']:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "Invalid gender: Choose Male or Female."}
            )

        # Map gender
        gender_numeric = 1 if gender == 'Male' else 0

        # Prepare data
        data = {
            'Gender': gender_numeric,
            'Age': age,
            'Height': height,
            'Weight': weight,
            'Duration': duration,
            'Heart_Rate': heart_rate,
            'Body_Temp': body_temp
        }
        df = pd.DataFrame([data])
        print("Input data:", df)

        # Preprocess
        df_imputed = imputer.transform(df)
        print("After imputer:", df_imputed)
        df_scaled = scaler.transform(df_imputed)
        print("After scaler:", df_scaled)

        # Predict
        calories = model.predict(df_scaled)[0]
        print(f"Predicted calories: {calories:.2f}")

        # Store in MongoDB
        user_data = {
            'user_id': user_id,
            'gender': gender,
            'gender_numeric': gender_numeric,
            'age': age,
            'height': height,
            'weight': weight,
            'duration': duration,
            'heart_rate': heart_rate,
            'body_temp': body_temp,
            'calories': float(calories),
            'timestamp': datetime.utcnow().isoformat()
        }
        try:
            result = collection.insert_one(user_data)
            print(f"Inserted document with ID: {result.inserted_id}, user_id: {user_id}")
        except Exception as e:
            print(f"MongoDB insert error: {e}")
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": f"Failed to store data: {str(e)}"}
            )

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "prediction": f"Predicted Calories: {calories:.2f}",
                "user_id": user_id
            }
        )
    except Exception as e:
        print(f"Prediction error: {e}")
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": f"Prediction error: {str(e)}"}
        )
# caloriesburner
project based on calculating calorie of a user by taking various parameter,and built with python which acts as backend and in frontend we used html
to run the program use the below command in your VS code terminal
uvicorn app:app --reload

then select the local host link using ctrl+Enter button
the fike structure should look like this
calorie_predictor/
├── data/
│   └── calories.csv
├── db/
├── models/
│   ├── calorie_model.pkl
│   ├── imputer.pkl
│   ├── scaler.pkl
├── templates/
│   ├── index.html
│   └── history.html
├── app.py
├── retrain_model.py
├── requirements.txt
└── .env

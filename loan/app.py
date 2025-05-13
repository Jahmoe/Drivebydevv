from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the pre-trained model
model = joblib.load('improved_neural_network_model.joblib')

# Load the training data to get feature names
train_data = pd.read_csv('train.csv')
encoded_data = pd.get_dummies(train_data.drop(['loan_status', 'loan_id'], axis=1))
expected_columns = encoded_data.columns.tolist()

@app.route('/')
def home():
    return render_template('loan_prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Create a dictionary for input data
        input_data = {
            'person_age': float(data.get('person_age', 0)),
            'person_income': float(data.get('person_income', 0)),
            'person_emp_exp': int(data.get('person_emp_exp', 0)),
            'loan_amnt': float(data.get('loan_amnt', 0)),
            'loan_int_rate': float(data.get('loan_int_rate', 0)),
            'loan_percent_income': float(data.get('loan_percent_income', 0)),
            'cb_person_cred_hist_length': float(data.get('cb_person_cred_hist_length', 0)),
            'credit_score': int(data.get('credit_score', 0)),
            f'person_gender_{data.get("person_gender", "male")}': 1,
            f'person_home_ownership_{data.get("person_home_ownership", "MORTGAGE")}': 1,
            f'loan_intent_{data.get("loan_intent", "education")}': 1,
            f'previous_loan_defaults_on_file_{data.get("previous_loan_defaults_on_file", "no")}': 1
        }

        # Convert input data to a DataFrame
        input_df = pd.DataFrame([input_data])

        # Align the input data with the expected columns
        for col in expected_columns:
            if col not in input_df:
                input_df[col] = 0

        # Reorder the columns to match the model input
        input_df = input_df[expected_columns]

        # Convert to numpy array
        features = input_df.values

        # Make prediction
        prediction = model.predict(features)[0]

        return jsonify({'prediction': str(prediction)})

    except Exception as e:
        return jsonify({'prediction': 'Error: ' + str(e)})

if __name__ == '__main__':
    app.run(debug=True)

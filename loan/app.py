from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the pre-trained model
model = joblib.load('logistic_regression_model.pkl')

# Feature list (22 columns)
expected_columns = [
    'person_age', 'person_income', 'person_emp_exp', 'loan_amnt', 
    'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length', 'credit_score', 
    'person_gender_male', 'person_education_Bachelor', 'person_education_Master', 
    'person_education_High School', 'person_education_Associate', 
    'person_home_ownership_MORTGAGE', 'person_home_ownership_RENT', 
    'person_home_ownership_OWN', 'loan_intent_EDUCATION', 
    'loan_intent_HOMEIMPROVEMENT', 'loan_intent_MEDICAL', 
    'loan_intent_PERSONAL', 'loan_intent_VENTURE', 
    'previous_loan_defaults_on_file_Yes'
]

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
            'person_gender_male': 1 if data.get('person_gender') == 'male' else 0,
            'person_education_Bachelor': 1 if data.get('person_education') == 'Bachelor' else 0,
            'person_education_Master': 1 if data.get('person_education') == 'Master' else 0,
            'person_education_High School': 1 if data.get('person_education') == 'High School' else 0,
            'person_education_Associate': 1 if data.get('person_education') == 'Associate' else 0,
            'person_home_ownership_MORTGAGE': 1 if data.get('person_home_ownership') == 'MORTGAGE' else 0,
            'person_home_ownership_RENT': 1 if data.get('person_home_ownership') == 'RENT' else 0,
            'person_home_ownership_OWN': 1 if data.get('person_home_ownership') == 'OWN' else 0,
            'loan_intent_EDUCATION': 1 if data.get('loan_intent') == 'EDUCATION' else 0,
            'loan_intent_HOMEIMPROVEMENT': 1 if data.get('loan_intent') == 'HOMEIMPROVEMENT' else 0,
            'loan_intent_MEDICAL': 1 if data.get('loan_intent') == 'MEDICAL' else 0,
            'loan_intent_PERSONAL': 1 if data.get('loan_intent') == 'PERSONAL' else 0,
            'loan_intent_VENTURE': 1 if data.get('loan_intent') == 'VENTURE' else 0,
            'previous_loan_defaults_on_file_Yes': 1 if data.get('previous_loan_defaults_on_file') == 'Yes' else 0
        }

        # Convert input data to a DataFrame and ensure correct order
        input_df = pd.DataFrame([input_data], columns=expected_columns)

        # Convert to numpy array
        features = input_df.values

        # Make prediction
        prediction = model.predict(features)[0]

        # Map prediction to Yes/No
        prediction_text = "Yes" if prediction == 1 else "No"

        return jsonify({'prediction': prediction_text})

    except Exception as e:
        return jsonify({'prediction': 'Error: ' + str(e)})

if __name__ == '__main__':
    app.run(debug=True)

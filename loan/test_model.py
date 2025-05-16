import joblib
import pandas as pd

# Load the trained model
model = joblib.load('logistic_regression_model.pkl')

# Load the test CSV file
test_df = pd.read_csv('train.csv')

# Define the expected columns in the correct order
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

# Check if the test data has the correct columns
if not set(expected_columns).issubset(test_df.columns):
    print("Error: The test.csv file does not contain the expected columns.")
else:
    # Initialize counters
    yes_count = 0
    no_count = 0
    total = len(test_df)

    # Loop through each row in the test DataFrame
    index = 0
    while index < total:
        # Extract the row as a DataFrame
        row = test_df.iloc[[index]][expected_columns]

        # Predict using the model
        prediction = model.predict(row)[0]
        prediction_text = "Yes" if prediction == 1 else "No"

        # Print the result
        print(f"Row {index + 1}: Prediction = {prediction_text}")

        # Count predictions
        if prediction_text == "Yes":
            yes_count += 1
        else:
            no_count += 1
        
        # Move to the next row
        index += 1

    # Summary
    print("\nSummary:")
    print(f"Total rows: {total}")
    print(f"Yes: {yes_count}")
    print(f"No: {no_count}")

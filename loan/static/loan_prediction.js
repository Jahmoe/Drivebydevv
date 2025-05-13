const loanForm = document.getElementById('loanForm');
const predictionResult = document.getElementById('predictionResult');

loanForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const data = {
        person_age: parseFloat(document.getElementById('person_age').value),
        person_gender: document.getElementById('person_gender').value,
        person_education: document.getElementById('person_education').value,
        person_income: parseFloat(document.getElementById('person_income').value),
        person_emp_exp: parseInt(document.getElementById('person_emp_exp').value),
        person_home_ownership: document.getElementById('person_home_ownership').value,
        loan_amnt: parseFloat(document.getElementById('loan_amnt').value),
        loan_intent: document.getElementById('loan_intent').value,
        loan_int_rate: parseFloat(document.getElementById('loan_int_rate').value),
        loan_percent_income: parseFloat(document.getElementById('loan_percent_income').value),
        cb_person_cred_hist_length: parseFloat(document.getElementById('cb_person_cred_hist_length').value),
        credit_score: parseInt(document.getElementById('credit_score').value),
        previous_loan_defaults_on_file: document.getElementById('previous_loan_defaults_on_file').value
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            predictionResult.textContent = `Prediction: ${result.prediction}`;
        } else {
            predictionResult.textContent = 'Error: Server responded with an error.';
        }
    } catch (error) {
        predictionResult.textContent = `Error: ${error.message}`;
    }
});

const loanForm = document.getElementById('loanForm');
const predictionResult = document.getElementById('predictionResult');

loanForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Collect data from the form
    const data = {
        person_age: parseFloat(document.getElementById('person_age').value) || 0,
        person_gender: document.getElementById('person_gender').value,
        person_education: document.getElementById('person_education').value,
        person_income: parseFloat(document.getElementById('person_income').value) || 0,
        person_emp_exp: parseInt(document.getElementById('person_emp_exp').value) || 0,
        person_home_ownership: document.getElementById('person_home_ownership').value,
        loan_amnt: parseFloat(document.getElementById('loan_amnt').value) || 0,
        loan_intent: document.getElementById('loan_intent').value,
        loan_int_rate: parseFloat(document.getElementById('loan_int_rate').value) || 0,
        loan_percent_income: parseFloat(document.getElementById('loan_percent_income').value) || 0,
        cb_person_cred_hist_length: parseFloat(document.getElementById('cb_person_cred_hist_length').value) || 0,
        credit_score: parseInt(document.getElementById('credit_score').value) || 0,
        previous_loan_defaults_on_file: document.getElementById('previous_loan_defaults_on_file').value
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            predictionResult.textContent = `Prediction: ${result.prediction}`;
            predictionResult.style.color = result.prediction === 'Yes' ? '#2ecc71' : '#e74c3c';
        } else {
            predictionResult.textContent = 'Error: Server responded with an error.';
            predictionResult.style.color = '#e74c3c';
        }
    } catch (error) {
        predictionResult.textContent = `Error: ${error.message}`;
        predictionResult.style.color = '#e74c3c';
    }
});

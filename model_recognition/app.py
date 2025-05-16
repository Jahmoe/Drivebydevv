from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load the model only once
MODEL_PATH = './model/vehicle_make_model_finetuned.h5'
NAMES_PATH = './model/names.csv'

# Ensure model file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# Load the model
try:
    print(f"Loading model from: {MODEL_PATH}")
    model = load_model(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# Load vehicle names from CSV file
if not os.path.exists(NAMES_PATH):
    raise FileNotFoundError(f"Vehicle names file not found at {NAMES_PATH}")

try:
    with open(NAMES_PATH, 'r') as file:
        vehicle_names = [line.strip() for line in file if line.strip()]
    print(f"Loaded {len(vehicle_names)} vehicle names.")
except Exception as e:
    print(f"Error loading vehicle names: {e}")
    raise

# Root route to serve the HTML file
@app.route('/')
def home():
    return render_template('model_recognition.html')

@app.route('/predict', methods=['POST'])
def predict():
    print("Predict endpoint hit!")  # Debug log

    # Check if a file is uploaded
    if 'file' not in request.files:
        print("No file uploaded")  # Debug log
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        print("No selected file")  # Debug log
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Open and preprocess the uploaded image
        print(f"Processing file: {file.filename}")  # Debug log
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        image = image.resize((224, 224))  # Resize to model input size
        image = np.array(image) / 255.0  # Normalize to [0, 1]
        image = np.expand_dims(image, axis=0)  # Add batch dimension

        # Check the image shape
        print(f"Image shape: {image.shape}")  # Debug log

        # Make prediction
        prediction = model.predict(image)
        label = np.argmax(prediction, axis=1)[0]

        # Map the predicted label to the vehicle name
        if 0 <= label < len(vehicle_names):
            vehicle_name = vehicle_names[label]
            print(f"Predicted label: {label}, Vehicle Name: {vehicle_name}")
            return jsonify({'prediction': vehicle_name})
        else:
            print(f"Invalid label: {label}")  # Debug log
            return jsonify({'error': f'Invalid label: {label}'}), 500
    except Exception as e:
        print(f"Error during prediction: {e}")  # Debug log
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

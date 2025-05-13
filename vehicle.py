from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
model = load_model('./vehicle_make_model_finetuned.h5')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Open the uploaded image
        image = Image.open(io.BytesIO(file.read())).resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)

        # Make prediction
        prediction = model.predict(image)
        label = np.argmax(prediction, axis=1)[0]

        return jsonify({'prediction': str(label)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

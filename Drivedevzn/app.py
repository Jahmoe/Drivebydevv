from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Mock data for vehicles (could be replaced with a database)
vehicles = [
    {"id": 1, "make": "Toyota", "model": "Corolla", "price": 20000},
    {"id": 2, "make": "Honda", "model": "Civic", "price": 22000},
    {"id": 3, "make": "Ford", "model": "Focus", "price": 18000}
]
@app.route('/')
def home():
    return render_template('index.html')

# Route to get available vehicles
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify(vehicles)

# Route to handle vehicle purchase
@app.route('/api/purchase', methods=['POST'])
def purchase_vehicle():
    data = request.get_json()
    vehicle_id = data.get('vehicleId')
    customer_name = data.get('customerName')
    customer_email = data.get('customerEmail')

    # Find the vehicle by ID
    vehicle = next((v for v in vehicles if v['id'] == vehicle_id), None)

    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    # For simplicity, just return a success message (in reality, you would save this to a database)
    return jsonify({
        "message": f"Thank you {customer_name}! You've successfully purchased a {vehicle['make']} {vehicle['model']} for ${vehicle['price']}."
    })

if __name__ == '__main__':
    app.run(debug=True)

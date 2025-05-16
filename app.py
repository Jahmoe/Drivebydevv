from flask import Flask, render_template, jsonify, request

app = Flask(__name__, static_url_path='/static') 
# Custom Database
vehicles = [
  {"id": 1, "make": "Honda", "model": "Fit (2018)"},
  {"id": 2, "make": "Toyota", "model": "Hiace"},
  {"id": 3, "make": "Subaru", "model": "Impreza"},
  {"id": 4, "make": "Suzuki", "model": "Alto"},
  {"id": 5, "make": "Mercedes-Benz", "model": "C-Class"},
  {"id": 6, "make": "Nissan", "model": "Latio (2014)"},
  {"id": 7, "make": "Hyundai", "model": "Tucson (2020)"},
  {"id": 8, "make": "Kia", "model": "Sportage"},
  {"id": 9, "make": "Mitsubishi", "model": "Outlander"},
  {"id": 10, "make": "Mazda", "model": "Demio (2016)"},
  {"id": 11, "make": "Isuzu", "model": "D-Max"},
  {"id": 12, "make": "Ford", "model": "EcoSport (2021)"},
  {"id": 13, "make": "Chevrolet", "model": "Cruze (2014)"},
  {"id": 14, "make": "Peugeot", "model": "208 (2020)"},
  {"id": 15, "make": "Renault", "model": "Duster"},
  {"id": 16, "make": "Volkswagen", "model": "Polo ()2016"},
  {"id": 17, "make": "BMW", "model": "X1 (2019)"},
  {"id": 18, "make": "Audi", "model": "Q3 (2021)"},
  {"id": 19, "make": "Jeep", "model": "Compass (2020)"},
  {"id": 20, "make": "MG", "model": "ZS (NEW)"},
  {"id": 21, "make": "BYD", "model": "Yuan Plus EV (2024)"},
  {"id": 21, "make": "Honda", "model": "CR-V EX"},
  {"id": 22, "make": "Honda", "model": "HR-V V LX"},
  {"id": 23, "make": "Honda", "model": "Civic Touring Sedan"},
  {"id": 24, "make": "Honda", "model": "Accord LX"},
  {"id": 25, "make": "Honda", "model": "Pilot"},
  {"id": 26, "make": "Honda", "model": "Stream (2011)"},
  {"id": 27, "make": "Honda", "model": "Passport Trailsport"},
  {"id": 28, "make": "Honda", "model": "BR-V"},
  {"id": 29, "make": "Toyota", "model": "Probox"},
  {"id": 30, "make": "Toyota", "model": "Corolla Axio"},
  {"id": 31, "make": "Toyota", "model": "Corolla Fielder"},
  {"id": 32, "make": "Toyota", "model": "Yaris Cross (2021)"},
  {"id": 33, "make": "Toyota", "model": "RAV4 (2019)"},
  {"id": 34, "make": "Toyota", "model": "Fortuner (2022)"},
  {"id": 35, "make": "Toyota", "model": "Raize (2021)"},
  {"id": 36, "make": "Toyota", "model": "Passo"},
  {"id": 37, "make": "Toyota", "model": "Prius"},
  {"id": 38, "make": "Toyota", "model": "Avalon"},
  {"id": 39, "make": "Toyota", "model": "Crown"},
  {"id": 40, "make": "Toyota", "model": "Vitz"},
  {"id": 41, "make": "Toyota", "model": "Vanguard (2011)"},
  {"id": 42, "make": "Toyota", "model": "Mark X"},
  {"id": 43, "make": "Toyota", "model": "Noah"},
  {"id": 44, "make": "Toyota", "model": "Camry"},
  {"id": 45, "make": "Toyota", "model": "Altis (2015)"}
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

    return jsonify({
        "message": f"Thank you {customer_name}! You've successfully purchased a {vehicle['make']} {vehicle['model']} for ${vehicle['price']}."
    })
@app.route('/model_recognition')
def model_recognition():
    return render_template('model_recognition.html')

if __name__ == '__main__':
    app.run(debug=True)

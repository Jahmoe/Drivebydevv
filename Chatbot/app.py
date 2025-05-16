from flask import Flask, request, jsonify, render_template
import json
from transformers import pipeline

app = Flask(__name__)

with open("vehicles.json") as f:
    vehicles = json.load(f)

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Generate a list of vehicle-related intents
labels = [
    "manufacturer info", "model info", "price info", "fuel type",
    "fuel efficiency", "tank size", "vehicle type", "use case", "description"
]

def classify_and_respond(query):
    query = query.strip()
    result = classifier(query, labels)
    top_label = result["labels"][0]

    # Search vehicle data for best match
    for vehicle in vehicles:
        if vehicle["model"].lower() in query.lower() or vehicle["manufacturer"].lower() in query.lower():
            if top_label == "manufacturer info":
                return {"message": f"The {vehicle['model']} is manufactured by {vehicle['manufacturer']}."}
            elif top_label == "model info":
                return {"message": f"{vehicle['model']}: {vehicle['description']}"}
            elif top_label == "price info":
                return {"message": f"The price of the {vehicle['model']} is {vehicle['price']}."}
            elif top_label == "fuel type":
                return {"message": f"The {vehicle['model']} uses {vehicle['fuel_type']}."}
            elif top_label == "fuel efficiency":
                return {"message": f"The fuel efficiency of the {vehicle['model']} is {vehicle['fuel_efficiency']}."}
            elif top_label == "tank size":
                return {"message": f"The {vehicle['model']} has a tank size of {vehicle['tank_size']}."}
            elif top_label == "vehicle type":
                return {"message": f"The {vehicle['model']} is classified as a {vehicle['vehicle_type']}."}
            elif top_label == "use case":
                return {"message": f"The {vehicle['model']} is typically used for {vehicle['use_case']}."}
            elif top_label == "description":
                return {"message": vehicle['description']}
    return {"message": "I'm sorry, I don't have information on that vehicle."}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat")
def chat():
    query = request.args.get("query", "")
    if not query.strip():
        return jsonify({"message": "Please ask a question."})
    response = classify_and_respond(query)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)

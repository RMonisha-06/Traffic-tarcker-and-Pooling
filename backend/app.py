from flask import Flask, request, jsonify
from flask_cors import CORS
import pyrebase

app = Flask(__name__)
CORS(app)

# Firebase config from firebase_config.py
from firebase_config import firebaseConfig
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Update bus location
@app.route('/update_bus_location', methods=['POST'])
def update_bus_location():
    data = request.json
    db.child("buses").child(data['bus_id']).set(data)
    return jsonify({"status": "success"}), 200

# Get bus location
@app.route('/get_bus_location/<bus_id>', methods=['GET'])
def get_bus_location(bus_id):
    bus = db.child("buses").child(bus_id).get().val()
    return jsonify(bus), 200

# Offer a ride
@app.route('/offer_ride', methods=['POST'])
def offer_ride():
    data = request.json
    db.child("rides").push(data)
    return jsonify({"status": "ride offered"}), 200

# Search for rides
@app.route('/search_rides', methods=['GET'])
def search_rides():
    source = request.args.get('source')
    destination = request.args.get('destination')
    all_rides = db.child("rides").get().val()
    matches = []
    if all_rides:
        for key, ride in all_rides.items():
            if ride['source'] == source and ride['destination'] == destination:
                ride['id'] = key
                matches.append(ride)
    return jsonify(matches), 200

if __name__ == '__main__':
    app.run(debug=True)

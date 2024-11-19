import json
from geopy.distance import geodesic
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load masjid locations from the JSON file
def load_masjid_locations(filename="masjid_locations.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

MASJIDS = load_masjid_locations()

@app.route("/geo_checkin", methods=["POST"])
def geo_checkin():
    """
    Receive user location and verify masjid attendance.
    """
    data = request.json
    user_location = data.get("location")  # {"latitude": 21.4225, "longitude": 39.8262}
    miner_address = data.get("miner")
    prayer_count = data.get("prayer_count", 1)

    if not user_location or not miner_address:
        return jsonify({"error": "Invalid data"}), 400

    user_coords = (user_location["latitude"], user_location["longitude"])
    for masjid in MASJIDS:
        masjid_coords = (masjid["latitude"], masjid["longitude"])
        distance = geodesic(user_coords, masjid_coords).meters  # Calculate distance in meters
        if distance <= 50:  # Allow 50 meters of error
            reward = {
                "miner": miner_address,
                "location": masjid["name"],
                "prayer_count": prayer_count,
                "reward_type": "MuslimCoin",
                "reward_amount": prayer_count * 5,  # Example: 5 coins per prayer
            }
            return jsonify({"message": f"Check-in successful at {masjid['name']}", "reward": reward}), 200

    return jsonify({"error": "No registered masjid found near your location"}), 400

if __name__ == "__main__":
    app.run(debug=True)

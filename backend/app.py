from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)

@app.route('/location', methods=['POST'])
def get_address():
    try:
        data = request.json
        latitude = data['latitude']
        longitude = data['longitude']

        print(f"Received request: Lat={latitude}, Lon={longitude}")  # Debug log

        geolocator = Nominatim(user_agent="my_geo_app")
        try:
            location = geolocator.reverse((latitude, longitude), language="en", timeout=10)
        except GeocoderTimedOut:
            print("Geocoder timed out")  # Debug log
            return jsonify({"error": "Geocoder service timed out. Try again."}), 500

        if location:
            print(f"Location found: {location.address}")  # Debug log
            address = location.raw.get("address", {})
            area = address.get("suburb", address.get("village", address.get("town", "Unknown Area")))
            region = address.get("state", "Unknown Region")
            country = address.get("country", "Unknown Country")

            return jsonify({
                "latitude": latitude,
                "longitude": longitude,
                "area": area,
                "region": region,
                "country": country,
                "full_address": location.address
            })
        else:
            print("Address not found")  # Debug log
            return jsonify({"error": "Unable to fetch address. Check internet connection."}), 400

    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

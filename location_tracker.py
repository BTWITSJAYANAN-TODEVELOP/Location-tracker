import requests
from geopy.geocoders import Nominatim

def get_location():
    try:
        # Fetch IP-based location data
        response = requests.get("https://ipinfo.io/json", timeout=5)  # Added timeout for reliability
        data = response.json()

        # Extract location details
        ip = data.get("ip", "Unknown")
        city = data.get("city", "Unknown")
        region = data.get("region", "Unknown")
        country = data.get("country", "Unknown")
        loc = data.get("loc", "0,0")  # Latitude, Longitude as a string

        print(f"IP Address: {ip}")
        print(f"Location: {city}, {region}, {country}")
        print(f"Coordinates: {loc}")

        # Split coordinates into latitude and longitude
        lat, lon = loc.split(",")

        # Convert coordinates to detailed address
        geolocator = Nominatim(user_agent="geoapi")
        location = geolocator.reverse((lat, lon), language="en")

        if location:
            print(f"Detailed Address: {location.address}")
        else:
            print("Unable to fetch a detailed address.")

    except requests.exceptions.RequestException as req_err:
        print(f"Network Error: {req_err}")
    except ValueError:
        print("Invalid coordinates received.")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# Run the function
get_location()

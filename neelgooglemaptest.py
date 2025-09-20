import requests

API_KEY = "AIzaSyAqTxkwjnnlo8wOzLzXe-Q9AnyXQ9JslWs"

def get_gps_coordinates():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}"

    # Empty payload means: just use IP (low accuracy)
    payload = {}

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        lat = data["location"]["lat"]
        lng = data["location"]["lng"]
        accuracy = data["accuracy"]
        print(f"Latitude: {lat}, Longitude: {lng} (±{accuracy}m)")
    else:
        print("Error:", response.text)

get_gps_coordinates()
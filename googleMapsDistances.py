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
        return(lat,lng)
        #print(f"Latitude: {lat}, Longitude: {lng} (±{accuracy}m)")
    else:
        #print("Error:", response.text)
        return (29.5636, -95.2861)


def walking_distance_time(coord_1, coord_2):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    

    origin_lat, origin_lon = coord_1
    dest_lat, dest_lon = coord_2

    params = {
        "origins": f"{origin_lat},{origin_lon}",
        "destinations": f"{dest_lat},{dest_lon}",
        "mode": "walking",
        "units": "imperial",  # or "imperial"
        "key": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    try:
        element = data["rows"][0]["elements"][0]
        if element["status"] == "OK":
            distance_text = element["distance"]["text"]
            distance_value = element["distance"]["value"]  # in meters
            duration_text = element["duration"]["text"] # e.g., "1 hour 5 mins"
            duration_value = element["duration"]["value"]  # in seconds
            
            return {
                "Distance": distance_text,
                "Distance (m)": distance_value,
                "Duration (hours)": duration_text,
                "Duration (seconds)": duration_value
            }
        else:
            return {"error": element["status"]}
    except Exception as e:
        return {"error": str(e)}


result = walking_distance_time(get_gps_coordinates(), (29.60078, -95.61840))  
print(result)



#print(get_gps_coordinates())
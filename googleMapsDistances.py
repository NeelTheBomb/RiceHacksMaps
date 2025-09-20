import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

API_KEY = "AIzaSyAqTxkwjnnlo8wOzLzXe-Q9AnyXQ9JslWs"


def get_gps_coordinates_webscrape():
    # Store profile folder next to script (cross-platform)
    profile_dir = os.path.join(os.getcwd(), "chrome_gps_profile")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_dir}")
    options.add_argument("--profile-directory=Default")

    driver = webdriver.Chrome(service=Service(), options=options)

    # Load a page that requests location
    driver.get("https://my-location.org/")  # can swap for another site

    print("👉 Allow location access in Chrome popup (only once).")
    time.sleep(10)  # wait for user to click Allow

    try:
        lat = driver.find_element(By.ID, "latitude").text
        lon = driver.find_element(By.ID, "longitude").text
        print(f"Latitude: {lat}, Longitude: {lon}")
    except:
        print("Could not extract coordinates. Check site structure.")

    driver.quit()




def get_gps_coordinates():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}"

    # Empty payload means: just use IP (low accuracy)
    #payload = {}
    payload = {
    "considerIp": "true",
    "wifiAccessPoints": [
        {
            "macAddress": "01:23:45:67:89:AB",
            "signalStrength": -65,
            "signalToNoiseRatio": 40
        },
        {
            "macAddress": "01:23:45:67:89:AC",
            "signalStrength": -70,
            "signalToNoiseRatio": 35
        }
    ]
    }

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
print(get_gps_coordinates_webscrape())


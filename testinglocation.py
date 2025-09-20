# Importing Necessary Modules
import requests
from selenium import webdriver
import folium
import geopy.distance

# this method will return us our actual coordinates
# using our ip address
def locationCoordinates():
    try:
        response = requests.get('https://ipinfo.io/')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        return lat, long
    except:
        return (29.5636, -95.2861)
    
def get_distance_between_coordinates(coords_1, coords_2):
    random_multiplier_constant = 1.2
    return geopy.distance.geodesic(coords_1, coords_2).miles * random_multiplier_constant

# Main method
if __name__ == "__main__":
    print(locationCoordinates())
    print(get_distance_between_coordinates((29.715517808137946, -95.3981633652495), (29.717148331431076, -95.41513943245693)))

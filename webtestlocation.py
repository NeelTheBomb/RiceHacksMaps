import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def get_gps_coordinates():
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

get_gps_coordinates()

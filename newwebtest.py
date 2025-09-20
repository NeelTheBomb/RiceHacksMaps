import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service

def get_gps_coordinates():
    # Profile so Edge remembers location permission after first run
    profile_dir = os.path.join(os.getcwd(), "edge_gps_profile")

    options = webdriver.EdgeOptions()
    options.add_argument(f"user-data-dir={profile_dir}")

    driver = webdriver.Edge(service=Service(), options=options)

    # Open a blank page
    driver.get("about:blank")

    # Inject JS that asks for geolocation
    js_script = """
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}),
            err => reject(err)
        );
    });
    """

    print("👉 Allow location access in the popup (only the first time).")
    coords = driver.execute_async_script("""
        const callback = arguments[0];
        navigator.geolocation.getCurrentPosition(
            pos => callback({lat: pos.coords.latitude, lon: pos.coords.longitude}),
            err => callback({error: err.message})
        );
    """)

    if "error" in coords:
        print("Error:", coords["error"])
    else:
        print(f"Latitude: {coords['lat']}, Longitude: {coords['lon']}")

    driver.quit()

get_gps_coordinates()

# get_gps.py
from flask import Flask, request, render_template_string, jsonify
import webbrowser
import threading
import time

app = Flask(__name__)

# Simple page that asks for geolocation and POSTs back to /coords
PAGE = """
<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Share Location</title></head>
  <body>
    <h2>Share location with this page</h2>
    <p>Click the button and allow location access when prompted.</p>
    <button onclick="getLocation()">Share location</button>
    <pre id="out"></pre>

    <script>
      function getLocation() {
        if (!navigator.geolocation) {
          document.getElementById('out').textContent = 'Geolocation not supported.';
          return;
        }
        navigator.geolocation.getCurrentPosition(success, error, {enableHighAccuracy: true, timeout: 10000});
      }
      function success(pos) {
        const coords = {lat: pos.coords.latitude, lon: pos.coords.longitude, accuracy: pos.coords.accuracy};
        document.getElementById('out').textContent = JSON.stringify(coords, null, 2);
        fetch('/coords', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(coords)
        }).then(r => r.text()).then(t => console.log(t));
      }
      function error(err) {
        document.getElementById('out').textContent = 'Error: ' + err.message;
      }
    </script>
  </body>
</html>
"""

# will hold last coords received
LAST_COORDS = None

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/coords', methods=['POST'])
def coords():
    global LAST_COORDS
    data = request.get_json()
    LAST_COORDS = data
    print("Received coords:", data)
    return "OK"

@app.route('/get_last')
def get_last():
    return jsonify(LAST_COORDS or {})

def open_browser():
    time.sleep(1)  # let flask start
    webbrowser.open("http://localhost:5000")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app.run(port=5000, debug=False)

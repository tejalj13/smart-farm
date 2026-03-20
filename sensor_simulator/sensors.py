import random
import time
import requests

FOG_URL = "http://127.0.0.1:5000/data"  # Fog node endpoint

def generate_sensor_data():
    return {
        "temperature": random.uniform(15, 40),
        "humidity": random.uniform(40, 90),
        "soil_moisture": random.uniform(20, 80),
        "leaf_wetness": random.uniform(0, 1),
        "light_intensity": random.uniform(100, 1000)
    }

while True:
    data = generate_sensor_data()
    print("Sending sensor data:", data)
    requests.post(FOG_URL, json=data)
    time.sleep(2)  # configurable frequency

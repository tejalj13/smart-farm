import json
import time
import random

FILE = "sensor_data.json"

while True:
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

    data["soil_moisture"] = random.uniform(20, 80)

    with open(FILE, "w") as f:
        json.dump(data, f)

    print("Soil Moisture:", data["soil_moisture"])
    time.sleep(2)

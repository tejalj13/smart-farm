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

    data["humidity"] = random.uniform(40, 90)

    with open(FILE, "w") as f:
        json.dump(data, f)

    print("Humidity:", data["humidity"])
    time.sleep(2)

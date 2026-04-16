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

    data["light_intensity"] = random.uniform(100, 1000)

    with open(FILE, "w") as f:
        json.dump(data, f)

    print("Light:", data["light_intensity"])
    time.sleep(2)

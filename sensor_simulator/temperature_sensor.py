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

    data["temperature"] = random.uniform(15, 40)

    with open(FILE, "w") as f:
        json.dump(data, f)

    print("Temperature:", data["temperature"])
    time.sleep(2)

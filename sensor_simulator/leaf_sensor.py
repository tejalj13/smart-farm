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

    data["leaf_wetness"] = random.uniform(0, 1)

    with open(FILE, "w") as f:
        json.dump(data, f)

    print("Leaf Wetness:", data["leaf_wetness"])
    time.sleep(2)

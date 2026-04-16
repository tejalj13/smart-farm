import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# 📁 Path to shared sensor file
FILE = "../sensor_simulator/sensor_data.json"

# 🔐 AWS IoT Config
ENDPOINT = "ay9h3u8xtlcgi-ats.iot.us-east-1.amazonaws.com"

ROOT_CA = "AmazonRootCA1.pem"
PRIVATE_KEY = "fa5499b69acb5356b7a60500db1e50e43305a4815368a0bea12998b3b347e2b0-private.pem.key"
CERTIFICATE = "fa5499b69acb5356b7a60500db1e50e43305a4815368a0bea12998b3b347e2b0-certificate.pem.crt"

TOPIC = "smartfarm/sensors"

# 🧠 Required fields
REQUIRED_FIELDS = [
    "temperature",
    "humidity",
    "soil_moisture",
    "leaf_wetness",
    "light_intensity"
]

# 🔥 Risk Logic


def detect_risk(data):
    if data["humidity"] > 80 and data["leaf_wetness"] > 0.7:
        return "HIGH"
    elif data["humidity"] > 60:
        return "MEDIUM"
    return "LOW"


# 🚀 MQTT Client Setup
client = AWSIoTMQTTClient("smartFarmClient")

client.configureEndpoint(ENDPOINT, 8883)

client.configureCredentials(
    ROOT_CA,
    PRIVATE_KEY,
    CERTIFICATE
)

# 🔧 Improve stability (IMPORTANT)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

print("Connecting to AWS IoT...")
client.connect()
print("Connected to AWS IoT")

# 🔄 Main Loop
while True:
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        print("Waiting for sensor data...")
        time.sleep(2)
        continue

    # 🚨 Ensure all sensor values are present
    if not all(key in data for key in REQUIRED_FIELDS):
        print("Incomplete data, skipping...")
        time.sleep(2)
        continue

    # 🧠 Add risk
    data["risk"] = detect_risk(data)

    print("Fog sending:", data)

    try:
        client.publish(TOPIC, json.dumps(data), 1)
        print("Sent successfully")
    except Exception as e:
        print("Publish failed:", str(e))

    # ⏱️ Slow down to avoid timeout
    time.sleep(5)

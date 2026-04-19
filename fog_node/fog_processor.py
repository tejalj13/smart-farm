import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


FILE = "../sensor_simulator/sensor_data.json"

# AWS IoT Config
ENDPOINT = "ay9h3u8xtlcgi-ats.iot.us-east-1.amazonaws.com"

ROOT_CA = "AmazonRootCA1.pem"
PRIVATE_KEY = "fa5499b69acb5356b7a60500db1e50e43305a4815368a0bea12998b3b347e2b0-private.pem.key"
CERTIFICATE = "fa5499b69acb5356b7a60500db1e50e43305a4815368a0bea12998b3b347e2b0-certificate.pem.crt"

TOPIC = "smartfarm/sensors"

REQUIRED_FIELDS = [
    "temperature",
    "humidity",
    "soil_moisture",
    "leaf_wetness",
    "light_intensity"
]


def detect_risk(data):
    temp = data["temperature"]
    humidity = data["humidity"]
    leaf = data["leaf_wetness"]
    soil = data["soil_moisture"]
    light = data["light_intensity"]

    # HIGH RISK
    if humidity > 80 and leaf > 0.7 and 20 < temp < 30:
        return "HIGH"

    # MEDIUM RISK
    elif humidity > 60 and (leaf > 0.5 or soil > 70 or light < 300):
        return "MEDIUM"

    # LOW RISK
    return "LOW"


client = AWSIoTMQTTClient("smartFarmClient")

client.configureEndpoint(ENDPOINT, 8883)

client.configureCredentials(
    ROOT_CA,
    PRIVATE_KEY,
    CERTIFICATE
)


client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

print("Connecting to AWS IoT...")
client.connect()
print("Connected to AWS IoT")


while True:
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        print("Waiting for sensor data...")
        time.sleep(2)
        continue

    if not all(key in data for key in REQUIRED_FIELDS):
        print("Incomplete data, skipping...")
        time.sleep(2)
        continue

    data["risk"] = detect_risk(data)

    print("Fog sending:", data)

    try:
        client.publish(TOPIC, json.dumps(data), 1)
        print("Sent successfully")
    except Exception as e:
        print("Publish failed:", str(e))

    time.sleep(5)

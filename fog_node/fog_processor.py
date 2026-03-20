from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:8080/api/sensor-data/"


def detect_disease_risk(data):
    return True   # 👈 TEMP: send all data


@app.route('/data', methods=['POST'])
def process_data():
    data = request.json

    print("Received at fog:", data)

    if detect_disease_risk(data):
        print("Sending to backend:", data)

        requests.post(BACKEND_URL, json={
            **data,
            "risk": "HIGH"
        })
    else:
        print("Normal data ignored")

    return jsonify({"status": "processed"})


if __name__ == '__main__':
    app.run(port=5000)

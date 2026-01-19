import ssl
import json
import time
import os
import random
import paho.mqtt.client as mqtt
from device_context import DEVICE_ID, DEVICE_ROLE, WORLD, uptime

# ============================
# AWS IoT Core Configuration
# ============================
IOT_ENDPOINT = "a3vm4tlq95958f-ats.iot.ap-south-1.amazonaws.com"
IOT_PORT = 8883

CA_CERT_PATH = "/root/sentinelmesh/certs/AmazonRootCA1.pem"
DEVICE_CERT_PATH = "/root/sentinelmesh/certs/cert.crt"
PRIVATE_KEY_PATH = "/root/sentinelmesh/certs/key.key"

# ============================
# Certificate Sanity Check
# ============================
def check_certificates():
    print("Checking certificate files...")
    print("Root CA exists:", os.path.exists(CA_CERT_PATH))
    print("Device cert exists:", os.path.exists(DEVICE_CERT_PATH))
    print("Private key exists:", os.path.exists(PRIVATE_KEY_PATH))

# ============================
# Air Purity Index Logic
# (numeric score ONLY)
# ============================
def clamp01(x):
    return max(0.0, min(1.0, x))

def compute_air_score(pm25, pm10, co2, voc, humidity):
    pm25_score = clamp01(pm25 / 35.0)
    pm10_score = clamp01(pm10 / 50.0)
    co2_score  = clamp01(co2 / 1000.0)
    voc_score  = clamp01(voc / 500.0)
    hum_score  = clamp01(abs(humidity - 50.0) / 50.0)

    air_score = (
        0.35 * pm25_score +
        0.20 * pm10_score +
        0.20 * co2_score +
        0.15 * voc_score +
        0.10 * hum_score
    )

    return round(air_score, 4)

# ============================
# Sensor Simulation
# ============================
def generate_air_sensors():
    return {
        "pm25": round(random.uniform(5, 60), 2),
        "pm10": round(random.uniform(10, 80), 2),
        "co2": round(random.uniform(400, 2000), 1),
        "voc": round(random.uniform(50, 800), 1),
        "humidity": round(random.uniform(30, 70), 1)
    }

# ============================
# MQTT Callbacks
# ============================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to AWS IoT Core!")
    else:
        print(f"Connection failed. RC={rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published")

# ============================
# MQTT Setup
# ============================
def setup_mqtt_client():
    client = mqtt.Client(client_id=DEVICE_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.tls_set(
        ca_certs=CA_CERT_PATH,
        certfile=DEVICE_CERT_PATH,
        keyfile=PRIVATE_KEY_PATH,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )

    return client

def connect_mqtt(client):
    print("Connecting to AWS IoT Core...")
    client.connect(IOT_ENDPOINT, IOT_PORT, 60)
    client.loop_start()
    print("MQTT loop started")

# ============================
# Telemetry Publisher
# ============================
def publish_telemetry(client):
    while True:
        sensors = generate_air_sensors()

        air_score = compute_air_score(
            sensors["pm25"],
            sensors["pm10"],
            sensors["co2"],
            sensors["voc"],
            sensors["humidity"]
        )

        payload = {
            "device_id": DEVICE_ID,
            "role": DEVICE_ROLE,
            "world": WORLD,
            "uptime": uptime(),
            "ts": int(time.time()),

            # Raw physical data
            "air": sensors,

            # Derived numeric feature
            "air_score": air_score
        }

        topic = f"factory/{WORLD}/{DEVICE_ROLE}/{DEVICE_ID}/telemetry"
        print(f"Publishing → {topic}")
        print(json.dumps(payload, indent=2))

        client.publish(topic, json.dumps(payload), qos=1)
        time.sleep(5)

# ============================
# Main
# ============================
def main():
    check_certificates()
    client = setup_mqtt_client()
    connect_mqtt(client)
    publish_telemetry(client)

if __name__ == "__main__":
    main()

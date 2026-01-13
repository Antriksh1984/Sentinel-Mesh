import ssl
import json
import time
import paho.mqtt.client as mqtt
import os
from device_context import DEVICE_ID, DEVICE_ROLE, WORLD, uptime

# IoT Core endpoint
IOT_ENDPOINT = "xxxxx.iot.us-west-2.amazonaws.com"  # Replace with your IoT Core endpoint

# Setup the MQTT client
client = mqtt.Client(client_id=DEVICE_ID)

# Load certificates
client.tls_set(
    ca_certs="/home/ubuntu/sentinelmesh/certs/AmazonRootCA1.pem",  # Path to Root CA
    certfile=f"/home/ubuntu/sentinelmesh/certs/{DEVICE_ID}.crt",    # Path to device cert
    keyfile=f"/home/ubuntu/sentinelmesh/certs/{DEVICE_ID}.key",      # Path to device key
    tls_version=ssl.PROTOCOL_TLSv1_2
)

# Connect to AWS IoT Core (TLS secured MQTT)
client.connect(IOT_ENDPOINT, 8883, 60)  # Port 8883 is the default for MQTT over TLS
client.loop_start()  # Start the MQTT loop

# Publish device telemetry every 5 seconds
while True:
    payload = {
        "device_id": DEVICE_ID,
        "role": DEVICE_ROLE,
        "world": WORLD,
        "uptime": uptime(),
        "ts": int(time.time())  # Timestamp for the telemetry
    }

    # Topic structure: factory/{world}/{role}/{device_id}/telemetry
    topic = f"factory/{WORLD}/{DEVICE_ROLE}/{DEVICE_ID}/telemetry"

    # Publish the telemetry
    client.publish(topic, json.dumps(payload), qos=1)
    
    time.sleep(5)  # Publish every 5 seconds

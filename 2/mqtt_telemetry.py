import ssl
import json
import time
import paho.mqtt.client as mqtt
import os
from device_context import DEVICE_ID, DEVICE_ROLE, WORLD, uptime

# IoT Core endpoint (replace with your endpoint)
IOT_ENDPOINT = "a3vm4tlq95958f-ats.iot.ap-south-1.amazonaws.com"  

# Define certificate file paths
CA_CERT_PATH = "/root/sentinelmesh/certs/AmazonRootCA1.pem"
DEVICE_CERT_PATH = "/root/sentinelmesh/certs/cert.crt"
PRIVATE_KEY_PATH = "/root/sentinelmesh/certs/key.key"

# Check if the certificate files exist
def check_certificates():
    print("Checking certificate files...")
    print(f"Root CA file exists: {os.path.exists(CA_CERT_PATH)}")
    print(f"Device certificate exists: {os.path.exists(DEVICE_CERT_PATH)}")
    print(f"Device key exists: {os.path.exists(PRIVATE_KEY_PATH)}")

# Setup MQTT client
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to AWS IoT Core!")
        client.subscribe(f"factory/{WORLD}/{DEVICE_ROLE}/{DEVICE_ID}/telemetry/response")
    else:
        print(f"Failed to connect to AWS IoT Core. Result code: {rc}")


def on_publish(client, userdata, mid):
    """Callback for when a message is published."""
    print(f"Message {mid} published.")

def setup_mqtt_client():
    """Set up the MQTT client and its callbacks."""
    client = mqtt.Client(client_id=DEVICE_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish
    return client

# Configure and start MQTT client connection
def connect_mqtt(client):
    """Connect to AWS IoT Core."""
    client.tls_set(
        ca_certs=CA_CERT_PATH,
        certfile=DEVICE_CERT_PATH,
        keyfile=PRIVATE_KEY_PATH,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )

    try:
        print("Connecting to AWS IoT Core...")
        client.connect(IOT_ENDPOINT, 8883, 60)
        client.loop_start()  # Start the MQTT loop for async operation
        print("MQTT client connected and loop started.")
    except Exception as e:
        print(f"Failed to connect: {e}")

# Publish telemetry data
def publish_telemetry(client):
    """Publish device telemetry every 5 seconds."""
    while True:
        payload = {
            "device_id": DEVICE_ID,
            "role": DEVICE_ROLE,
            "world": WORLD,
            "uptime": uptime(),
            "ts": int(time.time())  # Timestamp for the telemetry
        }

        topic = f"factory/{WORLD}/{DEVICE_ROLE}/{DEVICE_ID}/telemetry"
        print(f"Publishing to topic: {topic} with payload: {json.dumps(payload)}")

        client.publish(topic, json.dumps(payload), qos=1)
        time.sleep(5)  # Publish every 5 seconds

# Main execution flow
def main():
    """Main function to run the entire telemetry script."""
    # Check certificates before proceeding
    check_certificates()

    # Setup MQTT client
    client = setup_mqtt_client()

    # Connect to AWS IoT Core
    connect_mqtt(client)

    # Publish telemetry data
    publish_telemetry(client)

# Run the main function
if __name__ == "__main__":
    main()

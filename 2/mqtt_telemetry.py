import ssl
import json
import time
import paho.mqtt.client as mqtt
from device_context import DEVICE_ID, DEVICE_ROLE, WORLD, uptime

IOT_ENDPOINT = "endpoint-placeholder.amazonaws.com"

client = mqtt.Client(client_id=DEVICE_ID)
client.tls_set(
    ca_certs="AmazonRootCA1.pem",
    certfile=f"{DEVICE_ID}.crt",
    keyfile=f"{DEVICE_ID}.key",
    tls_version=ssl.PROTOCOL_TLSv1_2
)

client.connect(IOT_ENDPOINT, 8883, 60)
client.loop_start()

while True:
    payload = {
        "device_id": DEVICE_ID,
        "role": DEVICE_ROLE,
        "world": WORLD,
        "uptime": uptime(),
        "ts": int(time.time())
    }

    topic = f"factory/{WORLD}/{DEVICE_ROLE}/{DEVICE_ID}/telemetry"
    client.publish(topic, json.dumps(payload), qos=1)

    time.sleep(5)

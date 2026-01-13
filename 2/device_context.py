import os
import uuid
import time
import random

DEVICE_ID = os.getenv("DEVICE_ID", f"ot-{uuid.getnode():x}")
DEVICE_ROLE = os.getenv("DEVICE_ROLE", "plc")  # plc | camera | sensor
WORLD = os.getenv("WORLD", "production")       # production | deception

BOOT_TIME = time.time()

def uptime():
    return int(time.time() - BOOT_TIME)

def deterministic_noise(seed, scale=1.0):
    random.seed(seed + int(time.time() // 10))
    return random.uniform(-scale, scale)

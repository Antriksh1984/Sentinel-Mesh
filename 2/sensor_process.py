import time
import math
from device_context import deterministic_noise

BASE_TEMP = 68.0

while True:
    temp = BASE_TEMP + math.sin(time.time()/60)*4 + deterministic_noise(42, 0.6)
    pressure = 30 + deterministic_noise(7, 0.3)
    vibration = 0.02 + deterministic_noise(99, 0.005)

    print(f"T={temp:.2f} P={pressure:.2f} V={vibration:.4f}")
    time.sleep(5)

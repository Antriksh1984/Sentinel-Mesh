from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import threading
import random
import time

def registers():
    base = [1200, 2400, 3600, 4800]
    return base + [random.randint(0, 65535) for _ in range(16)]

store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, registers()),
    ir=ModbusSequentialDataBlock(0, registers())
)

context = ModbusServerContext(slaves=store, single=True)

threading.Thread(
    target=lambda: StartTcpServer(context, address=("0.0.0.0", 502)),
    daemon=True
).start()

while True:
    time.sleep(10)

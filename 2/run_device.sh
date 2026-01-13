#!/bin/bash
python3 ssh_banner.py &
python3 mqtt_telemetry.py &

if [ "$DEVICE_ROLE" = "plc" ]; then
  python3 plc_modbus.py &
  python3 plc_panel.py &
elif [ "$DEVICE_ROLE" = "camera" ]; then
  python3 camera_http.py &
elif [ "$DEVICE_ROLE" = "sensor" ]; then
  python3 sensor_process.py &
fi

wait

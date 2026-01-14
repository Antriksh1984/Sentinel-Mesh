import pymysql
import os

conn = pymysql.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    database=os.environ["DB_NAME"],
    connect_timeout=5
)

REQUIRED_FIELDS = [
    "device_id", "role", "world", "ts", "uptime",
    "pm25", "pm10", "co2", "voc", "humidity", "air_score"
]

def lambda_handler(event, context):
    # ---- Validation ----
    for field in REQUIRED_FIELDS:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")

    cur = conn.cursor()

    sql = """
    INSERT INTO telemetry (
      device_id, role, world, ts, uptime,
      pm25, pm10, co2, voc, humidity,
      air_score, mitm
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cur.execute(sql, (
        event["device_id"],
        event["role"],
        event["world"],
        event["ts"],
        event["uptime"],
        event["pm25"],
        event["pm10"],
        event["co2"],
        event["voc"],
        event["humidity"],
        event["air_score"],
        event.get("mitm", False)
    ))

    conn.commit()
    return {"status": "ok"}

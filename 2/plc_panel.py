from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/status")
def status():
    return jsonify({
        "mode": "AUTO",
        "scan_ms": 500,
        "cpu_load": round(random.uniform(0.55, 0.75), 2),
        "fault": False
    })

app.run(host="0.0.0.0", port=8080)

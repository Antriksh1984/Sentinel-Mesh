from flask import Flask, Response
import time

app = Flask(__name__)

@app.route("/live")
def live():
    def gen():
        while True:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n\xff\xd8\xff"
            time.sleep(0.25)
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

app.run(host="0.0.0.0", port=80)

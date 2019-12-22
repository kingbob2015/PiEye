from flask import Response, Flask, render_template
import threading
import cv2

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

def gen():
    while True:
        with lock:
            if outputFrame is None:
                continue
            ret, encodedImage = cv2.imencode(".jpg", outputFrame)
            if not ret:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
			bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    app.run()
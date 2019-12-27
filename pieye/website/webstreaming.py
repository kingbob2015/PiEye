"""
This file handles the web server and streaming of video for PiEye. Runs a Flask web server.
"""
from flask import Response, Flask, render_template
import threading
import cv2

# global variable for output frame so it can be set by the main logic loop
outputFrame = None
# Lock for manipulating the output frame to avoid race conditions
lock = threading.Lock()

app = Flask(__name__)


def gen():
    """
    Generates an output from the output frame that can be rendered by the webpage
    """
    while True:
        with lock:
            if outputFrame is None:
                continue
            ret, encodedImage = cv2.imencode(".jpg", outputFrame)
            if not ret:
                continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run()

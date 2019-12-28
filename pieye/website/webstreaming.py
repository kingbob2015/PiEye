"""
This file handles the web server and streaming of video for PiEye. Runs a Flask web server.
"""
from flask import Response, Flask, render_template
import threading
import cv2
from log.logger import Logger, LogLevel

# The logger instance
logger = Logger.get_instance()
# global variable for output frame so it can be set by the main logic loop
outputFrame = None
# Lock for manipulating the output frame to avoid race conditions
lock = threading.Lock()
# Kill switch
kill_switch = False

app = Flask(__name__)


def set_output_frame(frame):
    """
    Sets the new output frame

    @param: frame: the new output frame
    """
    global outputFrame
    outputFrame = frame


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


@app.route("/kill_app")
def kill_app():
    """
    When activated from the HTML webpage, sets the kill switch to true which triggers a boolean in the main app loop
    """
    with lock:
        global kill_switch
        kill_switch = True
        return "Shutting down..."


if __name__ == '__main__':
    app.run()

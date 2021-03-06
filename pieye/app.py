"""
This file is the main bootstrap for PiEye. Handles setting up the application and the main control loop.
"""
import cv2
import os
import imutils
from threading import Thread, Lock
import datetime
import sys

from config.config import Config
from log.logger import Logger, LogLevel
from motionDetection.motiondetection import MotionDetector
from messaging.messenger import TextMessenger
import website.webstreaming

# Constant to define the delay to send a new motion detection message
MESSAGE_DELAY = 100

# Threshold variable to start motion detection with minimum number of frames
md_frameCount = 5
# The current frame being analyzed
current_frame = None
# Total frame count
total_frames = 0
# The camera that is being used to retrieve frames
camera = None
# The logger instance
logger = None


def run():
    """
    Entry point for the program. Starts the web server in its own thread and begins the main loop.
    """

    # Create our logger singleton instance for the rest of the application to use
    global logger
    logger = Logger.get_instance()

    global camera
    camera = TempCamera()

    try:
        web_app = Thread(target=website.webstreaming.app.run,
                         kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': True, 'use_reloader': False,
                                 'threaded': True})
        web_app.daemon = True
        web_app.start()
        main_loop()
    except Exception as e:
        logger.log("Web server failed to start: " + str(e), LogLevel.ERROR)

def main_loop():
    """
    Main logic loop for the program.
    """

    global current_frame
    global total_frames
    global camera
    global logger

    # Load up our config to pass to components that need it
    config = Config(os.path.dirname(os.path.abspath(__file__)) + "/config.json")
    print(config)

    # Create the motion detect object
    md = MotionDetector(accumWeight=0.1)
    motion_detected = False
    lastMotionMessageSent = datetime.datetime.now()

    # Create our text messenger object
    text_messenger = TextMessenger(config)

    while True:
        current_frame = camera.get_frame()
        total_frames += 1
        try:
            current_frame = imutils.resize(current_frame, width=1080)
        except AttributeError as e:
            if current_frame is None:
                logger.log("current frame was none", LogLevel.ERROR)
            else:
                logger.log("failed to resize current frame: " + str(e), LogLevel.ERROR)

        try:
            motion_detected = motion_detect(md)
        except Exception as e:
            logger.log("Motion detection function failed: " + str(e), LogLevel.ERROR)
            motion_detected = False

        # Send message if motion detection occurred
        if motion_detected:
            current_time = datetime.datetime.now()
            if (current_time - lastMotionMessageSent).total_seconds() > MESSAGE_DELAY:
                lastMotionMessageSent = current_time
                text_messenger.send_message("Bob", "Motion occurred on your PiEye!!!")


        # Send our frame to the output frame in the web server to display
        with website.webstreaming.lock:
            # Kills the application based on a switch in the web server. Could be done a better way to have a callback.
            if website.webstreaming.kill_switch:
                camera.delete()
                break
            else:
                try:
                    website.webstreaming.set_output_frame(current_frame.copy())
                except AttributeError as e:
                    if current_frame is None:
                        logger.log("current frame was none", LogLevel.ERROR)
                    else:
                        logger.log("failed to copy current frame: " + str(e), LogLevel.ERROR)
    logger.log("Exiting Application", LogLevel.INFO)
    sys.exit()


def motion_detect(md):
    """
    Function handles the control logic of motion detection. Currently adds a box around the motion if it is detected
    via the MotionDetector object.

    @param: md: the motion detector object
    """
    global current_frame
    global total_frames
    global md_frameCount

    motion_detected = False

    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    timestamp = datetime.datetime.now()
    cv2.putText(current_frame, timestamp.strftime(
        "%A %d %B %Y %I:%M:%S%p"), (10, current_frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    if total_frames > md_frameCount:
        motion = md.detect(gray)

        if motion is not None:
            (thresh, (minX, minY, maxX, maxY)) = motion
            cv2.rectangle(current_frame, (minX, minY), (maxX, maxY),
                          (0, 0, 255), 2)
            motion_detected = True
    md.update(gray)
    return motion_detected


# TEMP CODE THAT WILL BE SUBBED FOR REAL CODE
class TempCamera:
    def __init__(self):
        self._cam = cv2.VideoCapture(0)
        self.frame = None
        ret, self.frame = self._cam.read()
        Thread(target=self._update, args=()).start()

    def __del__(self):
        self.release_camera()

    def _update(self):
        while True:
            ret, self.frame = self._cam.read()

    def get_frame(self):
        return self.frame

    def release_camera(self):
        self._cam.release()
        cv2.destroyAllWindows()

    def delete(self):
        self.__del__()


# END TEMP CODE


if __name__ == '__main__':
    # TODO: Add in command line parameters to Python module for config file path and such
    run()

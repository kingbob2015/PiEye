import cv2
import os
from imutils.video import VideoStream
import imutils
from threading import Thread
import datetime
from config.config import Config
from log.logger import Logger, LogLevel
from motionDetection.motiondetection import MotionDetector
import website.webstreaming

md_frameCount = 5
current_frame = None
total_frames = 0
camera = None

def run():
    global camera
    camera = TempCamera()
    t = Thread(target=main_loop, args=())
    t.daemon = True
    t.start()

    website.webstreaming.app.run(host='0.0.0.0', port=5555, debug=True, use_reloader=False, threaded=True)

    t.join()

    camera.delete()

def main_loop():
    """
    Main loop for the program
    """

    global current_frame
    global total_frames
    global camera

    # Create our logger singleton instance for the rest of the application to use
    logger = Logger.get_instance()

    # Load up our config to pass to components that need it
    config = Config(os.path.dirname(__file__) + "/config.json")

    md = MotionDetector(accumWeight=0.1)

    # t = Thread(target=website.webstreaming.app.run, kwargs={'host': '0.0.0.0', 'port': '5555', 'debug': True, 'threaded': True, 'use_reloader': False})
    # t.daemon = True
    # t.start()

    while True:
        current_frame = camera.get_frame()
        total_frames += 1
        current_frame = imutils.resize(current_frame, width=400)

        motion_detect(md)

        with website.webstreaming.lock:
            website.webstreaming.outputFrame = current_frame.copy()
        # TEMP CODE FOR SHOWING AN IMAGE

        cv2.imshow('frame', current_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # END TEMP CODE



def motion_detect(md):
    global current_frame
    global total_frames
    global md_frameCount

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

    md.update(gray)


# TEMP CODE THAT WILL BE SUBBED FOR REAL CODE
class TempCamera:
    def __init__(self):
        self.__cam = cv2.VideoCapture(0)
        self.frame = None
        ret, self.frame = self.__cam.read()
        Thread(target=self.__update, args=()).start()

    def __del__(self):
        self.release_camera()

    def __update(self):
        while True:
            ret, self.frame = self.__cam.read()

    def get_frame(self):
        return self.frame

    def release_camera(self):
        self.__cam.release()
        cv2.destroyAllWindows()

    def delete(self):
        self.__del__()

# END TEMP CODE


if __name__ == '__main__':
    # TODO: Add in command line parameters to Python module for config file path and such
    run()
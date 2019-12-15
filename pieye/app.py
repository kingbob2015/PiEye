import cv2
import os
from config.config import Config
from log.logger import Logger, LogLevel


def run():
    """
    Main loop for the program
    """

    # Create our logger singleton instance for the rest of the application to use
    logger = Logger.get_instance()

    # Load up our config to pass to components that need it
    config = Config(os.path.dirname(__file__)+"/config.json")
    camera = TempCamera()
    while True:
        frame = camera.next_frame()
        if temp_motion_detect(frame):
            temp_message_system(config.get_config("messaging"), "Bob", "Hey Bob Some Motion Was Detected")

        # TEMP CODE FOR SHOWING AN IMAGE
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # END TEMP CODE

    camera.delete()

# TEMP CODE THAT WILL BE SUBBED FOR REAL CODE


def temp_motion_detect(frame):
    return True


def temp_message_system(config, name, message):
    # Would need some error handling here in actual messaging system
    if config:
        print(config)
        print("Sending {} to {} at {}".format(message, name, config["names_to_numbers"][name]))


class TempCamera:
    def __init__(self):
      self.__cam = cv2.VideoCapture(0)

    def __del__(self):
        self.release_camera()

    def next_frame(self):
        ret, frame = self.__cam.read()
        return frame

    def release_camera(self):
        self.__cam.release()
        cv2.destroyAllWindows()

    def delete(self):
        self.__del__()

# END TEMP CODE


if __name__ == '__main__':
    # TODO: Add in command line parameters to Python module for config file path and such
    run()
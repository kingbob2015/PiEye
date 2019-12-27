"""
This class handles motion detection for the application in a single spot motion detection algorithm.
Code credit to Adrian Rosebrock https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
"""

import numpy as np
import imutils
import cv2


class MotionDetector:
    """
    Motion detection class that accumulates historical image data to determine if motion occurs
    """

    def __init__(self, accumWeight=0.5):
        # The larger accum weight is the less the background will be factored into the weighted average
        self.accumWeight = accumWeight
        self.bg = None

    def update(self, image):
        """
        Function to update the image history/ accumulated weight

        @param: image: the image used to add to the accumulated weight
        """
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return

        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image, tVal=25):
        """
        Function to detect motion from a new image and the accumulated weight

        @param: image: the image to detect motion detection on
        @param: tVal: the threshold value used to mark a pixel as motion or not

        @return: None if no motion or a tuple of the threshold image and a bounding box (thresh, (minx, miny, maxx, maxy))
        """
        # compute the absolute difference between the background model
        # and the image passed in, then threshold the delta image
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]

        # perform a series of erosions and dilations to remove small
        # blobs
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours in the thresholded image and initialize the
        # minimum and maximum bounding box regions for motion
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        # if no contours were found, return None
        if len(cnts) == 0:
            return None

        # otherwise, loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and use it to
            # update the minimum and maximum bounding box regions
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))

        # otherwise, return a tuple of the thresholded image along
        # with bounding box
        return (thresh, (minX, minY, maxX, maxY))

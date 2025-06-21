"""-------------------------------------------------------
PresenceAI: Module Description Here
-------------------------------------------------------
Author:  JD
ID:      91786
Uses:    OpenCV
Version:  1.0.9
__updated__ = Sat Jun 21 2025
-------------------------------------------------------
"""

import cv2 as cv


def flip_image(img):
    return cv.flip(img, 1)


def resize_frame(img, FRAME_WIDTH=640, FRAME_HEIGHT=480):
    return cv.resize(img, (FRAME_WIDTH, FRAME_HEIGHT))

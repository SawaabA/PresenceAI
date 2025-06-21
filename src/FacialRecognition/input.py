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


def get_video_capture(index=0):
    cap = cv.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam")
    return cap
